#!/usr/bin/env python3
"""自动修复 .nbt 结构文件，使其 size 与实际方块坐标匹配，兼容 Litematica。

用法:
    python nbt-fixer.py <文件或目录> [--overwrite]

零依赖，仅需 Python 3 标准库。
"""

import gzip
import struct
import sys
import os
import argparse
from pathlib import Path


class NBTReader:

    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def _b(self):
        v = struct.unpack(">b", self.data[self.pos : self.pos + 1])[0]
        self.pos += 1
        return v

    def _H(self):
        v = struct.unpack(">H", self.data[self.pos : self.pos + 2])[0]
        self.pos += 2
        return v

    def _i(self):
        v = struct.unpack(">i", self.data[self.pos : self.pos + 4])[0]
        self.pos += 4
        return v

    def _q(self):
        v = struct.unpack(">q", self.data[self.pos : self.pos + 8])[0]
        self.pos += 8
        return v

    def _str(self):
        length = self._H()
        s = self.data[self.pos : self.pos + length].decode("utf-8", errors="replace")
        self.pos += length
        return s

    def _payload(self, tag: int):
        if tag == 1:
            return self._b()
        if tag == 2:
            v = struct.unpack(">h", self.data[self.pos : self.pos + 2])[0]
            self.pos += 2
            return v
        if tag == 3:
            return self._i()
        if tag == 4:
            return self._q()
        if tag == 5:
            v = struct.unpack(">f", self.data[self.pos : self.pos + 4])[0]
            self.pos += 4
            return v
        if tag == 6:
            v = struct.unpack(">d", self.data[self.pos : self.pos + 8])[0]
            self.pos += 8
            return v
        if tag == 7:
            length = self._i()
            self.pos += length
            return f"<byte[{length}]>"
        if tag == 8:
            return self._str()
        if tag == 9:
            subtype = self.data[self.pos]
            self.pos += 1
            length = self._i()
            return [self._payload(subtype) for _ in range(length)]
        if tag == 10:
            d = {}
            while self.pos < len(self.data) and self.data[self.pos] != 0:
                t2 = self.data[self.pos]
                self.pos += 1
                key = self._str()
                d[key] = self._payload(t2)
            self.pos += 1
            return d
        if tag == 11:
            length = self._i()
            return [self._i() for _ in range(length)]
        if tag == 12:
            length = self._i()
            return [self._q() for _ in range(length)]
        return None

    def read_root(self) -> dict:
        self.pos += 1
        self._str()
        return self._payload(10)


def patch_size(raw: bytearray) -> tuple[list[int], int]:
    """返回 (旧size值, size字段起始偏移)。找不到则抛 ValueError。"""
    i = 0
    while i < len(raw) - 20:
        if raw[i] != 0x09:
            i += 1
            continue
        name_len = struct.unpack(">H", raw[i + 1 : i + 3])[0]
        if name_len > 256 or i + 3 + name_len > len(raw):
            i += 1
            continue
        name = raw[i + 3 : i + 3 + name_len]
        if name != b"size":
            i += 1
            continue

        off = i + 3 + name_len
        if off + 5 > len(raw):
            continue

        subtype = raw[off]
        list_len = struct.unpack(">i", raw[off + 1 : off + 5])[0]
        if subtype != 3 or list_len != 3:
            i += 1
            continue

        val_start = off + 5
        old = [struct.unpack(">i", raw[val_start + j * 4 : val_start + j * 4 + 4])[0] for j in range(3)]
        return old, val_start

    raise ValueError("未找到 'size' 标签")


def analyze_nbt(filepath: Path) -> dict | None:
    try:
        with open(filepath, "rb") as f:
            compressed = f.read()

        raw = gzip.decompress(compressed)
        reader = NBTReader(raw)
        data = reader.read_root()

        blocks = data.get("blocks", [])
        declared_size = data.get("size", [0, 0, 0])
        dv = data.get("DataVersion", 0)

        if not blocks or len(declared_size) != 3:
            return None

        xs = [b["pos"][0] for b in blocks]
        ys = [b["pos"][1] for b in blocks]
        zs = [b["pos"][2] for b in blocks]

        actual = [max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, max(zs) - min(zs) + 1]

        return {
            "filepath": filepath,
            "data_version": dv,
            "declared": declared_size,
            "actual": actual,
            "block_count": len(blocks),
            "raw_size": len(raw),
            "compressed_size": len(compressed),
        }

    except Exception as e:
        print(f"  ✗ 解析失败: {e}", file=sys.stderr)
        return None


def fix_nbt(filepath: Path, overwrite: bool = False) -> Path | None:
    info = analyze_nbt(filepath)
    if info is None:
        return None

    if info["declared"] == info["actual"]:
        print(f"  ✓ 无需修复")
        return None

    # 读取原始数据
    with open(filepath, "rb") as f:
        compressed = f.read()

    raw = bytearray(gzip.decompress(compressed))
    _, val_start = patch_size(raw)

    for j, v in enumerate(info["actual"]):
        struct.pack_into(">i", raw, val_start + j * 4, v)

    new_compressed = gzip.compress(bytes(raw))

    if overwrite:
        out = filepath
    else:
        out = filepath.with_name(f"{filepath.stem}_fixed.nbt")

    with open(out, "wb") as f:
        f.write(new_compressed)

    print(f"  ✓ size: {info['declared']} → {info['actual']}")
    print(f"  → 输出: {out}")
    return out


def process_path(path: Path, overwrite: bool = False):
    if path.is_file():
        if path.suffix.lower() == ".nbt":
            print(f"\n📦 {path.name}  ({path.stat().st_size / 1024:.1f} KB)")
            fix_nbt(path, overwrite=overwrite)
        else:
            print(f"⏭  跳过非 .nbt 文件: {path.name}")
    elif path.is_dir():
        nbt_files = sorted(path.glob("*.nbt"))
        if not nbt_files:
            print(f"未找到 .nbt 文件: {path}")
            return
        print(f"找到 {len(nbt_files)} 个 .nbt 文件\n")
        for i, f in enumerate(nbt_files, 1):
            print(f"[{i}/{len(nbt_files)}] {f.name}  ({f.stat().st_size / 1024:.1f} KB)")
            fix_nbt(f, overwrite=overwrite)
    else:
        print(f"✗ 路径不存在: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="自动修复 .nbt 结构文件的 size 字段，使其兼容 Litematica。"
    )
    parser.add_argument(
        "target",
        help=".nbt 文件或包含 .nbt 的目录",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="直接覆盖原文件（默认生成 *_fixed.nbt）",
    )
    args = parser.parse_args()

    path = Path(args.target)
    print(f"nbt-fixer | {'覆盖模式' if args.overwrite else '生成 *_fixed.nbt'}")
    process_path(path, overwrite=args.overwrite)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
refresh_stats.py — 2026-06-24 新增
====================================
被 .github/workflows/refresh-stats.yml 调用
────────────────────────────────────────────
功能：
  1. 调 Cloudflare Analytics GraphQL API 拿过去 30 天 PV/UV
  2. 原地更新 data/site-stats.yaml（用正则替换字段值，保留所有 # 注释）
  3. 自动更新 _meta.last_refreshed_at

依赖（GitHub Actions runner 自带）：
  - python3
  - re / urllib.request（标准库，无第三方依赖）

所需环境变量（在 GitHub Actions Secrets 配）：
  CF_API_TOKEN       Cloudflare API Token（Analytics: Read 权限）
  CF_ZONE_ID         Cloudflare Zone ID（lyrumu.top 的）

失败行为：
  - CF API 失败 → 打印 errors 字段 + 仍写 yaml（time + 0 值），workflow 标 success
  - YAML 写入失败 → 抛异常退出 1
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta


# =============================================================================
# 常量
# =============================================================================
DATA_PATH = "data/site-stats.yaml"
CF_GQL = "https://api.cloudflare.com/client/v4/graphql"

CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "")
CF_ZONE_ID = os.environ.get("CF_ZONE_ID", "")


# =============================================================================
# 工具函数
# =============================================================================
def cf_gql_query(query):
    """调 CF Analytics GraphQL API，返回 dict（含 errors 字段如有）"""
    body = json.dumps({"query": query}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(CF_GQL, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        # CF 返回 4xx/5xx 时 body 仍是 JSON（errors 字段）
        raw = e.read()
        try:
            err = json.loads(raw)
            print(f"ERR: CF HTTP {e.code}: {json.dumps(err)[:500]}", file=sys.stderr)
        except Exception:
            print(f"ERR: CF HTTP {e.code}: {raw[:500].decode('utf-8', errors='replace')}", file=sys.stderr)
        raise
    return json.loads(raw)


# =============================================================================
# 数据拉取
# =============================================================================
def fetch_cf():
    """返回 dict: {last30_pv, last30_uv}"""
    result = {"last30_pv": 0, "last30_uv": 0}
    if not CF_API_TOKEN or not CF_ZONE_ID:
        print("WARN: CF_API_TOKEN / CF_ZONE_ID empty, skip CF fetch", file=sys.stderr)
        return result

    # 30 天前的日期（CF 保留 30 天）
    date_30d_ago = (datetime.now(timezone.utc) - timedelta(days=31)).strftime("%Y-%m-%d")
    query = f"""
    query {{
      viewer {{
        zones(filter: {{ zoneTag: "{CF_ZONE_ID}" }}) {{
          httpRequests1dGroups(
            limit: 31
            filter: {{ date_gt: "{date_30d_ago}" }}
          ) {{
            sum {{
              requests
              uniqueVisitors
            }}
          }}
        }}
      }}
    }}
    """
    try:
        data = cf_gql_query(query)

        # 把 CF API errors 字段打出来（之前被吞了）
        if isinstance(data, dict) and data.get("errors"):
            print(f"ERR: CF API errors: {json.dumps(data['errors'])[:500]}", file=sys.stderr)
            return result

        # 防御 NoneType：CF 返回 data: null 时
        data_field = data.get("data") if isinstance(data, dict) else None
        if not data_field:
            print(f"WARN: CF data field is null/empty, raw: {json.dumps(data)[:500]}", file=sys.stderr)
            return result

        viewer = data_field.get("viewer") or {}
        zones = viewer.get("zones") or []
        if not zones:
            print(f"WARN: CF returned no zones", file=sys.stderr)
            return result

        groups = zones[0].get("httpRequests1dGroups", []) or []
        total_pv = sum((g["sum"]["requests"] for g in groups), 0)
        total_uv = sum((g["sum"]["uniqueVisitors"] for g in groups), 0)
        result["last30_pv"] = total_pv
        result["last30_uv"] = total_uv
        print(f"CF: last30_pv={total_pv} last30_uv={total_uv}", file=sys.stderr)
    except urllib.error.HTTPError:
        # cf_gql_query 已 print，不重复
        pass
    except Exception as e:
        print(f"ERR: CF fetch failed: {e}", file=sys.stderr)

    return result


# =============================================================================
# 原地更新 yaml（用正则替换，保留所有 # 注释）
# =============================================================================
def update_yaml_field(content, key, value):
    """把 `  key: ...` 替换为 `  key: value`，支持 # 行尾注释"""
    # 匹配 `  key: ` 后面的整个 value 字段（不跨行）
    pattern = re.compile(
        rf"^(\s*{re.escape(key)}\s*:\s*)[^\n#]*",
        re.MULTILINE,
    )
    new_content, n = pattern.subn(rf"\g<1>{value}", content)
    if n == 0:
        print(f"WARN: yaml field '{key}' not found, skipping", file=sys.stderr)
    return new_content


def update_yaml(content, last30_pv, last30_uv, timestamp):
    """原地更新 3 个字段"""
    content = update_yaml_field(content, "last_refreshed_at", f"'{timestamp}'")
    content = update_yaml_field(content, "last30_pv", str(last30_pv))
    content = update_yaml_field(content, "last30_uv", str(last30_uv))
    return content


# =============================================================================
# 主流程
# =============================================================================
def main():
    # 1. 读 yaml 文本（保留所有 # 注释）
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"ERR: read yaml failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. 拉数据
    cf = fetch_cf()

    # 3. 准备新值
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 4. 原地更新 yaml（保留 # 注释）
    new_content = update_yaml(content, cf["last30_pv"], cf["last30_uv"], timestamp)

    # 5. 写回
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("OK: site-stats.yaml updated", file=sys.stderr)
    except Exception as e:
        print(f"ERR: write yaml failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
refresh_stats.py — 2026-06-24 新增
====================================
被 .github/workflows/refresh-stats.yml 调用
────────────────────────────────────────────
功能：
  1. 调 Cloudflare Analytics GraphQL API 拿过去 30 天 PV/UV
  2. 写回 data/site-stats.yaml
  3. 自动更新 _meta.last_refreshed_at

依赖（GitHub Actions runner 自带）：
  - python3
  - pyyaml
  - urllib.request（标准库）

所需环境变量（在 GitHub Actions Secrets 配）：
  CF_API_TOKEN       Cloudflare API Token（Analytics: Read 权限）
  CF_ZONE_ID         Cloudflare Zone ID（lyrumu.top 的）

失败行为：
  - CF API 失败不阻塞整个 workflow（异常打 stderr，但脚本仍尝试写 yaml）
  - YAML 解析失败 → 抛异常退出 1
  - 写 yaml 失败 → 抛异常退出 1
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)


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
    """调 CF Analytics GraphQL API"""
    body = json.dumps({"query": query}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(CF_GQL, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


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
        zones = (
            data.get("data", {})
            .get("viewer", {})
            .get("zones", [])
        )
        if not zones:
            print(f"WARN: CF returned no zones, raw: {json.dumps(data)[:500]}", file=sys.stderr)
            return result
        groups = zones[0].get("httpRequests1dGroups", [])
        total_pv = sum(g["sum"]["requests"] for g in groups)
        total_uv = sum(g["sum"]["uniqueVisitors"] for g in groups)
        result["last30_pv"] = total_pv
        result["last30_uv"] = total_uv
        print(f"CF: last30_pv={total_pv} last30_uv={total_uv}", file=sys.stderr)
    except Exception as e:
        print(f"ERR: CF fetch failed: {e}", file=sys.stderr)

    return result


# =============================================================================
# 主流程
# =============================================================================
def main():
    # 1. 读现有 yaml
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"ERR: read yaml failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 兼容空 section
    data.setdefault("_meta", {})
    data.setdefault("visitors", {})

    # 2. 拉数据
    cf = fetch_cf()

    # 3. 更新字段（只动数据，保留 _meta.first_pv_at 等用户填的字段）
    data["visitors"]["last30_pv"] = cf["last30_pv"]
    data["visitors"]["last30_uv"] = cf["last30_uv"]

    # 4. 写时间戳
    data["_meta"]["last_refreshed_at"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    # 5. 写回 yaml（保留注释不行 — safe_dump 不支持，加 custom representer 略复杂）
    # 实际方案：先保留 _meta 字段顺序，safe_dump 简单粗暴就行
    try:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print("OK: site-stats.yaml updated", file=sys.stderr)
    except Exception as e:
        print(f"ERR: write yaml failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

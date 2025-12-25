#!/usr/bin/env python3
"""
Reddit MCP Server - シンプル版
データ取得のみ。分析はClaude Project指示プロンプトで行う。
"""

import asyncio
import json
import os
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# API設定
API_BASE_URL = "https://mainweb-production.up.railway.app"
JWT_TOKEN = os.environ.get("REDDIT_API_TOKEN", "")

server = Server("reddit-api")


def get_headers() -> dict:
    headers = {"Content-Type": "application/json"}
    if JWT_TOKEN:
        headers["Authorization"] = f"Bearer {JWT_TOKEN}"
    return headers


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_reddit_posts",
            description="Reddit投稿を取得。subreddit、検索、日付、ソート順でフィルタ可能。",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit": {
                        "type": "string",
                        "description": "Subreddit名（部分一致）例: stablediffusion, comfyui, localllama"
                    },
                    "search": {
                        "type": "string",
                        "description": "検索キーワード"
                    },
                    "date_from": {
                        "type": "string",
                        "description": "開始日 (YYYY-MM-DD)"
                    },
                    "date_to": {
                        "type": "string",
                        "description": "終了日 (YYYY-MM-DD)"
                    },
                    "ordering": {
                        "type": "string",
                        "description": "ソート順。例: -score(スコア降順), -created_utc(新しい順), score, created_utc"
                    },
                    "custom_feed": {
                        "type": "string",
                        "description": "カスタムフィード名"
                    },
                    "page": {
                        "type": "integer",
                        "description": "ページ番号（デフォルト: 1）",
                        "default": 1
                    },
                    "favorites_only": {
                        "type": "boolean",
                        "description": "お気に入りのみ取得（デフォルト: false）",
                        "default": False
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "get_reddit_posts":
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    try:
        # パラメータ構築
        params = {"page": arguments.get("page", 1)}
        
        if arguments.get("subreddit"):
            params["subreddit__icontains"] = arguments["subreddit"]
        if arguments.get("search"):
            params["search"] = arguments["search"]
        if arguments.get("date_from"):
            params["created_utc__date__gte"] = arguments["date_from"]
        if arguments.get("date_to"):
            params["created_utc__date__lte"] = arguments["date_to"]
        if arguments.get("ordering"):
            params["ordering"] = arguments["ordering"]
        if arguments.get("custom_feed"):
            params["custom_feeds__name__icontains"] = arguments["custom_feed"]
        
        # エンドポイント選択
        endpoint = "/api/B_ApiRedditPost/favorites/" if arguments.get("favorites_only") else "/api/B_ApiRedditPost/posts/"
        
        # API呼び出し
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{API_BASE_URL}{endpoint}",
                params=params,
                headers=get_headers(),
            )
            response.raise_for_status()
            data = response.json()
        
        # 結果をJSON形式で返す
        return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]
    
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"APIエラー: {e.response.status_code}")]
    except Exception as e:
        return [TextContent(type="text", text=f"エラー: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

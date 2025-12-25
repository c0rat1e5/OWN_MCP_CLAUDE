# Reddit Analysis MCP Server

Claude Desktop用のMCPサーバー。Reddit投稿を取得し、Claude Projectの指示プロンプトで分析します。

## 機能

- `get_reddit_posts` - Reddit投稿を取得（フィルタ・検索対応）

## セットアップ

### 1. 仮想環境作成 & 依存関係インストール

```bash
cd reddit_mcp_server
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### 2. Claude Desktop設定

`%APPDATA%\Claude\claude_desktop_config.json` に追加:

```json
{
  "mcpServers": {
    "reddit-analyzer": {
      "command": "C:\\path\\to\\reddit_mcp_server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\reddit_mcp_server\\server.py"],
      "env": {
        "REDDIT_API_TOKEN": ""
      }
    }
  }
}
```

### 3. Claude Desktop再起動

## Claude Project プロンプト

用途に応じて使用:

| ファイル | 用途 |
|----------|------|
| `Claude_Project_Reddit_AI_Analyzer_Prompt.md` | AI・画像生成・LLM分析 |
| `Claude_Project_Reddit_Invest_Prompt.md` | 投資・株式分析 |
| `Claude_Project_Reddit_WebDev_Prompt.md` | Web開発分析 |

## API

- Base URL: `https://mainweb-production.up.railway.app`
- Endpoints: `/api/B_ApiRedditPost/posts/`, `/api/B_ApiRedditPost/favorites/`

## License

MIT

# Reddit Analysis MCP Server

Claude Desktop用のMCPサーバー。Reddit投稿を取得・分析し、Obsidian形式で出力します。

## 機能

- **get_reddit_posts**: Reddit投稿を取得（フィルタ・検索対応）
- **get_reddit_favorites**: お気に入り投稿を取得
- **analyze_posts_invest**: 投資・株式分析の観点でObsidian形式に変換
- **analyze_posts_webdev**: Web開発の観点でObsidian形式に変換
- **get_recent_posts**: 直近N日間の投稿を取得

## セットアップ

### 1. 依存関係のインストール

```bash
cd reddit_mcp_server
pip install -r requirements.txt
```

### 2. 環境変数（オプション）

JWT認証が必要な場合:

```bash
set REDDIT_API_TOKEN=your_jwt_token_here
```

### 3. Claude Desktop設定

`claude_desktop_config.json` に以下を追加:

```json
{
  "mcpServers": {
    "reddit-analyzer": {
      "command": "python",
      "args": ["C:\\Users\\canto\\Downloads\\OWN_MCP_CLAUDE\\reddit_mcp_server\\server.py"],
      "env": {
        "REDDIT_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## 使用例

Claude Desktopで以下のように使用できます：

- 「直近の投稿を取得して」
- 「r/wallstreetbetsの投稿を投資分析して」
- 「Reactに関するWeb開発の投稿を分析して」
- 「お気に入りの投稿を表示して」

# VS Code Setup

Optional tooling for this repo. All items are independent — set up what applies to your environment.

**Note:** `mcp.json` and `settings.json` are shipped as `.example` files so VS Code doesn't
auto-load them and produce errors on clone. Copy them when you're ready to set up:

```bash
cp .vscode/mcp.example.json .vscode/mcp.json
cp .vscode/settings.example.json .vscode/settings.json
```

---

## 1. Recommended Extensions

VS Code will prompt you to install recommended extensions when you open the repo.
Or install manually:

- **LookML** (`Looker.lkml`) — Official Google/Looker extension. Syntax highlighting,
  field completion, inline validation. Requires a live Looker connection for full
  validation; syntax highlighting works offline.
- **Python** (`ms-python.python`) — Required if you run `scripts/validate.py`.

---

## 2. Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # nothing installs until you uncomment items
```

When lkml or spectacles are approved by your security team, uncomment the relevant
lines in `requirements.txt` and re-run `pip install -r requirements.txt`.

---

## 3. BigQuery MCP Toolbox

Provides BigQuery schema exploration and query tools directly in your IDE.

**Install the binary:**

1. Go to https://github.com/googleapis/mcp-toolbox/releases
2. Download the binary for your platform
3. Place it at `.tools/toolbox` (relative to this repo root)
4. Make it executable: `chmod +x .tools/toolbox`

**Authenticate:**

```bash
gcloud auth application-default login
```

The MCP server in `.vscode/mcp.json` is pre-configured for project `gcs-automation-project`.
Change `BIGQUERY_PROJECT` in `.vscode/mcp.json` if using a different project.

---

## 4. Google Developer Knowledge MCP

Provides search over Google's official developer documentation (Firebase, Cloud, Android, Maps, etc.).

**Enable and get an API key:**

```bash
gcloud beta services mcp enable developerknowledge.googleapis.com --project=YOUR_PROJECT
```

Then create a restricted API key in [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

**Set the key:**

```bash
cp .env.example .env
# Edit .env and set GOOGLE_DEV_KNOWLEDGE_API_KEY=your-key
source .env
```

The MCP server reads `GOOGLE_DEV_KNOWLEDGE_API_KEY` from your environment via `${env:...}` in `.vscode/mcp.json`.

---

## What Each MCP Server Provides

| Server | Transport | Auth | What it does |
|---|---|---|---|
| `bigquery` | stdio (local binary) | ADC (`gcloud auth`) | List tables, run queries, explore schema |
| `google-developer-knowledge` | remote HTTP | API key | Search Google developer docs |

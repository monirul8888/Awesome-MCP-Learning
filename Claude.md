# MCP Server Setup Guide — FastMCP + Claude Desktop (Windows)

## Prerequisites

| Tool | Install Command | Notes |
|------|----------------|-------|
| Python 3.10+ | [python.org](https://python.org) | Ensure added to PATH |
| `uv` | `pip install uv` or [docs.astral.sh/uv](https://docs.astral.sh/uv) | Fast Python package manager |
| Claude Desktop | [claude.ai/download](https://claude.ai/download) | Must be opened at least once |

---

## Project Structure

```
D:\Python\MCP\
└── YourProject\
    ├── main.py          # Your MCP server code
    ├── pyproject.toml   # Auto-created by uv
    └── .venv\           # Auto-created by uv
```

---

## Step 1 — Create Project

```powershell
mkdir D:\Python\MCP\YourProject
cd D:\Python\MCP\YourProject
uv init
uv add fastmcp
```

---

## Step 2 — Write Your MCP Server (`main.py`)

```python
from fastmcp import FastMCP
import random

mcp = FastMCP("Your Server Name")

@mcp.tool
def roll_dice(n_dice: int = 1) -> list[int]:
    """Roll n_dice 6-sided dice and return the results"""
    return [random.randint(1, 6) for _ in range(n_dice)]

@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

### Key rules for tools:
- Decorate with `@mcp.tool`
- Always include a **docstring** — Claude uses it to understand the tool
- Use **type hints** on all parameters and return values
- Keep functions focused and single-purpose

---

## Step 3 — Test the Server Locally

```powershell
uv run main.py
```

You should see the FastMCP banner and:
```
INFO  Starting MCP server '...' with transport 'stdio'
```

Press `Ctrl+C` to stop. If this works, the server is ready.

---

## Step 4 — Install into Claude Desktop

```powershell
uv run fastmcp install claude-desktop main.py
```

Expected output:
```
Successfully installed 'Your Server Name' in Claude Desktop
```

### If you get `Claude Desktop config directory not found`:
Claude Desktop hasn't been opened yet. Open it, sign in, close it, then retry.

### If you get `Failed to install server: Expecting value: line 1 column 1 (char 0)`:
The config file is empty or has a BOM encoding issue. Fix with:

```powershell
# Write a clean config manually (no BOM)
$config = '{"mcpServers":{}}'
[System.IO.File]::WriteAllText(
    "$env:APPDATA\Claude\claude_desktop_config.json",
    $config
)
```

Then retry `uv run fastmcp install claude-desktop main.py`.

---

## Step 5 — Restart Claude Desktop

1. Right-click the Claude icon in the **system tray**
2. Click **Quit**
3. Reopen Claude Desktop
4. Go to **Settings (⚙) → Developer**
5. Your server should appear with a ✅ green indicator

---

## Manual Config (Alternative to `fastmcp install`)

Config file location:
```
C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json
```

Write it without BOM using PowerShell:

```powershell
$config = @"
{
  "mcpServers": {
    "my-server": {
      "command": "C:\\Users\\<YourUsername>\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "D:\\Python\\MCP\\YourProject",
        "run",
        "main.py"
      ]
    }
  }
}
"@

[System.IO.File]::WriteAllText(
    "$env:APPDATA\Claude\claude_desktop_config.json",
    $config
)
```

> ⚠️ Always use `[System.IO.File]::WriteAllText()` — PowerShell's `Out-File` adds a BOM that breaks JSON parsing.

---

## Adding Multiple Servers

```json
{
  "mcpServers": {
    "basic": {
      "command": "C:\\Users\\SVA_Delta\\.local\\bin\\uv.exe",
      "args": ["--directory", "D:\\Python\\MCP\\Basic", "run", "main.py"]
    },
    "another-server": {
      "command": "C:\\Users\\SVA_Delta\\.local\\bin\\uv.exe",
      "args": ["--directory", "D:\\Python\\MCP\\AnotherProject", "run", "main.py"]
    }
  }
}
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Claude Desktop config directory not found` | Claude Desktop never opened | Open Claude Desktop once, sign in, close it |
| `Expecting value: line 1 column 1 (char 0)` | Config file is empty or has BOM | Use `WriteAllText()` to rewrite clean JSON |
| Server shows red ❌ in Developer settings | `uv.exe` path wrong or `main.py` has errors | Run `uv run main.py` manually to see errors |
| Tools don't appear in Claude | Server not restarted after install | Fully quit Claude Desktop via system tray, reopen |
| `uv` not found | uv not installed or not in PATH | Run `pip install uv` or check [astral.sh/uv](https://docs.astral.sh/uv) |

---

## Quick Reference

```powershell
# Find uv path
where.exe uv

# Test server runs
uv run main.py

# Install to Claude Desktop
uv run fastmcp install claude-desktop main.py

# Check config file
cat "$env:APPDATA\Claude\claude_desktop_config.json"

# Open config folder in Explorer
explorer "$env:APPDATA\Claude"
```

---

## FastMCP Tool Types

```python
# Basic tool
@mcp.tool
def my_tool(param: str) -> str:
    """Description Claude will see"""
    return result

# Tool with optional params
@mcp.tool
def greet(name: str, formal: bool = False) -> str:
    """Greet a person"""
    return f"Good day, {name}." if formal else f"Hey {name}!"

# Tool returning structured data
@mcp.tool
def get_stats(numbers: list[float]) -> dict:
    """Return basic statistics for a list of numbers"""
    return {
        "min": min(numbers),
        "max": max(numbers),
        "avg": sum(numbers) / len(numbers)
    }
```

---

*FastMCP docs: [gofastmcp.com](https://gofastmcp.com) | Claude Desktop: [claude.ai/download](https://claude.ai/download)*

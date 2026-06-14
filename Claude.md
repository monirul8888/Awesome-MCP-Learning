# FastMCP + Claude Desktop Setup Guide (Windows)

Complete setup guide for creating and connecting FastMCP servers with Claude Desktop on Windows.

---

# 1. Requirements

Install these first:

| Tool           | Download / Install                                      |
| -------------- | ------------------------------------------------------- |
| Python 3.10+   | https://python.org                                      |
| uv             | https://docs.astral.sh/uv/getting-started/installation/ |
| Claude Desktop | https://claude.ai/download                              |

---

# 2. Install uv

### Option 1 — Recommended

Open PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart terminal.

Check installation:

```powershell
uv --version
```

Find uv path:

```powershell
where.exe uv
```

Example output:

```text
C:\Users\YourName\.local\bin\uv.exe
```

---

# 3. Create MCP Project

```powershell
mkdir D:\Python\MCP\Basic
cd D:\Python\MCP\Basic

uv init
uv venv
.venv\Scripts\activate

uv add fastmcp
```

---

# 4. Create `main.py`

Create `main.py`:

```python
from fastmcp import FastMCP
import random

mcp = FastMCP("Basic")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello"""
    return f"Hello {name}"

@mcp.tool()
def roll_dice(n_dice: int = 1) -> list[int]:
    """Roll dice"""
    return [random.randint(1, 6) for _ in range(n_dice)]

@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

---

# 5. Run MCP Server Locally

```powershell
uv run main.py
```

Expected output:

```text
INFO Starting MCP server 'Basic' with transport 'stdio'
```

Press:

```text
Ctrl + C
```

to stop.

---

# 6. Claude Desktop Setup

Install Claude Desktop:

https://claude.ai/download

IMPORTANT:

* Open Claude Desktop at least once
* Login
* Wait until chat UI fully loads
* Close Claude Desktop

---

# 7. Open Claude Config

PowerShell:

```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

If file does not exist, Notepad will create it.

---

# 8. Add MCP Server Config

Paste this:

```json
{
  "mcpServers": {
    "basic": {
      "command": "C:\\Users\\YOUR_USERNAME\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "D:\\Python\\MCP\\Basic",
        "run",
        "main.py"
      ]
    }
  }
}
```

IMPORTANT:

* Replace `YOUR_USERNAME`
* JSON paths MUST use double backslashes `\\`

---

# 9. Restart Claude Desktop

Completely close Claude Desktop:

* System tray → Right click Claude → Quit

Then reopen Claude Desktop.

---

# 10. Verify MCP Server

In Claude Desktop ask:

```text
What tools are available?
```

or

```text
Call the hello tool
```

If successful, Claude will detect your MCP tools.

---

# 11. Multiple MCP Servers

Example:

```json
{
  "mcpServers": {
    "basic": {
      "command": "C:\\Users\\YourName\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "D:\\Python\\MCP\\Basic",
        "run",
        "main.py"
      ]
    },

    "weather": {
      "command": "C:\\Users\\YourName\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "D:\\Python\\MCP\\Weather",
        "run",
        "main.py"
      ]
    }
  }
}
```

---

# 12. FastMCP CLI Commands

## Run Server

```powershell
uv run main.py
```

## Run via FastMCP

```powershell
uv run fastmcp run main.py
```

## Inspector UI

```powershell
uv run fastmcp dev inspector main.py
```

---

# 13. Troubleshooting

## Error:

```text
Unknown command "main.py"
```

Use:

```powershell
uv run fastmcp dev inspector main.py
```

NOT:

```powershell
uv run fastmcp dev main.py
```

---

## Error:

```text
Claude Desktop config directory not found
```

Fix:

* Open Claude Desktop once
* Login
* Close Claude
* Retry

---

## Error:

```text
Expecting value: line 1 column 1 (char 0)
```

Config file broken or empty.

Fix:

```powershell
$config = '{"mcpServers":{}}'

[System.IO.File]::WriteAllText(
"$env:APPDATA\Claude\claude_desktop_config.json",
$config
)
```

---

## Error:

```text
uv not found
```

Install uv again:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Error:

```text
Server shows red X
```

Usually:

* Wrong uv.exe path
* Broken JSON
* Python error in main.py

Test manually:

```powershell
uv run main.py
```

---

# 14. Useful Commands

## Find uv path

```powershell
where.exe uv
```

---

## Open Claude config folder

```powershell
explorer "$env:APPDATA\Claude"
```

---

## View config file

```powershell
cat "$env:APPDATA\Claude\claude_desktop_config.json"
```

---

## Activate virtual environment

```powershell
.venv\Scripts\activate
```

---

## Deactivate virtual environment

```powershell
deactivate
```

---

# 15. Recommended Project Structure

```text
D:\Python\MCP\
│
├── Basic\
│   ├── main.py
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .venv\
│
├── Weather\
│   ├── main.py
│   └── .venv\
```

---

# 16. Best Practices

* Always use type hints
* Always add docstrings
* Keep tools small and focused
* Test with `uv run main.py` before Claude integration
* Use separate folders for separate MCP servers

---

# 17. Example Tool Patterns

## Simple Tool

```python
@mcp.tool()
def greet(name: str) -> str:
    """Greet a user"""
    return f"Hello {name}"
```

---

## Optional Parameters

```python
@mcp.tool()
def greet(name: str, formal: bool = False) -> str:
    """Greeting tool"""
    return f"Good day {name}" if formal else f"Hey {name}"
```

---

## Structured Output

```python
@mcp.tool()
def stats(numbers: list[float]) -> dict:
    """Return statistics"""
    return {
        "min": min(numbers),
        "max": max(numbers),
        "avg": sum(numbers)/len(numbers)
    }
```

---

# References

* FastMCP: https://gofastmcp.com
* uv Docs: https://docs.astral.sh/uv/
* Claude Desktop: https://claude.ai/download

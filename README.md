# Awesome MCP Learning

A beginner-friendly repository for learning the **Model Context Protocol (MCP)** using **FastMCP** and **uv**.

## 🚀 Environment

```text
FastMCP version: 3.4.2
MCP version: 1.27.2
Python version: 3.14.3
Platform: Windows 11
```

---

# 📦 Prerequisites

* Python 3.14+
* Git
* uv
* FastMCP

Install uv:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```bash
uv --version
```

---

# 🛠️ Project Setup

## Clone the Repository

```bash
git clone https://github.com/monirul8888/Awesome-MCP-Learning.git
cd Awesome-MCP-Learning
```

## Create a Virtual Environment

```bash
uv venv
```

Activate the environment:

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
uv sync
```

This installs all dependencies defined in `pyproject.toml` and locked in `uv.lock`.

---

# ▶️ Running the MCP Server

Run the server:

```bash
uv run python main.py
```

Or:

```bash
fastmcp run main.py
```

---

# 📁 Project Structure

```text
Awesome-MCP-Learning/
│
├── main.py
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── README.md
├── .gitignore
└── .python-version
```

---

# 🔄 Development Workflow

Install a new package:

```bash
uv add package-name
```

Example:

```bash
uv add fastmcp
```

Remove a package:

```bash
uv remove package-name
```

Update dependencies:

```bash
uv lock
uv sync
```

Run Python scripts:

```bash
uv run python main.py
```

---

# 🌿 Git Workflow

Initialize Git:

```bash
git init
```

Stage files:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Initial MCP Project Server"
```

Add GitHub remote:

```bash
git remote add origin https://github.com/monirul8888/Awesome-MCP-Learning.git
```

Rename branch to `main`:

```bash
git branch -M main
```

Push to GitHub:

```bash
git push -u origin main
```

---

# 📚 Learning Goals

* Understand MCP fundamentals
* Build MCP servers with FastMCP
* Manage dependencies using uv
* Work with Git and GitHub
* Create reusable MCP tools and resources

---

# 👨‍💻 Author

**Monirul Islam**

GitHub: https://github.com/monirul8888

---

# 📄 License

This project is licensed under the MIT License.

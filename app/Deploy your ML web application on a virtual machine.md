# Cloud Computing — Practical Lab

## Deploy a Machine Learning web application on a Virtual Machine

---

### Who is this for?

Absolute beginners. You are not expected to know Linux or Python.
Just read each step, understand **why** you do it, then type the commands.

> Please feel free to ask any question!

### What are you going to build?

A **"price prediction" web application**. It is a Python program that loads a
trained Machine Learning model (XGBoost) and shows a web form in your browser.
You fill the form, you click a button, the model answers with a predicted
insurance price.

The web interface is built with **Streamlit**: a Python library that turns a
simple Python script into a web page, with no HTML/CSS/JavaScript needed.

### Where do you work?

Everything below is typed in a **terminal** (a black window where you type
commands), inside your Cloud/Local Virtual Machine (VM) — a computer that runs
in a datacenter / on your PC and that you reach through SSH.

---

## Vocabulary you need

*Read this once, it will save you a lot of time.*

| Term | What it means |
| --- | --- |
| **Terminal / shell** | The window where you type commands. |
| **Package manager** | A tool that downloads and installs software for you (`apt` for the Linux system, `uv` for Python libraries). |
| **Repository (repo)** | A folder of source code hosted online, here on GitHub. |
| **Git** | The tool used to download / update that source code. |
| **Dependency** | An external library your program needs to run (pandas, streamlit, xgboost…). |
| **`pyproject.toml`** | The file that **lists** all the dependencies of the project, with their versions. It is the recipe. |
| **Virtual environment (venv)** | A private, isolated Python installation for **one** project. It avoids breaking the system Python and avoids version conflicts between projects. |
| **uv** | A modern, very fast Python tool. It can install Python itself, create virtual environments, and install dependencies. It replaces `pip` + `venv` + `poetry`. |
| **Port** | A "door" number on a machine. A web app listens on a port; Streamlit uses **8501** by default. |

---

## Rules of the lab

1. Do the steps **in order**. Each one depends on the previous one.
2. **Read the output** of every command. Errors are written in plain English.
3. If a command fails, do **not** jump to the next step: fix it first.
4. **Never** run the application outside the virtual environment.

---

## Step 1 — Install the Operating System dependencies

> **Goal:** get the base tools your machine needs before anything Python-related.
> **Install:** `curl` (to download files from the internet), `git` (to get the
> code), and the Python basics (`python3`, `python3-venv`).
> **Why:** a fresh VM is almost empty. Nothing is installed by default.

**Checklist**

- [ ] Refresh the list of available packages
- [ ] Install: `curl`, `git`, `python3`, `python3-venv`
- [ ] Verify the installation (`git --version`, `python3 --version`)

💡 *Hint:* on Debian/Ubuntu the system package manager is `apt`, and installing
system software requires administrator rights (`sudo`).

---

## Step 2 — Get the application source code from GitHub

> **Goal:** download the project to your VM.
> **Repo:** <https://github.com/AbdKenn/cloud-course>

**Checklist**

- [ ] Clone the repository
- [ ] List the files you just downloaded, and find the `app` folder
- [ ] Enter the `app` folder (this is your working directory for the lab)

✅ **Expected:** inside `app` you must see a file named `pyproject.toml` and a
folder named `src`. If you do not see them, you are in the wrong directory.

### 2.bis — Updating the code later *(not asked in the exam)*

If the teacher pushes a correction to GitHub, you do not clone again: you
**pull** the new commits into the folder you already have.

---

## Step 3 — Install uv and create the virtual environment

> **Goal:** have an isolated Python environment, ready to receive the project
> dependencies.
> **Why a specific version:** the project declares
> `requires-python = ">=3.11,<3.12"` in `pyproject.toml`. Another version will
> be refused.

**Checklist**

- [ ] Install `uv` (official installer, downloaded with `curl`)
- [ ] Make `uv` available in your terminal (check with `uv --version`)
- [ ] Ask `uv` to install Python (you do **not** need `apt` for this)
- [ ] Create a virtual environment with `uv`
- [ ] Activate the virtual environment
- [ ] Verify you are inside it: your prompt starts with `(.venv)` and
      `python --version` answers `3.x.x` (depending on your version)

⚠️ **Important:** activation is valid only for the **current** terminal session.
If you close the terminal or reconnect by SSH, activate again.

---

## Step 4 — Install the Python dependencies with uv

> **Goal:** install every library listed in `pyproject.toml`, in one command.
> **Why:** the application imports streamlit, pandas, xgboost, loguru,
> scikit-learn… Without them, Python stops with `ModuleNotFoundError`.

**Checklist**

- [ ] From the `app` folder, install the dependencies declared in
      `pyproject.toml` using `uv`
- [ ] Wait until the end (`uv` prints the list of installed packages)
- [ ] Verify that `streamlit` is installed and runnable

The dependencies of this project — *for information only, do not type them one
by one, `uv` reads them from `pyproject.toml`*:

```
pandas, loguru==0.6.0, scikit-learn, xgboost==1.6.1, setuptools<81,
streamlit==1.32.2, altair==4.*, flask>=3.0.0,<4, pytest>=7.4.3,<8,
gunicorn>=21.2.0,<22, google-cloud-bigquery>=3.14.1,<4
```

❗ If you get an error about the Python version: your venv was not created with
the correct Python version. Delete it and redo **Step 3**.

---

## Step 5 — Locate and run `main.py` with Streamlit

> **Goal:** start the web application.

**Checklist**

- [ ] Find the file named `main.py` inside the project
- [ ] Move into the folder that **contains** `main.py`
      *(important: the script loads images and the model with relative paths —
      if you run it from elsewhere, it will not find them)*
- [ ] Run `main.py` with Streamlit
- [ ] Read the output: Streamlit prints a **Local URL** and a **Network URL**

💡 *Note:* on a Cloud VM, Streamlit must listen on **all** network interfaces,
not only on the machine itself, otherwise nobody can reach it from outside.
Keep that in mind when you build your command.

---

## Step 6 — Open the application in a browser and make a prediction

> **Goal:** prove the deployment works end to end.

**Case A — your machine has a graphical interface**

- [ ] Open a browser and go to <http://localhost:8501>

**Case B — the app runs on a remote Cloud VM (no graphical interface)**

- [ ] Open `http://<EXTERNAL_IP_OF_YOUR_VM>:<PORT>`

**Then**

- [ ] In the left sidebar, switch the page from **Home** to **Prediction**
- [ ] Fill in every field of the form — only dates are required
      *(dates must use the format `dd/mm/YYYY`, for example `01/01/1990`)*
- [ ] Click the prediction button
- [ ] A predicted price must be displayed, with **no error** on the page and
      **no traceback** in the terminal

🎉 **Done.** You have deployed a Machine Learning application on a Cloud/Local VM.

---

## Step 7 *(bonus)* — Stop and clean up

- [ ] Stop the application in the terminal (`Ctrl + C`)
- [ ] Leave the virtual environment (`deactivate`)
- [ ] If you worked on a Cloud VM: **stop or delete** the VM so it stops costing
      money

---

## Troubleshooting — the 6 errors you will probably meet

| Error message | What it means / how to fix it |
| --- | --- |
| `command not found: uv` | uv is installed but your terminal does not know where it is. Reload your shell configuration, or open a new terminal. |
| `ModuleNotFoundError: No module named 'streamlit'` | The virtual environment is not activated, or Step 4 failed. |
| `No solution found ... requires Python >=3.11,<3.12` | Your venv uses the wrong Python version. Redo Step 3. |
| `FileNotFoundError: ci.jpg` / model file not found | You launched Streamlit from the wrong directory. Move into the folder that contains `main.py`. |
| `Port 8501 is already in use` | An older Streamlit is still running. Stop it, or use another port. |
| The page never loads from outside the VM | Either Streamlit listens only on `localhost`, or the Cloud firewall blocks the port. Check both. |

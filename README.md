# Auto-Fix Python Script with Ollama Integration 🐍🤖

## Overview

This project automatically monitors a Python script for errors, sends detected errors to Ollama's `deepseek-r1:32b` model for fixes, and updates the script with the corrected code. Say goodbye to endless debugging sessions!

## Features

- **Error Monitoring**: Continuously runs your target script and captures errors.
- **Automated Fixes**: Sends errors to Ollama for intelligent fixes.
- **Seamless Updates**: Replaces the faulty script with the corrected version.
- **Backup Creation**: Keeps a backup of your original script before making changes.

## Installation

1. **Set Up Virtual Environment**
    
    - **Working with python3.11**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install Dependencies**

    ```bash
    pip install ollama
    pip install open-webui  # Optional
    ```

3. **Run DeepSeek Model**

    ```bash
    ollama run deepseek-r1:32b
    ```

## Usage

1. **Prepare Your Target Script**

    Ensure your `target_script.py` is in the project directory and contains some errors for demonstration.

2. **Run the Monitoring Script**

    ```bash
    python3 monitoring_script.py
    ```

    **What Happens:**
    - The script executes `target_script.py`.
    - If an error occurs, it's sent to Ollama for fixing.
    - The script updates `target_script.py` with the fixed code.
    - A backup is saved as `target_script.py.backup`.
    - The target script is re-run to verify the fix.

## Example

### Faulty `target_script.py`

```python
# target_script.py

def calculate_factoriaL(n):
    return n * calculate_factoriaL(n - 1)

print(calculate_factrial(5))  # Typo alert!

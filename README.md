# Auto-Fix Python Script with Ollama Integration 🐍🤖

## Overview

Right now this project can automatically detect python files in a directory, run them, identify errors in the output and update the files with the corrected code. 

Sends detected errors to Ollama's `deepseek-r1:32b` model for fixes, and updates the file with the corrected code. It runs the script again after file update to make sure there aren't additional errors.

Eventually I would like this to be framework agnostic and aware so it can troubleshoot and build for you on the fly. 

## Features

- **Error Monitoring**: Continuously runs your target script and captures errors.
- **Automated Fixes**: Sends errors to Ollama for intelligent fixes.
- **Seamless Updates**: Replaces the faulty script with the corrected version.
- **Backup Creation**: Keeps a backup of your original script before making changes.

## TODO

- **Framework awareness**: put this in your project and let it fix errors on the fly.
- **Add javascript support**: support for js files and frameworks.
- **Project Scaffolding**: take in natural language and scaffold out file structure with complete code.

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
    ```

3. **Run DeepSeek Model**

    ```bash
    ollama run deepseek-r1:32b
    ```

## Usage

1. **Target Scripts**

    The scripts in the project directory contains some errors for demonstration. 

2. **Run the Monitoring Script**

    ```bash
    python3 monitoring_script.py
    ```

    **What Happens:**
    - The script executes each .py file
    - If an error occurs, it's sent to Ollama for fixing.
    - The script updates the .py file with the fixed code.
    - A backup is saved as `example.py.backup`.
    - The target script is re-run to verify the fix.


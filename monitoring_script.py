import subprocess
import sys
import time
import os
import re
import ollama
import glob
#from ollama import chat, ChatResponse

def process_script(script_path):
    """
    Processes the given script by running it, checking for errors, and attempting to fix them.
    Recursively calls itself until the script runs successfully or cannot be fixed.
    """
    print(f"\nRunning '{script_path}'...")
    stdout, stderr = run_target_script(script_path)

    # Display the standard output
    if stdout:
        print("Standard Output:")
        print(stdout)

    # Check for errors in stderr
    if stderr:
        print("Standard Error:")
        print(stderr)
        print("Sending error to Ollama for fixing...")

        # Read the current content of the script
        try:
            with open(script_path, 'r') as file:
                current_code = file.read()
        except Exception as e:
            print(f"Failed to read the script: {e}")
            return False

        # Get the fixed code from Ollama
        fixed_code = send_error_to_ollama(stderr, current_code)

        if fixed_code:
            # Update the script with the fixed code
            update_script(script_path, fixed_code)
            print("Script has been updated. Re-running the script...\n")
            time.sleep(2)  # Wait before re-running

            # Recursively call the function to re-run the updated script
            return process_script(script_path)
        else:
            print("Could not fix the error automatically. Moving to the next script.")
            return False
    else:
        # No errors, script ran successfully
        print(f"Script '{script_path}' executed successfully without errors.")
        return True



def run_target_script(script_path):
    """
    Runs the target Python script and captures its stdout and stderr.
    Prints the script name and whether it ran successfully or encountered an error.
    Returns the stdout and stderr as strings.
    """
    try:
        print(f"Running script: {script_path}...")
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=10  # Adjust the timeout as needed
        )

        # Check for errors in stderr
        if result.stderr:
            print(f"Script '{script_path}' encountered an error.")
        else:
            print(f"Script '{script_path}' ran successfully.")

        return result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        print(f"Script '{script_path}' timed out.")
        return "", "Error: Script execution timed out."

def extract_code_from_response(response):
    """
    Extract Python code from Ollama's response.

    Args:
        response: The raw response from Ollama

    Returns:
        Extracted Python code or None if no valid code found
    """
    try:
        # Skip thinking sections
        if '<think>' in response:
            response = response.split('</think>')[-1].strip()

        # Look for code blocks between triple backticks
        if "```python" in response:
            # Extract code between python code blocks
            start = response.find("```python") + 9
            end = response.find("```", start)
            if end != -1:
                return response[start:end].strip()
        elif "```" in response:
            # Extract code between generic code blocks
            start = response.find("```") + 3
            end = response.find("```", start)
            if end != -1:
                return response[start:end].strip()
        else:
            # If no code blocks, return the raw response
            # assuming it's directly code
            return response.strip()
    except Exception as e:
        print(f"Error extracting code from response: {e}")
        return None

def send_error_to_ollama(error_message, script_content):
    """
    Sends the error message and current script content to Ollama to get the fixed code.
    Returns the fixed code as a string or None if extraction fails.
    """
    prompt = f"""Fix this Python script that produced the following error:

    Error Output:
    {error_message}

    Standard Output:
    {script_content}

    Please provide only the complete fixed Python code the entire script without any explanations. Make sure to NOT include your output other than the code including everything between the think brackets <think></think>."""

    try:
        response = ollama.chat(model='deepseek-r1:32b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        # Extract the content from the response
        response_text = response.message.content.strip()
        print(f"Response text received:\n{response_text}\n")

        # Extract code using the helper function
        fixed_code = extract_code_from_response(response_text)

        if fixed_code:
            print("Code successfully extracted from Ollama's response.")
            return fixed_code
        else:
            print("Failed to extract code from Ollama's response.")
            print("Full response received:\n", response_text)
            return None
    except Exception as e:
        print(f"An error occurred while communicating with Ollama: {e}")
        return None

def update_script(script_path, new_content):
    """
    Updates the target script with the new content.
    """
    backup_path = f"{script_path}.backup"
    try:
        # Create a backup of the original script
        if not os.path.exists(backup_path):
            os.rename(script_path, backup_path)
            print(f"Backup created at '{backup_path}'.")
        else:
            print(f"Backup already exists at '{backup_path}'.")

        # Write the fixed code to the original script path
        with open(script_path, 'w') as file:
            file.write(new_content)
        print(f"Script '{script_path}' has been updated with the fixes.")
    except Exception as e:
        print(f"Failed to update the script: {e}")

def main():
    # Find all Python files in the current directory and subdirectories
    script_paths = []
    current_script = os.path.basename(__file__)

    # Define patterns to ignore
    ignore_patterns = ['__pycache__', '*.pyc', '*.pyo', '*.pyd', '.git']

    print("Scanning for Python files...")
    for py_file in glob.glob("**/*.py", recursive=True):
        # Skip files matching ignore patterns
        if any(pattern in py_file for pattern in ignore_patterns):
            continue

        # Skip the monitoring script itself and any backup files
        if py_file != current_script and not py_file.endswith('.backup'):
            # Convert path to absolute for consistent handling
            abs_path = os.path.abspath(py_file)
            script_paths.append(abs_path)

    if not script_paths:
        print("No Python files found to monitor.")
        sys.exit(1)

    # Group files by directory for better organization
    files_by_dir = {}
    for script in script_paths:
        dir_name = os.path.dirname(script) or "root"
        if dir_name not in files_by_dir:
            files_by_dir[dir_name] = []
        files_by_dir[dir_name].append(os.path.basename(script))

    # Print discovered files grouped by directory
    print("\nDiscovered Python files to monitor:")
    for dir_name, files in files_by_dir.items():
        print(f"\nIn {dir_name}:")
        for file in sorted(files):
            print(f"  - {file}")
    print(f"\nTotal files to monitor: {len(script_paths)}\n")

    # Main loop to process each script in script_paths
    for script_path in script_paths:
        success = process_script(script_path)
        if not success:
            print(f"Script '{script_path}' could not be fixed. Moving to the next script.")

    print("\nProcessing completed!")


if __name__ == "__main__":
    main()

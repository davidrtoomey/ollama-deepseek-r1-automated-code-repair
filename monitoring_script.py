import subprocess
import sys
import time
import os
import re
from ollama import chat, ChatResponse

def run_target_script(script_path):
    """
    Runs the target Python script and captures its stdout and stderr.
    Returns the stdout and stderr as strings.
    """
    try:
        # Execute the target script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=10  # Adjust the timeout as needed
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Script execution timed out."

def extract_code_from_response(response_text):
    """
    Extracts Python code blocks from the response text.
    Returns the concatenated code as a single string.
    """
    code_blocks = re.findall(r"```python(.*?)```", response_text, re.DOTALL)
    if not code_blocks:
        # Try without specifying python (in case Ollama doesn't tag it)
        code_blocks = re.findall(r"```(.*?)```", response_text, re.DOTALL)
    if code_blocks:
        # Concatenate all extracted code blocks
        return "\n".join(block.strip() for block in code_blocks)
    else:
        return None

def send_error_to_ollama(error_message, script_content):
    """
    Sends the error message and current script content to Ollama to get the fixed code.
    Returns the fixed code as a string or None if extraction fails.
    """
    prompt = (
        "I encountered the following error in my Python script:\n\n"
        f"{error_message}\n\n"
        "Here is the current code:\n\n"
        f"{script_content}\n\n"
        "Please fix the code to resolve the above error. "
        "Provide only the corrected Python code without any additional explanations."
    )

    try:
        response: ChatResponse = chat(
            model='deepseek-r1:32b',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ]
        )
        # Extract the content from the response
        response_text = response.message.content.strip()
        fixed_code = extract_code_from_response(response_text)

        if fixed_code:
            return fixed_code
        else:
            print("Failed to extract code from Ollama's response.")
            print("Full response received:")
            print(response_text)
            return None
    except Exception as e:
        print(f"Failed to communicate with Ollama: {e}")
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
    target_script = 'target_script.py'  # Replace with your target script path

    while True:
        print(f"\nRunning '{target_script}'...")
        stdout, stderr = run_target_script(target_script)

        # Display the standard output
        if stdout:
            print("Standard Output:")
            print(stdout)

        # If there is an error, attempt to fix it
        if stderr:
            print("Standard Error:")
            print(stderr)
            print("Sending error to Ollama for fixing...")

            # Read the current content of the script
            try:
                with open(target_script, 'r') as file:
                    current_code = file.read()
            except Exception as e:
                print(f"Failed to read the script: {e}")
                break

            # Get the fixed code from Ollama
            fixed_code = send_error_to_ollama(stderr, current_code)

            if fixed_code:
                # Update the script with the fixed code
                update_script(target_script, fixed_code)
                print("Waiting before re-running the script...\n")
                time.sleep(2)  # Wait before re-running
            else:
                print("Could not fix the error automatically.")
                break
        else:
            print("Script executed successfully without errors.")
            break

        # Optional: Add a condition to prevent infinite loops
        # For example, limit the number of retries
        # This example runs indefinitely until success or a failure in fixing
        time.sleep(1)  # Short pause before next iteration

if __name__ == "__main__":
    main()

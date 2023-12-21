import psutil, os, signal, subprocess, platform, json, pyautogui, time

def get_pid_by_name(partial_name):
    words = partial_name.split()
    
    for word in words:
        found_processes = []
        for process in psutil.process_iter(['pid', 'name']):
            if word.lower() in process.info['name'].lower():
                found_processes.append(process)
        
        if len(found_processes) == 1:
            return found_processes[0].info['pid']
        elif len(found_processes) > 1:
            print(f"Multiple processes found for '{word}'. Please provide more details.")
            return None
    
    print(f"No matching process found for the given name.")
    return None

def terminate_process(pid):
    try:
        # Send the SIGTERM signal
        os.kill(int(pid), signal.SIGTERM)
        print(f"Process with PID {pid} terminated successfully.")
        
        # Check if the process is still alive after SIGTERM
        time.sleep(1)  # Give some time for the process to respond to SIGTERM
        try:
            os.kill(int(pid), 0)  # Check if the process is still alive
            print(f"Process with PID {pid} is still alive. Sending SIGKILL.")
            os.kill(int(pid), signal.SIGKILL)  # Send the SIGKILL signal
            print(f"Process with PID {pid} forcefully terminated.")
        except ProcessLookupError:
            print(f"Process with PID {pid} not found after SIGTERM.")
    except ProcessLookupError:
        print(f"Error: Process with PID {pid} not found.")
        exit(-1)
    except PermissionError:
        print(f"Error: Permission denied to terminate process with PID {pid}.")
        exit(-2)
    except:
        print(f"Error: Process {pid} failed to terminate. Unknown Error.")
        exit(-3)

def force_terminate_process():
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')

def save_data(data):
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the directory and file path relative to the script's directory
    directory_path = os.path.join(script_directory, '.temp')
    file_path = os.path.join(directory_path, "application.txt")

    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Save data to the file
        with open(file_path, 'w') as file:
            file.write(str(data))

        print(f'Data saved to {file_path}')
    except Exception as e:
        print(f'Error: {e}')

def load_data():
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the directory and file path relative to the script's directory
    directory_path = os.path.join(script_directory, '.temp')
    file_path = os.path.join(directory_path, "application.txt")

    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Load data from the file
            with open(file_path, 'r') as file:
                loaded_data = file.read()

            # Delete the file
            os.remove(file_path)

            print(f'Data loaded from and file deleted: {file_path}')
            return loaded_data
        else:
            print(f'File not found: {file_path}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None
    
def get_sunshine_apps():
    program_name = "Sunshine"
    system = platform.system().lower()
    sunshine_path = None

    if system == 'linux':
        # Check if installed via Flatpak
        flatpak_info = subprocess.run(['flatpak', 'list', '--app'], capture_output=True, text=True)
        if flatpak_info.returncode == 0:
            lines = flatpak_info.stdout.strip().split('\n')
            for line in lines:
                if program_name in line:
                    # Extract the installation directory from the line
                    flatpak_name = line.split()[1]
                    try:
                        # Run the 'flatpak --installations' command and capture the output
                        result = subprocess.run(["flatpak", "--installations"], capture_output=True, text=True, check=True)
                        flatpak_dir = result.stdout.strip()
                    except subprocess.CalledProcessError as e:
                        print(f"Error: {e}")

                    if os.path.exists(os.path.expanduser("~/.local/share/flatpak/app/" + flatpak_name + "/x86_64/stable/active/files/share/sunshine")):
                        sunshine_path = os.path.expanduser("~/.local/share/flatpak/app/" + flatpak_name + "/x86_64/stable/active/files/share/sunshine")
                    elif os.path.exists(flatpak_dir + "/" + flatpak_name + "/x86_64/stable/active/files/share/sunshine"):
                        sunshine_path = flatpak_dir + "/" + flatpak_name + "/x86_64/stable/active/files/share/sunshine"

        # Check if installed via which command
        which_info = subprocess.run(['which', program_name], capture_output=True, text=True)
        if which_info.returncode == 0:
            return os.path.dirname(which_info.stdout.strip())

    elif system == 'windows' and not sunshine_path:
        # Check if installed via executable (exe)
        # You might need to customize this based on the specific behavior of the installer
        # For example, Inno Setup installers usually have /D= parameter for specifying the installation directory
        # Modify the command accordingly for other installer types
        exe_info = subprocess.run(['where', program_name], capture_output=True, text=True)
        if exe_info.returncode == 0:
            sunshine_path = os.path.dirname(exe_info.stdout.strip())

    # Open application json file
    try:
        with open(sunshine_path + "/apps.json", 'r') as json_file:
            data = json.load(json_file)
            return data
    except:
        return None
import subprocess
import webbrowser
import time
import os
import platform

def run_terminal_commands():
    # Define the commands to run
    
    if platform.system() == 'Darwin':  # macOS
        commands = [
            'python3 -m http.server 8000',  # Command to run HTTP server
            'python3 app.py'                # Command to run app
        ]
    elif platform.system() == 'Windows':  # Windows
         commands = [
            'python -m http.server 8000',  # Command to run HTTP server
            'python app.py'                # Command to run app
        ]
    elif platform.system() == 'Linux':  # Linux
         commands = [
            'python3 -m http.server 8000',  # Command to run HTTP server
            'python3 app.py'                # Command to run app
        ]
    # Open a terminal and run the first command
    if platform.system() == 'Darwin':  # macOS
        subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "{commands[0]}"'])
    elif platform.system() == 'Windows':  # Windows
        subprocess.Popen(['start', 'cmd', '/k', commands[0]], shell=True)
    elif platform.system() == 'Linux':  # Linux
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', commands[0]])

    # Wait a bit to ensure the server starts
    time.sleep(2)

    # Open another terminal and run the second command
    if platform.system() == 'Darwin':  # macOS
        subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "{commands[1]}"'])
    elif platform.system() == 'Windows':  # Windows
        subprocess.Popen(['start', 'cmd', '/k', commands[1]], shell=True)
    elif platform.system() == 'Linux':  # Linux
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', commands[1]])

    # Wait a bit to ensure the app starts
    time.sleep(5)

def open_firefox():
    # Define the URL to open
    url = 'http://127.0.0.1:5000/'

    # Check if Firefox is already open
    if platform.system() == 'Darwin':  # macOS
        subprocess.Popen(['osascript', '-e', f'tell application "Firefox" to open location "{url}"'])
    elif platform.system() == 'Windows':  # Windows
        webbrowser.get('firefox').open(url)
    elif platform.system() == 'Linux':  # Linux
        subprocess.Popen(['firefox', url])

if __name__ == '__main__':
    run_terminal_commands()
    #open_firefox()

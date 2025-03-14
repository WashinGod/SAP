import platform
import socket
import subprocess
import psutil
import os
import sys
from pystyle import Colors, Colorate, Center

def list_processes():
    print(f"{'PID':<10} {'Name':<25} {'Status':<15}")
    print("="*50)
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            print(f"{proc.info['pid']:<10} {proc.info['name']:<25} {proc.info['status']:<15}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait()
        print(f"Process {pid} terminated successfully.")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print(f"Failed to terminate process {pid}.")

def search_process_by_name(name):
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        if name.lower() in proc.info['name'].lower():
            print(f"Found: {proc.info['pid']} - {proc.info['name']}")
            found = True
    if not found:
        print("No process found with that name.")

def get_system_info():
    info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Architecture": platform.architecture(),
        "CPU Cores": psutil.cpu_count(logical=True),
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "Disk Usage": f"{round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB",
        "Users": [user.name for user in psutil.users()],
        "Network Interfaces": psutil.net_if_addrs(),
        "Running Processes": [proc.info for proc in psutil.process_iter(attrs=['pid', 'name', 'username'])],
        "Environment Variables": dict(os.environ),
        "System Uptime": f"{round(psutil.boot_time())} seconds since boot",
        "Python Version": platform.python_version(),
        "Installed Packages": subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8').splitlines()
    }
    return info

def print_system_info(info):
    for key, value in info.items():
        print(f"{key}: {value}")

banner = """

            ,-.----.    
  .--.--.   \    /  \   
 /  /    '. |   :    \  
|  :  /`. / |   |  .\ : 
;  |  |--`  .   :  |: | 
|  :  ;_    |   |   \ : 
 \  \    `. |   : .   / 
  `----.   \;   | |`-'  
  __ \  \  ||   | ;     
 /  /`--'  /:   ' |     
'--'.     / :   : :     
  `--'---'  |   | :     
            `---'.|     
              `---` 
              
    ==============================
      ➤ [1] list all proccess
      ➤ [2] kill proccess by PID
      ➤ [3] search proccess by name
      ➤ [4] system info
      ➤ [5] coders
      ➤ [6] exit
    ==============================                    
"""
print(Colorate.Vertical(Colors.blue_to_red, Center.XCenter(banner)))

if __name__ == "__main__":
    while True:
    
        choice = input(Colorate.Horizontal(Colors.green_to_blue, "[!] Choose : "))

        if choice == '1':
            list_processes()
        elif choice == '2':
            name = input(Colorate.Horizontal(Colors.green_to_blue, "[!] Enter PID to kill: "))
            kill_process(pid)
        elif choice == '3':
            name = input(Colorate.Horizontal(Colors.green_to_blue, "[!] Enter process name to search: "))
            search_process_by_name(name)
        elif choice == '4':
            system_info = get_system_info()
            print_system_info(system_info)
        elif choice == '5':
            print(Colorate.Horizontal(Colors.green_to_black, f"[!] Coders:\nhareoku,fantom\nTG - hareoku.t.me,\n"))
        elif choice == '6':
            break
        else:
            print("Invalid option. Please try again.")


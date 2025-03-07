
import psutil
import os

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

print("""
          _____                    _____                    _____          
         /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\    \        
       /::::\    \              /::::\    \              /::::\    \       
      /::::::\    \            /::::::\    \            /::::::\    \      
     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \     
    /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \    
    \:::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \   
  ___\:::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \  
 /\   \:::\   \:::\    \  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\ 
/::\   \:::\   \:::\____\/:::/  \:::\   \:::\____\/:::/  \:::\   \:::|    |
\:::\   \:::\   \::/    /\::/    \:::\  /:::/    /\::/    \:::\  /:::|____|
 \:::\   \:::\   \/____/  \/____/ \:::\/:::/    /  \/_____/\:::\/:::/    / 
  \:::\   \:::\    \               \::::::/    /            \::::::/    /  
   \:::\   \:::\____\               \::::/    /              \::::/    /   
    \:::\  /:::/    /               /:::/    /                \::/____/    
     \:::\/:::/    /               /:::/    /                  ~~          
      \::::::/    /               /:::/    /                               
       \::::/    /               /:::/    /                                
        \::/    /                \::/    /                                 
         \/____/                  \/____/                                  
                                                                           
   """)

if __name__ == "__main__":
    while True:
        print("\n1. List all processes")
        print("2. Kill a process by PID")
        print("3. Search process by name")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            list_processes()
        elif choice == '2':
            pid = int(input("Enter PID to kill: "))
            kill_process(pid)
        elif choice == '3':
            name = input("Enter process name to search: ")
            search_process_by_name(name)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")


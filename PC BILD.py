
import sys
import psutil
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox, QLineEdit

class ProcessViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Procces Bild 1.0Beta")
        self.setGeometry(100, 100, 600, 500)
        
        self.layout = QVBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by process name...")
        self.layout.addWidget(self.search_input)
        
        self.process_list = QListWidget()
        self.layout.addWidget(self.process_list)
        
        self.refresh_button = QPushButton("Refresh Processes")
        self.refresh_button.clicked.connect(self.refresh_processes)
        self.layout.addWidget(self.refresh_button)
        
        self.terminate_button = QPushButton("Terminate Process")
        self.terminate_button.clicked.connect(self.terminate_process)
        self.layout.addWidget(self.terminate_button)
        
        self.system_info_button = QPushButton("Show Full System Info")
        self.system_info_button.clicked.connect(self.show_full_system_info)
        self.layout.addWidget(self.system_info_button)
        
        self.message_button = QPushButton("Channel Telegram")
        self.message_button.clicked.connect(self.show_message)
        self.layout.addWidget(self.message_button)
        
        self.setLayout(self.layout)
        self.refresh_processes()

    def refresh_processes(self):
        self.process_list.clear()
        search_term = self.search_input.text().lower()
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            if search_term in proc.info['name'].lower():
                self.process_list.addItem(f"{proc.info['pid']} - {proc.info['name']} - {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB - CPU: {proc.info['cpu_percent']}%")

    def terminate_process(self):
        selected_item = self.process_list.currentItem()
        if selected_item:
            pid = int(selected_item.text().split(" - ")[0])
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                QMessageBox.information(self, "Success", f"Process {pid} terminated.")
                self.refresh_processes()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "No process selected.")

    def show_full_system_info(self):
        info = f"System: {platform.system()} {platform.release()} ({platform.version()})\n"
        info += f"Machine: {platform.machine()}\n"
        info += f"Processor: {platform.processor()}\n"
        info += f"CPU Cores: {psutil.cpu_count(logical=False)}\n"
        info += f"Logical CPUs: {psutil.cpu_count(logical=True)}\n"
        info += f"Total RAM: {psutil.virtual_memory().total / (1024 * 1024):.2f} MB\n"
        info += f"Available RAM: {psutil.virtual_memory().available / (1024 * 1024):.2f} MB\n"
        info += f"Used RAM: {psutil.virtual_memory().used / (1024 * 1024):.2f} MB\n"
        info += f"RAM Usage Percentage: {psutil.virtual_memory().percent}%\n"
        info += f"Total Disk Space: {psutil.disk_usage('/').total / (1024 * 1024 * 1024):.2f} GB\n"
        info += f"Used Disk Space: {psutil.disk_usage('/').used / (1024 * 1024 * 1024):.2f} GB\n"
        info += f"Available Disk Space: {psutil.disk_usage('/').free / (1024 * 1024 * 1024):.2f} GB\n"
        info += f"Disk Usage Percentage: {psutil.disk_usage('/').percent}%\n"
        info += f"Network Interfaces: {psutil.net_if_addrs()}\n"
        info += f"Network Stats: {psutil.net_if_stats()}\n"
        
        QMessageBox.information(self, "Full System Information", info)

    def show_message(self):
        QMessageBox.information(self, "Telegram Channel", "Channel - https://goodperexod.t.me")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ProcessViewer()
    viewer.show()
    sys.exit(app.exec_())


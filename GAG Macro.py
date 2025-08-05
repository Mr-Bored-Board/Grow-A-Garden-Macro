import sys, re, requests, json, appdirs
from packaging import version
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from appdirs import user_data_dir



current_macro_version = "0.0.0.1"
macro_requirements_url = "https://raw.githubusercontent.com/Mr-Bored-Board/Grow-A-Garden-Macro/main/Macro%20Requirements.json"
github_release_url = "https://api.github.com/repos/Mr-Bored-Board/Grow-A-Garden-Macro/releases/latest"
latest_macro_version = None

# make the script tell the user what went wrong if something happened
def check_for_updates():
    try:
        response = requests.get(macro_requirements_url, timeout=5)
        if response.status_code == 200:
            config = json.loads(response.text)
            macro_info = config["Macro Requirements"]["latest_macro_version"]
            print(macro_info)
            global latest_macro_version
            latest_macro_version = macro_info.get("Latest Macro Version", None)
            if latest_macro_version:
                return version.parse(latest_macro_version) > version.parse(current_macro_version)
            else:
                print("Could not find 'Latest Macro Version' in config.")
                return False
        else:
            print("Failed to fetch requirements.json (HTTP {})".format(response.status_code))
            return False
    except Exception as e:
        QMessageBox.information(None, "Error", f"Failed to check for updates: {str(e)}")
    return False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GAG Macro")
        self.setGeometry(100, 100, 400, 100)
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.status_label = QLabel("Status: Stopped")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        vbox.addWidget(self.status_label)
        vbox.addLayout(hbox)
        central_widget.setLayout(vbox)
        self.setObjectName("MainWindow")
        self.status_label.setObjectName("Status_Label")
        self.setStyleSheet("""QMainWindow {background-color: black; } QPushButton {background-color: black; color: cyan; border-radius: 5px; border: 1px solid cyan; font-size: 30px;} QLabel {color: cyan; font-size: 50px;}""")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    check_for_updates()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
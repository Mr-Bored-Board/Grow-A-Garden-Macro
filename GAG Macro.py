import sys, re, requests, json, appdirs, os, socket, subprocess
from packaging import version
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from appdirs import user_data_dir

current_macro_version = "0.0.0.2"
macro_requirements_url = "https://raw.githubusercontent.com/Mr-Bored-Board/Grow-A-Garden-Macro/main/Macro%20Requirements.json"
github_release_url = "https://api.github.com/repos/Mr-Bored-Board/Grow-A-Garden-Macro/releases/latest"
updater_url = github_release_url + "/download/GAG%20Macro%20Updater.exe"
updater_location = os.path.join(user_data_dir("GAG Macro", "Bored Developments"), "GAG Macro Updater.exe")
latest_macro_version = None

def show_exception_message(error, location=None):
    error_key = {404: f"{location} Not Found"}
    try:
        error_message = error_key[error]
    except KeyError:
        error_message = str(error)

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(f"An Error Occurred: {error_message}")
    msg.exec_()

# make the script tell the user what went wrong if something happened
def check_for_updates():
    try:
        response = requests.get(macro_requirements_url, timeout=5)
        if response.status_code == 200:
            macro_requirements_json = json.loads(response.text)
            global latest_macro_version
            latest_macro_version = macro_requirements_json["Macro Requirements"]["Latest Macro Version"]
            if version.parse(latest_macro_version) > version.parse(current_macro_version):
                update_macro()
        else:
            QMessageBox.warning(None, "Error", "Failed to fetch requirements.json (HTTP {})".format(response.status_code))
            return False
    except Exception as e:
        show_exception_message(e)
    return False

def check_if_updater_exists():
    if os.path.exists(updater_location):
        pass
    else:
        create_updater()

def create_updater():
    global updater_url, updater_location
    try:
        response = requests.get(updater_url, timeout=3)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(updater_location), exist_ok=True)
            with open(updater_location, "wb") as f:
                f.write(response.content)
            return True
        else:
            show_exception_message(404)
            return False
    except Exception as e:
        show_exception_message(e)
        return False

def update_macro():
    subprocess.Popen([updater_location], close_fds=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Updater:
        try:
            Updater.connect(('localhost', 32968))
            Updater.sendall(b"Update")
            Updater_Response = Updater.recv(1024)
            status = Updater_Response.decode() == "True"
            if status:
                Updater.sendall(__file__.encode())
        except Exception as e:
            print(f"Socket error: {e}")
    sys.exit()

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
    check_if_updater_exists()
    check_for_updates()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
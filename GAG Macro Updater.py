import sys, socket, subprocess, os, requests
from PyQt5.QtWidgets import QApplication, QMessageBox
github_release_url = "https://api.github.com/repos/Mr-Bored-Board/Grow-A-Garden-Macro/releases/latest"
main_macro_url = github_release_url + "/download/GAG Macro.exe"

def check_status():
    global main_macro_url
    try:
        global response
        response = requests.get(main_macro_url, timeout=3)
        if response.status_code == 200:
            return True
        
    except Exception as e:
        print(f"Error creating updater: {e}")
        return False

def update_macro():
    Updater = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Updater.bind(('localhost', 32968))
    Updater.listen(1)
    conn, addr = Updater.accept()
    with conn:
        data = conn.recv(1024)
        if data == b"Update":
            status = check_status()
            conn.sendall(str(status).encode())
            global main_macro_location
            main_macro_location = conn.recv(1024).decode()

    if status:
        with open(main_macro_location, "wb") as f:
            f.write(response.content)
        
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen([main_macro_location], close_fds=True , creationflags=DETACHED_PROCESS)
        app = QApplication(sys.argv)
        QMessageBox.information(None, "Update", "Macro updated successfully.")
        sys.exit()



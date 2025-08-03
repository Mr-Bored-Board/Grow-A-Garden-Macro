import sys, re, requests
from packaging import version
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

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
        self.status_label.setAlignment(Qt.AlignCenter)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
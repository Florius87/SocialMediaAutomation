import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QInputDialog,
    QSpinBox, QLabel
)
from PyQt5.QtCore import QThread, pyqtSignal

print("GUI started")

class ScriptRunner(QThread):
    output_signal = pyqtSignal(str)
    input_request_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None
        self.waiting_for_input = False

    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8"
            )
            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.output_signal.emit(line)
                # Detect input request
                if "Approve, Deny, Skip, or Quit? [a/d/s/q]:" in line:
                    self.waiting_for_input = True
                    self.input_request_signal.emit()
                    while self.waiting_for_input:
                        self.msleep(100)
            self.process.stdout.close()
            self.process.wait()
        except Exception as e:
            self.output_signal.emit(f"Error: {e}\n")
        self.finished_signal.emit()

    def send_input(self, text):
        if self.process and self.process.stdin:
            self.process.stdin.write(text + '\n')
            self.process.stdin.flush()
        self.waiting_for_input = False

runner = None

def run_script(command):
    global runner
    # Disable workflow buttons during run
    btn_crawl.setEnabled(False)
    btn_posts.setEnabled(False)
    btn_approve.setEnabled(False)
    btn_send.setEnabled(False)
    # Disable action bar at start
    set_action_bar_enabled(False)
    textedit.clear()
    runner = ScriptRunner(command)
    runner.output_signal.connect(lambda s: textedit.append(s.rstrip()))
    runner.finished_signal.connect(enable_buttons)
    runner.input_request_signal.connect(wait_for_action)
    runner.start()

def enable_buttons():
    btn_crawl.setEnabled(True)
    btn_posts.setEnabled(True)
    btn_approve.setEnabled(True)
    btn_send.setEnabled(True)
    set_action_bar_enabled(False)
    label_waiting.setText("")

def wait_for_action():
    set_action_bar_enabled(True)
    label_waiting.setText("Waiting for your action...")

def set_action_bar_enabled(enabled):
    btn_action_approve.setEnabled(enabled)
    btn_action_deny.setEnabled(enabled)
    btn_action_skip.setEnabled(enabled)
    btn_action_quit.setEnabled(enabled)

def send_action_input(letter):
    global runner
    if runner:
        runner.send_input(letter)
    set_action_bar_enabled(False)
    label_waiting.setText("")

def crawl():
    run_script(['python', 'crawler.py'])

def posts():
    count = spin_posts.value()
    run_script(['python', 'main.py', str(count)])

def approve():
    run_script(['python', 'Approve.py'])

def send():
    run_script(['python', 'send.py'])

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Workflow Control")
window.resize(780, 450)

# ---- Top Workflow Buttons ----
h_layout = QHBoxLayout()
btn_width = 160

btn_crawl = QPushButton("Crawl")
btn_crawl.setFixedWidth(btn_width)
btn_crawl.clicked.connect(crawl)
h_layout.addWidget(btn_crawl)

# Generate Posts with number input
h_posts_layout = QHBoxLayout()
btn_posts = QPushButton("Generate Posts")
btn_posts.setFixedWidth(btn_width)
btn_posts.clicked.connect(posts)
h_posts_layout.addWidget(btn_posts)

spin_posts = QSpinBox()
spin_posts.setMinimum(1)
spin_posts.setMaximum(20)
spin_posts.setValue(1)
spin_posts.setFixedWidth(60)
h_posts_layout.addWidget(QLabel("How many:"))
h_posts_layout.addWidget(spin_posts)

h_layout.addLayout(h_posts_layout)

btn_approve = QPushButton("Approve")
btn_approve.setFixedWidth(btn_width)
btn_approve.clicked.connect(approve)
h_layout.addWidget(btn_approve)

btn_send = QPushButton("Send (Twitter)")
btn_send.setFixedWidth(btn_width)
btn_send.clicked.connect(send)
h_layout.addWidget(btn_send)

# ---- Output Area ----
textedit = QTextEdit()
textedit.setPlaceholderText("Output will appear here")
textedit.setFixedHeight(270)
textedit.setReadOnly(True)

# ---- Action Bar (Approve/Deny/Skip/Quit) ----
action_bar = QHBoxLayout()
btn_action_approve = QPushButton("Approve")
btn_action_deny = QPushButton("Deny")
btn_action_skip = QPushButton("Skip")
btn_action_quit = QPushButton("Quit")
for b in [btn_action_approve, btn_action_deny, btn_action_skip, btn_action_quit]:
    b.setFixedWidth(110)
    action_bar.addWidget(b)

btn_action_approve.clicked.connect(lambda: send_action_input('a'))
btn_action_deny.clicked.connect(lambda: send_action_input('d'))
btn_action_skip.clicked.connect(lambda: send_action_input('s'))
btn_action_quit.clicked.connect(lambda: send_action_input('q'))

set_action_bar_enabled(False)  # Start disabled

label_waiting = QLabel("")
label_waiting.setStyleSheet("color: #666; margin-top: 4px; margin-bottom: 4px;")

# ---- Layout All ----
v_layout = QVBoxLayout()
v_layout.addLayout(h_layout)
v_layout.addWidget(textedit)
v_layout.addWidget(label_waiting)
v_layout.addLayout(action_bar)

window.setLayout(v_layout)
window.show()
app.exec_()

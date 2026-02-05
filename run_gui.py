"""
Launch the Biometric Systems PyQt5 GUI.
Run from project root: python run_gui.py
"""
import os
import sys

# Ensure project root is on path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Change to project root so relative paths in config work
os.chdir(PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from gui.window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Biometric Systems")
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

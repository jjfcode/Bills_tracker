import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.gui.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop() 
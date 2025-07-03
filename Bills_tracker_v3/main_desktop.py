import sys
import os
import tkinter
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.core.db import initialize_database
from src.gui.main_window import MainWindow

if __name__ == "__main__":
    # Initialize database before starting the application
    initialize_database()
    
    app = MainWindow()
    try:
        app.mainloop()
    except tkinter.TclError as e:
        if "bad window path name" in str(e) or "focus" in str(e):
            pass  # Ignorar error de focus en widgets destruidos
        else:
            raise 
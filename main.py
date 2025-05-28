import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'package')))

from package.views import AppFinanceiro

if __name__ == "__main__":
    root = tk.Tk()
    app = AppFinanceiro(root)
    root.mainloop()
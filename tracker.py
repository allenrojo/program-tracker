import time
import threading
import tkinter as tk
from tkinter import ttk
import pygetwindow as gw

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Program Usage Tracker")
        self.geometry("400x300")
        
        self.tree = ttk.Treeview(self, columns=("Program", "Time Spent (seconds)"), show='headings')
        self.tree.heading("Program", text="Program")
        self.tree.heading("Time Spent (seconds)", text="Time Spent (seconds)")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.usage = {}
        self.update_ui()

    def update_ui(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for program, time_spent in self.usage.items():
            self.tree.insert("", tk.END, values=(program, time_spent))
        self.after(1000, self.update_ui)

    def track_time(self):
        while True:
            active_window = get_active_window_title()
            if active_window:
                if active_window not in self.usage:
                    self.usage[active_window] = 0
                self.usage[active_window] += 1
            time.sleep(1)

def get_active_window_title():
    try:
        active_window = gw.getActiveWindow()
        return active_window.title if active_window else None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    app = App()
    tracking_thread = threading.Thread(target=app.track_time, daemon=True)
    tracking_thread.start()
    app.mainloop()
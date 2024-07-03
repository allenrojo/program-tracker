import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt5.QtCore import QTimer
import pygetwindow as gw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotCanvas, self).__init__(fig)
        self.setParent(parent)

    def plot_donut(self, usage):
        self.axes.clear()
        programs = list(usage.keys())
        times = list(usage.values())
        
        # Create labels with time spent
        labels = [f"{program} ({time_spent} s)" for program, time_spent in zip(programs, times)]
        
        # Plotting the donut chart
        self.axes.pie(times, labels=labels, startangle=90, counterclock=False, wedgeprops={'width': 0.4})
        self.axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.axes.set_title('Program Usage')
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Program Usage Tracker")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.title_label = QLabel("Program Usage Tracker", self)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.desc_label = QLabel("Track time spent on different programs", self)
        self.layout.addWidget(self.desc_label)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Program", "Time Spent (seconds)"])
        self.layout.addWidget(self.table)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.start_button = QPushButton("Start Tracking")
        self.start_button.clicked.connect(self.start_tracking)
        self.button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Tracking")
        self.stop_button.clicked.connect(self.stop_tracking)
        self.button_layout.addWidget(self.stop_button)

        self.clear_button = QPushButton("Clear Data")
        self.clear_button.clicked.connect(self.clear_data)
        self.button_layout.addWidget(self.clear_button)

        self.plot_button = QPushButton("Show Donut Chart")
        self.plot_button.clicked.connect(self.show_plot)
        self.button_layout.addWidget(self.plot_button)

        self.status_label = QLabel("Status: Stopped", self)
        self.layout.addWidget(self.status_label)

        self.plot_canvas = PlotCanvas(self, width=5, height=4)
        self.layout.addWidget(self.plot_canvas)

        self.usage = {}
        self.tracking = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)

    def update_ui(self):
        self.table.setRowCount(0)
        for program, time_spent in self.usage.items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(program))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(time_spent)))

    def start_tracking(self):
        if not self.tracking:
            self.tracking = True
            self.status_label.setText("Status: Tracking")
            self.tracking_thread = threading.Thread(target=self.track_time, daemon=True)
            self.tracking_thread.start()
            self.timer.start(1000)

    def stop_tracking(self):
        self.tracking = False
        self.status_label.setText("Status: Stopped")
        self.timer.stop()

    def clear_data(self):
        self.usage.clear()
        self.update_ui()

    def show_plot(self):
        self.plot_canvas.plot_donut(self.usage)

    def track_time(self):
        while self.tracking:
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
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

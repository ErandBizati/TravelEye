#-------------------#
# File: TravelEye.py #
#-------------------#

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCursor
import MultiSigDetection
import multipleChoiceMenu

# Simulating SEARCHLIST and TRESHOLD from MultiSigDetection
SEARCHLIST = MultiSigDetection.SEARCHLIST
TRESHOLD = MultiSigDetection.TRESHOLD

class TravelEye(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TravelEye")
        self.setGeometry(0, 0, 1024, 600)  # Adjust for 1024x600 resolution
        self.setStyleSheet("background-color: black; color: lime;")

        self.inputList = []
        self.recursive_timer = QTimer()  # Initialize QTimer for recursive scanning
        self.recursive_timer.timeout.connect(self.update_recursive_scan)  # Connect timer to update function
        self.current_freq = None  # Track the frequency being recursively scanned

        # Create a stacked widget to hold all frames
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize UI components
        self.initUI()

    def initUI(self):
        # Main menu
        self.main_menu_widget = QWidget()
        self.main_menu_layout = QVBoxLayout()
        self.main_menu_layout.setSpacing(20)  # Increase spacing for touch-friendliness
        self.main_menu_widget.setLayout(self.main_menu_layout)

        title = QLabel("TravelEye")
        title.setStyleSheet("font-family: Courier; font-size: 32px; font-weight: bold; color: lime;")
        title.setAlignment(Qt.AlignCenter)
        self.main_menu_layout.addWidget(title)

        start_button = QPushButton("Start Scan")
        start_button.clicked.connect(self.start_scan)
        self.set_button_style(start_button)
        self.main_menu_layout.addWidget(start_button)

        help_button = QPushButton("Help/Instructions")
        help_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.help_widget))
        self.set_button_style(help_button)
        self.main_menu_layout.addWidget(help_button)

        about_button = QPushButton("About")
        about_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.about_widget))
        self.set_button_style(about_button)
        self.main_menu_layout.addWidget(about_button)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)
        self.set_button_style(quit_button)
        self.main_menu_layout.addWidget(quit_button)

        # Help frame
        self.help_widget = QWidget()
        help_layout = QVBoxLayout()
        help_layout.setSpacing(20)

        help_text = QLabel("Instructions:\n1. Press Start to scan\n2. Tap a frequency to view details.")
        help_text.setStyleSheet("font-family: Courier; font-size: 20px; color: lime;")
        help_layout.addWidget(help_text)

        help_back_button = QPushButton("Back")
        help_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu_widget))
        self.set_button_style(help_back_button)
        help_layout.addWidget(help_back_button)
        self.help_widget.setLayout(help_layout)

        # About frame
        self.about_widget = QWidget()
        about_layout = QVBoxLayout()
        about_layout.setSpacing(20)

        about_text = QLabel("Travel Eye v1.3\nA tool for scanning RF signals.")
        about_text.setStyleSheet("font-family: Courier; font-size: 20px; color: lime;")
        about_layout.addWidget(about_text)

        about_back_button = QPushButton("Back")
        about_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu_widget))
        self.set_button_style(about_back_button)
        about_layout.addWidget(about_back_button)
        self.about_widget.setLayout(about_layout)

        # Result frame with scrollable area
        self.result_widget = QWidget()
        result_layout = QVBoxLayout()
        result_layout.setSpacing(20)

        # Labels for total signals detected and strongest signal
        self.total_signals_label = QLabel("Total Signals Detected: 0")
        self.total_signals_label.setStyleSheet("font-family: Courier; font-size: 20px; color: lime;")
        result_layout.addWidget(self.total_signals_label)

        self.strongest_signal_label = QLabel("Strongest Signal: N/A")
        self.strongest_signal_label.setStyleSheet("font-family: Courier; font-size: 20px; color: lime;")
        result_layout.addWidget(self.strongest_signal_label)

        # Scroll area for frequency buttons
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setSpacing(15)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        
        result_layout.addWidget(self.scroll_area)

        # "Scan Again" and "Back" buttons in result screen
        button_layout = QHBoxLayout()
        
        scan_again_button = QPushButton("Scan Again")
        scan_again_button.clicked.connect(self.start_scan)
        self.set_button_style(scan_again_button)
        button_layout.addWidget(scan_again_button)

        result_back_button = QPushButton("Back")
        result_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu_widget))
        self.set_button_style(result_back_button)
        button_layout.addWidget(result_back_button)

        result_layout.addLayout(button_layout)
        self.result_widget.setLayout(result_layout)

        # Recursive scan frame
        self.recursive_widget = QWidget()
        recursive_layout = QVBoxLayout()
        recursive_layout.setSpacing(20)

        self.recursive_label = QLabel("")
        self.recursive_label.setStyleSheet("font-family: Courier; font-size: 20px; color: lime;")
        recursive_layout.addWidget(self.recursive_label)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.go_to_menu)
        self.set_button_style(next_button)
        recursive_layout.addWidget(next_button)

        back_button_recursive = QPushButton("Back")
        back_button_recursive.clicked.connect(self.stop_recursive_scan)
        self.set_button_style(back_button_recursive)
        recursive_layout.addWidget(back_button_recursive)

        self.recursive_widget.setLayout(recursive_layout)

        # Add all widgets to the stacked widget
        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.help_widget)
        self.stacked_widget.addWidget(self.about_widget)
        self.stacked_widget.addWidget(self.result_widget)
        self.stacked_widget.addWidget(self.recursive_widget)

    def set_button_style(self, button):
        # Button styles with a green border and solid green background when pressed, no focus outline
        button.setStyleSheet(
            """
            QPushButton {
                font-family: Courier;
                font-size: 20px; 
                font-weight: bold; 
                color: lime; 
                background-color: black; 
                padding: 20px; 
                border: 2px solid lime;
                outline: none;
            }
            QPushButton:pressed {
                background-color: green;
                color: black;
                border: 2px solid green;
                outline: none;
            }
            """
        )

    def go_to_menu(self):
        multipleChoiceMenu.menu([(self.recursive_label.text())])

    def start_scan(self):
        # Clear previous scan results
        self.inputList = []
        self.total_signals_label.setText("Total Signals Detected: 0")
        self.strongest_signal_label.setText("Strongest Signal: N/A")

        for i in reversed(range(self.scroll_layout.count())): 
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        max_power = None
        max_signal = None

        # Perform scan and create frequency buttons
        for freq in SEARCHLIST:
            try:
                result = MultiSigDetection.scan(MultiSigDetection.sdr, freq, TRESHOLD)
                if result:
                    for detected in result:
                        freq_found, power = detected
                        self.inputList.append((freq_found, power))

                        # Track the strongest signal
                        if max_power is None or power > max_power:
                            max_power = power
                            max_signal = freq_found

                        # Create button for each detected frequency
                        freq_button = QPushButton(f"{freq_found:.2f} MHz | {power:.2f} dB")
                        freq_button.clicked.connect(lambda _, f=freq_found: self.start_recursive_scan(f))
                        self.set_button_style(freq_button)
                        self.scroll_layout.addWidget(freq_button)
            except Exception as e:
                error_label = QLabel(f"Error scanning {freq} MHz")
                error_label.setStyleSheet("font-family: Courier; color: red; font-size: 16px;")
                self.scroll_layout.addWidget(error_label)

        # Update total signals and strongest signal
        self.total_signals_label.setText(f"Total Signals Detected: {len(self.inputList)}")
        if max_signal is not None:
            self.strongest_signal_label.setText(f"Strongest Signal: {max_signal:.2f} MHz | {max_power:.2f} dB")

        self.stacked_widget.setCurrentWidget(self.result_widget)

    def start_recursive_scan(self, freq):
        if self.recursive_timer.isActive():
            self.recursive_timer.stop()

        self.current_freq = freq
        self.recursive_label.setText(f"Scanning {freq:.2f} MHz...")
        self.stacked_widget.setCurrentWidget(self.recursive_widget)

        self.recursive_timer.start(1000)

    def update_recursive_scan(self):
        if self.current_freq is None:
            return

        result = MultiSigDetection.scan(MultiSigDetection.sdr, self.current_freq, TRESHOLD)
        if result:
            for detected in result:
                freq_found, power = detected
                self.recursive_label.setText(f"Signal at {freq_found:.2f} MHz: {power:.2f} dB")
        else:
            self.recursive_label.setText(f"No signal detected at {self.current_freq:.2f} MHz")

    def stop_recursive_scan(self):
        if self.recursive_timer.isActive():
            self.recursive_timer.stop()
        self.stacked_widget.setCurrentWidget(self.result_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)  # Hide the cursor application-wide
    window = TravelEye()
    window.showFullScreen()
    sys.exit(app.exec_())

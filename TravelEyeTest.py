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
        next_button.clicked.connect(lambda: self.menu(self.inputList))
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
        multipleChoiceMenu.menu(inputList)

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
                        #self.inputList.append((freq_found, power))

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
        self.inputList.append((self.current_freq, freq, 'power'))
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

    def menu(self, inputList):

        self.mcm_widget = QWidget()
        mcm_layout = QVBoxLayout()
        mcm_layout.setSpacing(20)

        #self.mcm_label = QLabel("")
        self.mcm_label.setStyleSheet("font-family: Courier; font-size: 20px; color: lime;")
        mcm_layout.addWidget(self.mcm_widget)

        #self.mcm.setLayout(mcm_layout)

        # Define styles for text and buttons
        text_styleg = "color: lime; font-family: Courier; font-size: 16px; font-weight: bold;"
        text_styley = "color: yellow; font-family: Courier; font-size: 16px; font-weight: bold;"
        text_styleo = "color: orange; font-family: Courier; font-size: 16px; font-weight: bold;"
        text_styler = "color: red; font-family: Courier; font-size: 16px; font-weight: bold;"
        title_text_style = "color: lime; font-family: Courier; font-size: 28px; font-weight: bold;"
        button_style = "background-color: black; color: lime; font-family: Courier; font-size: 14px; font-weight: bold; border: 2px solid lime; padding: 10px;"



        def yes1():
            question.setText("Are you able to touch the device?")
            yes_button.clicked.connect(yesTouch)
            no_button.clicked.connect(noTouch)

        def no1():
            question.setText("It could be hidden. \nCheck smoke alarms, power outlets, walls, lights, etc.\nDid you find anything?")
            yes_button.clicked.connect(yes1)
            no_button.clicked.connect(noSmoke)

        def yesTouch():
#            if len(inputList) > 1:
#                question.setText("There seems to be another signal found, move onto the next?")
#                yes_button.setText("Next")
#                yes_button.clicked.connect(nextFreq)
#            else:
            question.setText("If you never gave consent for a camera or microphone to be where you are,\nyou may be allowed to disable it. Look for power buttons around the device. \nIf there is not one, see if it is connected to a power source like an outlet and unplug it.\nIf none of these options are possible, your best scenario may be to physically obstruct the camera \nso it cannot see you and muffle the sound by wrapping it in something like a towel.\n If it is a microphone, muffle the sound with something like a towel or blanket and be wary.")
            reset_button = QPushButton("Back", window)
            reset_button.setStyleSheet(button_style)
            reset_button.clicked.connect(self.result_widget)
            mcm_layout.addWidget(reset_button)

        def noTouch():
            question.setText("If the device is a microphone, it may be impossible to stop it. \nLook for places it may be plugged into like outlets or holes in the wall and unplug it if possible.\nBe careful of what you say in the room\nIf it is a camera, try to cover the line of sight so that it cannot see you.\nIt still may be able to hear, so be careful.")
            reset_button = QPushButton("Back", window)
            reset_button.setStyleSheet(button_style)
            reset_button.clicked.connect(self.result_widget)
            mcm_layout.addWidget(reset_button)

        def yesWindow():
            question.setText("Try to cover any windows or openings near you.\nThis may be where you are being monitored from.\nBlock your windows as well as you can.")
            reset_button = QPushButton("Back", window)
            reset_button.setStyleSheet(button_style)
            reset_button.clicked.connect(rescan)
            mcm_layout.addWidget(reset_button)

        def noWindow():
            question.setText("There may be a false signal or it is well hidden. \nKeep searching or scan again.")
            reset_button = QPushButton("Back", window)
            reset_button.setStyleSheet(button_style)
            reset_button.clicked.connect(rescan)
            mcm_layout.addWidget(reset_button)


        if len(inputList) != 0: 
            result = inputList[0]
        else:
            result = (-1, -1)





        resultString = f'A frequency was found at {result[0]} MHz\n'
        label = QLabel(resultString, window)



        #list of extremely hostile frequencies
        xHostileList = [37.6000,49.8300,49.8550,49.8900,139.6000,140.0000,140.8500,143.5000,146.5350,146.5356,148.0050,164.4625,164.8625,166.6625,166.8625,168.0000,168.8000,169.4450,169.5050,170.1000,170.2450,170.3050,170.4875,170.9750,171.0450,171.1050,171.4500,171.6000,171.8250,171.8450,171.9050,172.0000,172.2000,172.8875,172.8875,173.3500,175.0200,184.8500,190.6000,203.0000,221.5000,224.5000,303.6150,303.8250,304.2450,304.2614,310.0000,314.3750,314.8500,315.0000,321.9850,391.2050,392.7280,398.6050,399.0300,399.4550,414.9800,416.2500,416.8450,418.0000,420.5440,423.1250,427.1250,427.4750,427.8250,428.6350,429.5050,433.9200,439.2500,499.9700,499.9750,673.9350,1310.0000,1350.0000,1521.3068,1572.0350]

        resultString += f'A frequency was found at {result[0]} MHz\n'
        #very long list of possibilities
        if float(result[0]) in xHostileList:
            label.setStyleSheet(text_styler)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: EXTREME")

        #20-45
        elif float(result[0]) >= 20 and float(result[0]) < 45:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Medium")
            
            resultString += 'The device is likely an old camera or microphone.'
            secondLabel.setText(resultString)
            
        #45-50
        elif float(result[0]) >= 45 and float(result[0]) < 50:
            label.setStyleSheet(text_styler)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: EXTREME")
            
            resultString += 'This is in the range of a list of devices that can be very likely for surveillance devices. \nIt can be a camera or a microphone.'
            secondLabel.setText(resultString)
            
        #45-88
        elif float(result[0]) >= 45 and float(result[0]) < 88:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'This is in the range of a list of devices that can be very likely for surveillance devices.\n It can be a camera or a microphone.'
            secondLabel.setText(resultString)
            
        #88-108
        elif float(result[0]) >= 88 and float(result[0]) < 108:
            label.setStyleSheet(text_styley)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Medium")
            
            resultString += 'The range this frequency is in is likely for eavesdropping devices \nlike microphones or crystal controlled devices.'
            secondLabel.setText(resultString)
            
        #108-135
        elif float(result[0]) >= 108 and float(result[0]) < 135:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in is likely to be a low cost device for eavesdropping. \nMicrophone is likely.'
            secondLabel.setText(resultString)
            
        #135-150
        elif float(result[0]) >= 135 and float(result[0]) < 150:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in is where thousands of eavesdropping devices are used. \nBe very wary of a microphone or other devices such as kit bugs.'
            secondLabel.setText(resultString)
            
        #150-175
        elif float(result[0]) >= 150 and float(result[0]) < 175:
            label.setStyleSheet(text_styler)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: EXTREME")
            
            resultString += 'The range this frequency is in is very popular for wireless microphones.'
            secondLabel.setText(resultString)
            
        #175-200
        elif float(result[0]) >= 175 and float(result[0]) < 200:
            label.setStyleSheet(text_styley)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Medium")
            
            resultString += 'The range this frequency is in is popular for wireless microphones.'
            secondLabel.setText(resultString)
            
        #200-225
        elif float(result[0]) >= 200 and float(result[0]) < 225:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in is very popular for eavesdropping devices. \nBe wary of anything nearby.'
            secondLabel.setText(resultString)
            
        #225-300
        elif float(result[0]) >= 225 and float(result[0]) < 300:
            label.setStyleSheet(text_styleg)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Low")
            
            resultString += 'The range this frequency is in is mainly for the military. \nIt is unlikely there is a device, but if there is it is a low power device.'
            secondLabel.setText(resultString)
            
        #300-365
        elif float(result[0]) >= 300 and float(result[0]) < 365:
            label.setStyleSheet(text_styley)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Medium")
            
            resultString += 'The range this frequency is in is mainly used for military purposes, \nbut there are some possibilities of devices watching or listening.'
            secondLabel.setText(resultString)
            
        #365-420
        elif float(result[0]) >= 365 and float(result[0]) < 400:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in has many newer eavesdropping devices. \nBe careful when talking.'
            secondLabel.setText(resultString)
            
        #420-450
        elif float(result[0]) >= 420 and float(result[0]) < 450:
            label.setStyleSheet(text_styler)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High to EXTREME")
            
            resultString += 'The range this frequency is in is can be very dangerous. \nIf between 433 MHz and 434 MHz it is very likely to be a device.'
            secondLabel.setText(resultString)
            
        #450-470
        elif float(result[0]) >= 450 and float(result[0]) < 470:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in is very popular for long range eavesdropping, \nyou may not find the device.'
            secondLabel.setText(resultString)
            
        #470-700
        elif float(result[0]) >= 470 and float(result[0]) < 700:
            label.setStyleSheet(text_styleg)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Low")
            
            resultString += 'The range this frequency is in is not very popular. \nIf there is a device it could be a low power microphone'
            secondLabel.setText(resultString)
            
        #700-800
        elif float(result[0]) >= 700 and float(result[0]) < 800:
            label.setStyleSheet(text_styler)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: EXTREME")
            
            resultString += 'The range this frequency is in is very popular for wireless microphones.'
            secondLabel.setText(resultString)
            
        #800-900
        elif float(result[0]) >= 800 and float(result[0]) < 900:
            label.setStyleSheet(text_styley)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Medium")
            
            resultString += 'The range this frequency is in is popular for eavesdropping devices.'
            secondLabel.setText(resultString)
            
        #900-928
        elif float(result[0]) >= 900 and float(result[0]) < 928:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in is very popular for spy shop toys. \nIt is likely there is one nearby.'
            secondLabel.setText(resultString)
            
        #928-1000
        elif float(result[0]) >= 928 and float(result[0]) < 1000:
            label.setStyleSheet(text_styley)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Medium")
            
            resultString += 'The range this frequency is in is mainly used by high end equipment. \nCameras and microphones are possibly nearby.'
            secondLabel.setText(resultString)
            
        #1000-1350
        elif float(result[0]) >= 1000 and float(result[0]) < 1350:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in is popular for video and ultra-miniature audio devices.'
            secondLabel.setText(resultString)
            
        #1350-1500
        elif float(result[0]) >= 1350 and float(result[0]) < 1500:
            label.setStyleSheet(text_styley)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Medium")
            
            resultString += 'The range this frequency is in is moderately used. \nIt can be a camera or a microphone.'
            secondLabel.setText(resultString)
            
        #1500-1700
        elif float(result[0]) >= 1500 and float(result[0]) < 1700:
            label.setStyleSheet(text_styleg)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: Low")
            
            resultString += 'The range this frequency is in is where a minor amount of activity is found. \nIt is less likely there is a device nearby.'
            secondLabel.setText(resultString)
            
        #1700-2000
        elif float(result[0]) >= 1700 and float(result[0]) < 2000:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in is has a large amount of audio and video devices. \nBe wary of cameras and microphones.'
            secondLabel.setText(resultString)
            
        #2000-2300
        elif float(result[0]) >= 2000 and float(result[0]) < 2300:
            label.setStyleSheet(text_styleo)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: High")
            
            resultString += 'The range this frequency is in is used by spyshop toys. \nBe wary of ultra-low powered cameras.'
            secondLabel.setText(resultString)
            
        # >2400
        elif float(result[0]) >= 2400:
            label.setStyleSheet(text_styler)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("Threat: EXTREME")
            
            resultString += 'The range this frequency is in is where millions of devices are. \nCameras are very likely to be nearby.'
            secondLabel.setText(resultString)
            
        elif float(result[0]) == -1:
            label.setStyleSheet(text_styleg)
            mcm_layout.addWidget(label)
            secondLabel.setStyleSheet(text_style)
            mcm_layout.addWidget(secondLabel)
            label.setText("No signal was found.\nThe likelihood of a device is very low.\nYou can either scan again or exit.")
            
        if result[0] == -1:
            layout = QVBoxLayout()
            question = QLabel("Something went wrong.", window)
            question.setStyleSheet(title_text_style)
            mcm_layout.addWidget(question)

            result_back_button = QPushButton("Exit")
            result_back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu_widget))
            set_button_style(result_back_button)
            button_layout.addWidget(result_back_button)

        else:

            layout = QVBoxLayout()
            question = QLabel("", window)
            question.setStyleSheet(title_text_style)
            mcm_layout.addWidget(question)

            yes_button = QPushButton("Yes")
            yes_button.clicked.connect(yes1)
            set_button_style(yes_button)
            mcm_layout.addWidget(yes_button)

            no_button = QPushButton("No")
            no_button.clicked.connect(no1)
            set_button_style(no_button)
            mcm_layout.addWidget(no_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)  # Hide the cursor application-wide
    window = TravelEye()
    window.showFullScreen()
    sys.exit(app.exec_())

#-------------------#
#File: TravelEye.py #
#-------------------#

import tkinter as tk
from tkinter import scrolledtext, Listbox, END
from PIL import Image, ImageTk
import MultiSigDetection

# Simulating SEARCHLIST and TRESHOLD from MultiSigDetection
SEARCHLIST = MultiSigDetection.SEARCHLIST
TRESHOLD = MultiSigDetection.TRESHOLD

# Create the main window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.configure(cursor="none")

# Creating frames for different menus
main_menu_frame = tk.Frame(root, bg="black")
help_frame = tk.Frame(root, bg="black")
about_frame = tk.Frame(root, bg="black")
result_frame = tk.Frame(root, bg="black")
recursive_scan_frame = tk.Frame(root, bg="black")  # Frame for recursive scanning

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Themed text style
text_style = {"fg": "lime", "bg": "black", "font": ("Courier", 20, "bold")}  # Increased font size for visibility
title_text_style = {"fg": "lime", "bg": "black", "font": ("Courier", 32, "bold")}  # Increased title text size

status_label = tk.Label(main_menu_frame, text="", **text_style)
status_label.pack(pady=5)

# Main menu widgets
label = tk.Label(main_menu_frame, text="TravelEye", **title_text_style)
label.pack(pady=5)

status_label = tk.Label(main_menu_frame, text="", **text_style)
status_label.pack(pady=5)

# Global variable to store scan result
scan_result = ""

# Function to start the scan and display the result
def start_scan():
    global scan_result
    scan_result = ""
    result_listbox.delete(0, END)
    
    # Perform the scan
    for freq in SEARCHLIST:
        try:
            result = MultiSigDetection.scan(MultiSigDetection.sdr, freq, TRESHOLD)

            if result:
                for detected in result:
                    freq_found, power = detected
                    display_text = f"Detected {freq_found:.2f} MHz with {power:.2f} dB"
                    result_listbox.insert(END, display_text)
            else:
                result_listbox.insert(END, f"No signal detected at {freq} MHz.")

        except Exception as e:
            result_listbox.insert(END, f"Error scanning {freq} MHz: {str(e)}")
            break  # Stop if there's an issue with the RTL-SDR setup

    show_frame(result_frame)

# Themed button style
button_style = {"fg": "lime", "bg": "black", "font": ("Courier", 18, "bold"), "activebackground": "green", "activeforeground": "black", "width": 30, "height": 4, "bd": 2}

# Main menu buttons
start_button = tk.Button(main_menu_frame, text="Start Scan", command=start_scan, **button_style)
start_button.pack(pady=10)

help_button = tk.Button(main_menu_frame, text="Help/Instructions", command=lambda: show_frame(help_frame), **button_style)
help_button.pack(pady=10)

about_button = tk.Button(main_menu_frame, text="About", command=lambda: show_frame(about_frame), **button_style)
about_button.pack(pady=10)

# Quit button on the main menu
quit_button = tk.Button(main_menu_frame, text="Quit", command=root.destroy, **button_style)
quit_button.pack(pady=10)

# Help/Instructions frame widgets
instructions_label = tk.Label(help_frame, text="Instructions:\n1. Press Start to scan\n2. Select a frequency to track it.", **text_style)
instructions_label.pack(pady=40)

back_button = tk.Button(help_frame, text="Back", command=lambda: show_frame(main_menu_frame), **button_style)
back_button.pack(pady=10)

# About frame widgets
about_label = tk.Label(about_frame, text="Travel Eye v1.3\nA tool for scanning RF signals.", **text_style)
about_label.pack(pady=40)

back_button = tk.Button(about_frame, text="Back", command=lambda: show_frame(main_menu_frame), **button_style)
back_button.pack(pady=10)

# Result frame widgets with larger font
result_listbox = Listbox(result_frame, width=100, height=20, fg="lime", bg="black", font=("Courier", 20, "bold"))  # Larger font for touch screen visibility
result_listbox.pack(pady=10)

# Event handler to start recursive scan on selected frequency
def on_select_frequency(event):
    selected = result_listbox.curselection()
    if selected:
        freq_text = result_listbox.get(selected[0])
        freq = float(freq_text.split()[1])  # Extract frequency from text
        start_recursive_scan(freq)

result_listbox.bind("<<ListboxSelect>>", on_select_frequency)

# "Scan Again" button in the result frame
scan_again_button = tk.Button(result_frame, text="Scan Again", command=start_scan, **button_style)
scan_again_button.pack(pady=10)

# Back button in result frame to return to main menu
back_button_result = tk.Button(result_frame, text="Back", command=lambda: show_frame(main_menu_frame), **button_style)
back_button_result.pack(pady=10)

# Recursive scanning function
def start_recursive_scan(freq):
    recursive_scan_label.config(text=f"Scanning {freq:.2f} MHz...")
    show_frame(recursive_scan_frame)
    perform_recursive_scan(freq)

def perform_recursive_scan(freq):
    # Only display the latest scan result centered on the chosen frequency
    MultiSigDetection.sdr.center_freq = freq * 1e6  # Center the RTL-SDR on the exact frequency selected
    result = MultiSigDetection.scan(MultiSigDetection.sdr, freq, TRESHOLD)
    
    if result:
        for detected in result:
            freq_found, power = detected
            recursive_scan_label.config(text=f"Signal at {freq_found:.2f} MHz: {power:.2f} dB")
    else:
        recursive_scan_label.config(text="No signal detected.")

    # Call this function every second for continuous scanning
    root.after(1000, perform_recursive_scan, freq)

# Recursive scan frame widgets with larger text
recursive_scan_label = tk.Label(recursive_scan_frame, text="", fg="lime", bg="black", font=("Courier", 28, "bold"))  # Larger text for recursive scan display
recursive_scan_label.pack(pady=5)

back_button_recursive = tk.Button(recursive_scan_frame, text="Back", command=lambda: show_frame(result_frame), **button_style)
back_button_recursive.pack(pady=10)

# Packing the frames
for frame in (main_menu_frame, help_frame, about_frame, result_frame, recursive_scan_frame):
    frame.grid(row=0, column=0, sticky='nsew')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

show_frame(main_menu_frame)
root.mainloop()

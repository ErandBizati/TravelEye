import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import MultiSigDetection  # Importing the MultiSigDetection module

# Simulating SEARCHLIST and TRESHOLD from MultiSigDetection
SEARCHLIST = MultiSigDetection.SEARCHLIST
TRESHOLD = MultiSigDetection.TRESHOLD

# Create the main window
root = tk.Tk()
root.attributes("-fullscreen", True)  # Enable full-screen mode
root.configure(bg="black")  # Set background color to black
root.configure(cursor="none") # Hides mouse cursor

# Creating frames for different menus
main_menu_frame = tk.Frame(root, bg="black")
help_frame = tk.Frame(root, bg="black")
about_frame = tk.Frame(root, bg="black")
result_frame = tk.Frame(root, bg="black")  # New frame to show the scan results

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Themed text style
text_style = {"fg": "lime", "bg": "black", "font": ("Courier", 16, "bold")}
title_text_style = {"fg": "lime", "bg": "black", "font": ("Courier", 28, "bold")}

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
    scan_result = ""  # Clear previous scan results
    result_textbox.delete(1.0, tk.END)  # Clear previous content in the text box
    
    # Perform the scan
    for freq in SEARCHLIST:
        try:
            # Call the scan function from MultiSigDetection for each frequency
            result = MultiSigDetection.scan(MultiSigDetection.sdr, freq, TRESHOLD)

            # If any signals were detected, append them to the result
            if result:
                for detected in result:
                    freq_found, power = detected
                    scan_result += f"Detected signal at {freq_found:.2f} MHz with power {power:.2f} dB\n"
            else:
                scan_result += f"No signal detected at {freq} MHz.\n"

        except Exception as e:
            scan_result += f"Error scanning {freq} MHz: {str(e)}\n"
            break  # Stop if there's an issue with the RTL-SDR setup

    # Insert the new scan results and switch to the result frame
    result_textbox.insert(tk.END, scan_result)  # Insert the new scan results
    show_frame(result_frame)  # Display the result frame

# Themed button style
button_style = {"fg": "lime", "bg": "black", "font": ("Courier", 14, "bold"), "activebackground": "green", "activeforeground": "black", "width": 30, "height": 4, "bd": 2}

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
instructions_label = tk.Label(help_frame, text="Instructions:\n1. Press Start to scan\n2. The scan result will be shown.", **text_style)
instructions_label.pack(pady=40)

back_button = tk.Button(help_frame, text="Back", command=lambda: show_frame(main_menu_frame), **button_style)
back_button.pack(pady=10)

# About frame widgets
about_label = tk.Label(about_frame, text="Travel Eye v1.3\nA tool for scanning RF signals.", **text_style)
about_label.pack(pady=40)

back_button = tk.Button(about_frame, text="Back", command=lambda: show_frame(main_menu_frame), **button_style)
back_button.pack(pady=10)

# Result frame widgets
result_textbox = scrolledtext.ScrolledText(result_frame, width=100, height=20, fg="lime", bg="black", font=("Courier", 12))  # Scrollable textbox for results
result_textbox.pack(pady=10)

# "Scan Again" button in the result frame
scan_again_button = tk.Button(result_frame, text="Scan Again", command=start_scan, **button_style)
scan_again_button.pack(pady=10)

# Back button in result frame to return to main menu
back_button = tk.Button(result_frame, text="Back", command=lambda: show_frame(main_menu_frame), **button_style)
back_button.pack(pady=10)

# Packing the frames and making them fill the entire window
for frame in (main_menu_frame, help_frame, about_frame, result_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configure grid layout to expand the frames
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Show the main menu by default
show_frame(main_menu_frame)

root.after(100, lambda: root.attributes("-fullscreen", True))
root.configure(cursor="none")

root.mainloop()

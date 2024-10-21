import tkinter as tk
from MultiSigDetection import SEARCHLIST, TRESHOLD, scan, sdr  # Import functions from MultiSigDetection.py

# Create the main window
root = tk.Tk()
root.geometry("1024x600")
root.attributes("-fullscreen", True)  # Enable fullscreen mode

# Define a larger font for better touch interaction
large_font = ("Helvetica", 20)
button_font = ("Helvetica", 18)

# Creating frames for different menus
main_menu_frame = tk.Frame(root)
help_frame = tk.Frame(root)
about_frame = tk.Frame(root)
result_frame = tk.Frame(root)  # New frame to show the scan results

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Main menu widgets
label = tk.Label(main_menu_frame, text="Travel Eye", font=large_font)
label.pack(pady=20)

status_label = tk.Label(main_menu_frame, text="", font=large_font)
status_label.pack(pady=20)

# Global variable to store scan result
scan_result = ""


# Function to start the scan and directly show the result
def start_button():
    global scan_result
    scan_result = ""  # Clear previous scan results
    detected_signals = []

    # Loop through SEARCHLIST frequencies and scan
    for freq in SEARCHLIST:
        result = scan(sdr, freq, TRESHOLD)

        # If any signals were detected, append them to the result
        if result:
            for detected in result:
                freq_found, power = detected
                scan_result += f"Detected signal at {freq_found:.2f} MHz with power {power:.2f} dB\n"
        else:
            scan_result += f"No signal detected at {freq} MHz.\n"

    # Update the result label in the result frame and show the result frame
    result_label.config(text=scan_result, font=large_font)
    show_frame(result_frame)


# Buttons for the main menu
start_button = tk.Button(main_menu_frame, text="Start Scan", command=start_button, width=20, height=2, font=button_font)
start_button.pack(pady=20)

help_button = tk.Button(main_menu_frame, text="Help/Instructions", command=lambda: show_frame(help_frame), width=20, height=2, font=button_font)
help_button.pack(pady=20)

about_button = tk.Button(main_menu_frame, text="About", command=lambda: show_frame(about_frame), width=20, height=2, font=button_font)
about_button.pack(pady=20)

# Help/Instructions frame widgets
instructions_label = tk.Label(help_frame, text="Instructions: \n1. Press Start to scan\n2. The scan result will be shown.", font=large_font)
instructions_label.pack(pady=40)

back_button = tk.Button(help_frame, text="Back", command=lambda: show_frame(main_menu_frame), width=20, height=2, font=button_font)
back_button.pack(pady=20)

# About frame widgets
about_label = tk.Label(about_frame, text="Travel Eye v1.3\nA tool for scanning RF signals.", font=large_font)
about_label.pack(pady=40)

back_button = tk.Button(about_frame, text="Back", command=lambda: show_frame(main_menu_frame), width=20, height=2, font=button_font)
back_button.pack(pady=20)

# Result frame widgets
result_label = tk.Label(result_frame, text="", font=large_font)  # This will display the scan result
result_label.pack(pady=20)

exit_button = tk.Button(result_frame, text="Exit", command=lambda: show_frame(main_menu_frame), width=20, height=2, font=button_font)
exit_button.pack(pady=20)

# Packing the frames and making them fill the entire window
for frame in (main_menu_frame, help_frame, about_frame, result_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configure grid layout to expand the frames
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Show the main menu by default
show_frame(main_menu_frame)

root.mainloop()

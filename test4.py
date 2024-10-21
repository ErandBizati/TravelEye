import tkinter as tk
from MultiSigDetection import SEARCHLIST, TRESHOLD, scan, sdr  # Import functions from MultiSigDetection.py

# Create the main window
root = tk.Tk()
root.geometry("1024x600")

# Creating frames for different menus
main_menu_frame = tk.Frame(root)
help_frame = tk.Frame(root)
about_frame = tk.Frame(root)
result_frame = tk.Frame(root)  # New frame to show the scan results

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Main menu widgets
label = tk.Label(main_menu_frame, text="Travel Eye")
label.pack(pady=10)

status_label = tk.Label(main_menu_frame, text="")
status_label.pack(pady=10)

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

    # Clear the text box and insert the new result
    result_textbox.config(state=tk.NORMAL)
    result_textbox.delete(1.0, tk.END)  # Clear previous content
    result_textbox.insert(tk.END, scan_result)
    result_textbox.config(state=tk.DISABLED)  # Disable editing of the text box
    show_frame(result_frame)


# Buttons for the main menu
start_button = tk.Button(main_menu_frame, text="Start Scan", command=start_button, width=20, height=2)
start_button.pack(pady=10)

help_button = tk.Button(main_menu_frame, text="Help/Instructions", command=lambda: show_frame(help_frame), width=20, height=2)
help_button.pack(pady=10)

about_button = tk.Button(main_menu_frame, text="About", command=lambda: show_frame(about_frame), width=20, height=2)
about_button.pack(pady=10)

# Help/Instructions frame widgets
instructions_label = tk.Label(help_frame, text="Instructions: \n1. Press Start to scan\n2. The scan result will be shown.")
instructions_label.pack(pady=40)

back_button = tk.Button(help_frame, text="Back", command=lambda: show_frame(main_menu_frame), width=20, height=2)
back_button.pack(pady=10)

# About frame widgets
about_label = tk.Label(about_frame, text="Travel Eye v1.3\nA tool for scanning RF signals.")
about_label.pack(pady=40)

back_button = tk.Button(about_frame, text="Back", command=lambda: show_frame(main_menu_frame), width=20, height=2)
back_button.pack(pady=10)

# Result frame widgets
result_label = tk.Label(result_frame, text="Scan Results")
result_label.pack(pady=10)

# Scrollbar for the scan results
result_textbox = tk.Text(result_frame, wrap="word", height=20, width=80)
result_textbox.config(state=tk.DISABLED)  # Initially disable the textbox
result_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_frame, command=result_textbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_textbox.config(yscrollcommand=scrollbar.set)

# Buttons in the result frame
button_frame = tk.Frame(result_frame)
button_frame.pack(pady=10)

scan_again_button = tk.Button(button_frame, text="Scan Again", command=start_button, width=20, height=2)
scan_again_button.pack(side=tk.LEFT, padx=5)

back_button = tk.Button(button_frame, text="Back", command=lambda: show_frame(main_menu_frame), width=20, height=2)
back_button.pack(side=tk.LEFT, padx=5)

# Packing the frames and making them fill the entire window
for frame in (main_menu_frame, help_frame, about_frame, result_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configure grid layout to expand the frames
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Show the main menu by default
show_frame(main_menu_frame)

root.mainloop()

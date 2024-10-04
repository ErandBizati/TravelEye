import tkinter as tk
#from PIL import Image, ImageTk
from TestFunctions import scan  # Import the scan function from TestFunctions.py

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

# Load and resize the image
#image = Image.open("/Users/jacobphilips/School/Fall2024/CSC355/python/logo.png")  
#resized_image = image.resize((150, 150), Image.LANCZOS)
#photo = ImageTk.PhotoImage(resized_image)

# Main menu widgets
#image_label = tk.Label(main_menu_frame, image=photo)
#image_label.pack(pady=10)

label = tk.Label(main_menu_frame, text="Travel Eye")
label.pack(pady=10)

status_label = tk.Label(main_menu_frame, text="")
status_label.pack(pady=10)

# Global variable to store scan result
scan_result = ""

# Function to start the scan and directly show the result
def start_button():
    global scan_result
    result = scan()  # Call the scan function from TestFunctions.py

    # Store scan result for display in the result frame
    if isinstance(result, tuple) and result[0] is not None:
        freq, ftype = result
        scan_result = f"Detected {ftype} at {freq} MHz"
    elif isinstance(result, tuple) and result[0] is None:
        scan_result = "No signal detected."
    elif isinstance(result, tuple) and len(result) == 2:
        result1, result2 = result
        freq1, ftype1 = result1
        freq2, ftype2 = result2
        scan_result = f"Detected {ftype1} at {freq1} MHz and {ftype2} at {freq2} MHz"
    
    # Update the result label in the result frame and show the result frame
    result_label.config(text=scan_result)
    show_frame(result_frame)

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
about_label = tk.Label(about_frame, text="Travel Eye v1.0\nA tool for scanning RF signals.")
about_label.pack(pady=40)

back_button = tk.Button(about_frame, text="Back", command=lambda: show_frame(main_menu_frame), width=20, height=2)
back_button.pack(pady=10)

# Result frame widgets
#image_label_result = tk.Label(result_frame, image=photo)  # Logo in result frame
#image_label_result.pack(pady=10)

result_label = tk.Label(result_frame, text="")  # This will display the scan result
result_label.pack(pady=10)

exit_button = tk.Button(result_frame, text="Exit", command=lambda: show_frame(main_menu_frame), width=20, height=2)
exit_button.pack(pady=10)

# Packing the frames and making them fill the entire window
for frame in (main_menu_frame, help_frame, about_frame, result_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configure grid layout to expand the frames
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Show the main menu by default
show_frame(main_menu_frame)

root.mainloop()
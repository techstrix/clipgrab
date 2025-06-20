import requests
import os
import pyperclip
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import threading
import time
import pystray
from PIL import Image
import sys

# Your original functions, unchanged
def is_downloadable(url):
    """
    Check if the URL is downloadable.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def download_file(url,destination):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination,'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            print(f"Failed to download file:Error code{response.status_code}")
    except requests.RequestException as e: 
        print(f"An error occurred while downloading the file: {e}")
        
def get_file_type(url):
    """
    Get the file type from the URL.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '')
        return content_type.split('/')[-1] if content_type else 'unknown'
    except requests.RequestException:
        return 'unknown'

def get_destination_path(filename,destination=None,url=None):
    if not destination:
        destination = os.path.expanduser("~\\Documents")
    
    os.makedirs(destination, exist_ok=True)
    return os.path.join(destination, f"{filename}.{get_file_type(url)}")

def check_clipboard_for_downloadable_content_and_download():
    clipboard_text = pyperclip.paste()
    if is_downloadable(clipboard_text):
        print(f"Downloadable content found in clipboard: {clipboard_text}")
        root = tk.Tk()
        root.title("Clipgrab Clipboard Monitor")
        root.iconbitmap("clipboard_monitor.ico")  # Set the icon for the window
        root.geometry("800x200")
        root.withdraw()  # Hide the main window
        label = tk.Label(root, text=f"Downloadable content found in clipboard: {clipboard_text}")
        label.pack(padx=20, pady=20)
     
        destination_label = tk.Label(root, text="Choose destination please")
        destination_label.pack(padx=20, pady=5)
        def choose_destination_and_download():
            file_type = get_file_type(clipboard_text)
            file_path = filedialog.asksaveasfilename( defaultextension=f".{file_type}",
                filetypes=[("All Files", "*.*")],
                title="Save As")     

            if file_path:
                download_file(clipboard_text, file_path)
                messagebox.showinfo("Download Complete", f"File downloaded to: {file_path}")
            else:
                messagebox.showwarning("Download Cancelled", "No file path provided. Download cancelled.")
        
        label2 = tk.Label(root, text="Do not enter any extension, it will be added automatically")
        destination_button = tk.Button(root, text="Choose Destination and Download", command=choose_destination_and_download)
        destination_button.pack(padx=20, pady=5)
        
        # Make the window visible for the dialog
        root.deiconify()
        root.mainloop()
    else:
        print("No downloadable content found in clipboard.")
        return None

def monitor_clipboard():
    """Continuously monitor the clipboard in a background thread."""
    last_clipboard = None
    while True:
        clipboard_text = pyperclip.paste()
        if clipboard_text != last_clipboard:  # Only process new clipboard content
            check_clipboard_for_downloadable_content_and_download()
            last_clipboard = clipboard_text
        time.sleep(1)  # Check every second to reduce CPU usage

def create_system_tray_icon():
    """Create a system tray icon to control the application."""
    def exit_app(icon, item):
        icon.stop()
        sys.exit()

    # Create a simple placeholder icon (replace with your own .ico file if desired)
    icon = pystray.Icon("Clipboard Monitor")
    icon.icon = Image.open("clipboard_monitor.ico")
    icon.menu = pystray.Menu(
        pystray.MenuItem("Exit", exit_app)
    )
    icon.run()

if __name__ == "__main__":
    # Start clipboard monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    monitor_thread.start()

    # Start system tray icon in a separate thread
    tray_thread = threading.Thread(target=create_system_tray_icon, daemon=True)
    tray_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()
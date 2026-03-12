import tkinter as tk
from tkinter import messagebox
import json
from utils.config_loader import get_config_path, load_config

class SkipperUI:
    def __init__(self, root, listener_manager):
        self.root = root
        self.listener_manager = listener_manager
        
        # Window setup
        self.root.title("Spotify Skipper Settings")
        self.root.geometry("400x250")
        self.root.configure(padx=20, pady=20)
        self.root.resizable(False, False)

        self.config_path = get_config_path()
        self.current_config = load_config()

        # Build UI Elements
        self._build_ui()

    def _build_ui(self):
        # Title
        title = tk.Label(self.root, text="Spotify Global Skipper", font=("Helvetica", 16, "bold"), fg="#1DB954")
        title.pack(pady=(0, 10))

        # Instructions
        instructions = (
            "Enter your desired hotkey combination below.\n"
            "Use <ctrl>, <shift>, <alt> for modifiers.\n"
            "Example: <ctrl>+<shift>+n"
        )
        tk.Label(self.root, text=instructions, justify="center").pack(pady=(0, 15))

        # Hotkey Input Field
        self.hotkey_entry = tk.Entry(self.root, font=("Courier", 14), width=20, justify="center")
        self.hotkey_entry.insert(0, self.current_config.get("hotkey", "<ctrl>+<shift>+s"))
        self.hotkey_entry.pack(pady=5)

        # Save Button
        save_btn = tk.Button(
            self.root, text="Save & Apply", 
            command=self.save_hotkey, 
            bg="#1DB954", fg="white", 
            font=("Helvetica", 11, "bold"),
            relief="flat", width=15
        )
        save_btn.pack(pady=15)

    def save_hotkey(self):
        new_hotkey = self.hotkey_entry.get().strip().lower()
        
        try:
            # Attempt to restart the listener with the new key to validate it
            self.listener_manager.restart_listener(new_hotkey)
            
            # If successful, save to disk
            with open(self.config_path, 'w') as f:
                json.dump({"hotkey": new_hotkey}, f)
                
            messagebox.showinfo("Success", f"Hotkey successfully updated to: {new_hotkey}\n\nYou can now minimize this window. The listener is active in the background.")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid hotkey format!\n\nPlease use valid pynput formatting (e.g. <ctrl>+<shift>+s)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to bind hotkey.\nError: {e}")
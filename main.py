import tkinter as tk
import sys
from ui.app_window import SkipperUI
from core.listener import GlobalListener
from utils.config_loader import load_config

class ListenerManager:
    """Manages the background keyboard listener so the UI can easily restart it."""
    def __init__(self):
        self.listener = None

    def restart_listener(self, hotkey_str):
        self.stop() # Stop existing listener if it exists
        
        # Start the new listener with the provided hotkey
        self.listener = GlobalListener(hotkey_str)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()

def main():
    # 1. Load Config and Start Background Listener
    config = load_config()
    manager = ListenerManager()
    
    try:
        manager.restart_listener(config.get("hotkey", "<ctrl>+<shift>+s"))
    except Exception as e:
        print(f"Failed to start initial listener: {e}")

    # 2. Start the Tkinter UI
    root = tk.Tk()
    
    # Connects the UI to our background manager
    app = SkipperUI(root, manager)

    # 3. Handle window close cleanly
    def on_closing():
        manager.stop()
        root.destroy()
        sys.exit()

    # Bind the 'X' button on the window to our closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Keeps the UI window running on the screen
    root.mainloop()

if __name__ == "__main__":
    main()
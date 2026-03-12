from pynput import keyboard
from core.controller import skip_track

class GlobalListener:
    def __init__(self, hotkey_str):
        self.hotkey_str = hotkey_str
        self.listener = None

    def start(self):
        """Starts the global keyboard listener in a background thread."""
        print(f"Listening for hotkey: {self.hotkey_str}")
        
        # GlobalHotKeys is a convenient class in pynput for handling combos
        self.listener = keyboard.GlobalHotKeys({
            self.hotkey_str: self.on_activate_skip
        })
        
        # Starts the listener thread
        self.listener.start()

    def on_activate_skip(self):
        """Callback executed when the hotkey combination is pressed."""
        skip_track()

    def stop(self):
        """Stops the listener safely."""
        if self.listener:
            self.listener.stop()
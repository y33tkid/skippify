import win32gui
import win32api

# Windows API Constants for Media Controls
WM_APPCOMMAND = 0x0319
APPCOMMAND_MEDIA_NEXTTRACK = 11

def get_spotify_hwnd():
    """Finds the window handle (HWND) for Spotify."""
    hwnds = []
    
    def enum_handler(hwnd, ctx):
        # Removed win32gui.IsWindowVisible(hwnd) check to catch minimized/tray instances
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        
        # Spotify's main window uses the generic Chromium class
        if class_name.startswith("Chrome_WidgetWin"):
            # Check title text (Spotify often changes this based on playing status)
            if title in ["Spotify Premium", "Spotify Free", "Spotify"] or " - " in title:
                ctx.append(hwnd)
    
    # Enumerate through all top-level windows
    win32gui.EnumWindows(enum_handler, hwnds)
    
    # Return the first match, or None if not found
    return hwnds[0] if hwnds else None

def skip_track():
    """Sends the 'Next Track' command directly to the Spotify window."""
    spotify_hwnd = get_spotify_hwnd()
    
    if spotify_hwnd:
        print(f"Skipping track... (Targeted Spotify HWND: {spotify_hwnd})")
        # Send the hardware-level media next command directly to Spotify
        win32api.SendMessage(spotify_hwnd, WM_APPCOMMAND, 0, APPCOMMAND_MEDIA_NEXTTRACK << 16)
    else:
        print("Action Failed: Spotify window not found. Is the application running?")
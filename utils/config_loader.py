import json
import os

def get_config_path():
    """Gets a safe path to save the config file, ensuring it survives after being compiled to an .exe"""
    # Use the Windows AppData directory
    appdata_dir = os.getenv('APPDATA')
    
    if appdata_dir:
        # Create a dedicated folder for our app in AppData
        config_folder = os.path.join(appdata_dir, 'SpotifySkipper')
        os.makedirs(config_folder, exist_ok=True)
        return os.path.join(config_folder, 'config.json')
    else:
        # Fallback if running outside of a standard Windows environment
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')

def load_config():
    """Loads the hotkey configuration."""
    config_path = get_config_path()
    default_config = {"hotkey": "<ctrl>+<shift>+s"}
    
    if not os.path.exists(config_path):
        # Create default config if it doesn't exist yet
        with open(config_path, 'w') as f:
            json.dump(default_config, f)
        return default_config
        
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return default_config
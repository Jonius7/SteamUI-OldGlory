import winreg

def find_library_dir():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Valve\Steam");
    steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
    print(steam_path)
    steamui_path = steam_path.replace("/","\\") + "\steamui"
    print(steamui_path)




from os import name, system

def clear():
    # Check the name attribute to determine the operating system
    if name == 'nt':  # 'nt' represents Windows
        _ = system('cls')  # Use 'cls' command to clear the screen in Windows
    else:
        _ = system('clear')  # Use 'clear' command to clear the screen in Unix/Linux/Mac


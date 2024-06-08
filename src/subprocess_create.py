import subprocess
CREATE_NO_WINDOW = 0x08000000
def run():
    print(str(subprocess.check_output('tasklist', creationflags=CREATE_NO_WINDOW)))

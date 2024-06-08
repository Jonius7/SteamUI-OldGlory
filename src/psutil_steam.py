import psutil

def check_running(process_name="steam.exe"):
    '''for process in psutil.process_iter():
        cmdline = process.cmdline()
        if "steam.exe" in cmdline and "-dev" in cmdline:
            print("Steam is running in -dev mode")
        else:
            print("Steam is not running or not in -dev mode")'''
    
    for process in psutil.process_iter():
        if process.name().startswith(process_name):
            if len(process.cmdline()) >= 2:
                print(process.cmdline())
                args = process.cmdline()[1:]
                print(args)
                dev_running = ['-dev' == arg for arg in args]
                if True in dev_running:
                    print("Steam is running in -dev mode")
                    break
            print("Steam is running")
    #process_list = [(p.name(), p.cmdline()[1]) for p in psutil.process_iter() if p.name().startswith('steam.exe')]
    #print(process_list)
    #running = ['-dev' == process[1] for process in process_list]
    #print(True in running)


def is_process_running_with_arg(process_name, arg):
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if the process name matches
            if process_name.lower() in proc.info['name'].lower():
                # Ensure cmdline is not None and check for the specific argument
                if proc.info['cmdline'] and arg in proc.info['cmdline']:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def run():
    process_name = "steam"
    argument = "-dev"

    if is_process_running_with_arg(process_name, argument):
        print(f"The process {process_name} is running with the argument {argument}.")
    else:
        print(f"The process {process_name} is not running with the argument {argument}.")

#if __name__ == "__main__":
#    run()

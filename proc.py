import psutil
procs = {}
def process_find(path):
    global procs
    if path in procs:
        proc = psutil.Process(procs[path])
        if proc.exe() == path:
            return True
    for proc in psutil.process_iter():
        try:
            if proc.exe() == path:
                if not(path in procs):
                    procs[path] = proc.pid
                return True
        except psutil.AccessDenied:
            pass
    return False
if __name__ == '__main__':
    for i in range(2):
        process_find("C:\Program Files (x86)\Steam\steamapps\common\Stormworks\stormworks64.exe")
        print(procs)
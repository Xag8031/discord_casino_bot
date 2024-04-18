import time
import os
import sys
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, init

init(autoreset=True)

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, cmd):
        self.cmd = cmd
        self.proc = subprocess.Popen(self.cmd)

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            self.proc.kill()
            print(Fore.RED + 'Restarting...')
            self.proc = subprocess.Popen(self.cmd)

if __name__ == "__main__":
    args = sys.argv[1:]
    observer = Observer()
    event_handler = ChangeHandler(args)
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
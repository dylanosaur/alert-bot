import subprocess
import time
from python_scripts.file_watcher import FileWatcher

# Run sysdig command and write output to sysdig_logs.txt
sysdig_process = subprocess.Popen(["sudo", "sysdig", "-c", "spy_users"], stdout=open("sysdig_logs/sysdig_logs.txt", "w"))

# Create a FileWatcher object and start watching the file
file_watcher = FileWatcher("https://discordapp.com/api/webhooks/123456789/abcdefg", "path/to/file", "dev")
while True:
    file_watcher.check_file()
    time.sleep(10)

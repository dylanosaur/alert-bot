import hashlib
import time
import requests

class FileWatcher:
    def __init__(self, webhook_url, channel_name, file_path, check_interval=10):
        self.webhook_url = webhook_url
        self.channel_name = channel_name
        self.file_path = file_path
        self.check_interval = check_interval
        self.file_hash = None
        self.file_contents = None

    def compute_hash(self, file_path):
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            return hashlib.sha256(file_bytes).hexdigest()

    def run(self):
        while True:
            print('running')
            new_hash = self.compute_hash(self.file_path)

            if self.file_hash is None:
                print('first hash', new_hash)
                with open(self.file_path, 'r') as f:
                    self.file_contents = f.readlines()
                self.file_hash = new_hash
            elif new_hash != self.file_hash:
                print('comparing hashes', new_hash, self.file_hash)
                with open(self.file_path, 'r') as f:
                    new_contents = f.readlines()
                    print('new contents\n', new_contents)
                block_list = ["'\x1b[0m\n'"]
                new_lines = [str(x) for x in new_contents if x not in self.file_contents and len(str(x)) > 5 and 'root)' not in str(x)]

                print('new lines', new_lines)
                if len(new_lines) > 0:
                    chunks = [new_lines[i:i + 10] for i in range(0, len(new_lines), 10)]
                    for chunk in chunks:
                        content = ''.join(chunk)
                        payload = {"content": content}
                        res = requests.post(self.webhook_url, json=payload)
                        print('request response', res, res.text, res.status_code)
                self.file_hash = new_hash
                self.file_contents = new_contents

            print('sleeping', self.check_interval)
            time.sleep(self.check_interval)


if __name__ == "__main__":
    # Replace these values with your own webhook URL and Discord channel name
    WEBHOOK_URL = "https://discordapp.com/api/webhooks/1097982508395675799/kMRlaprJBYYrgFfFWZQbzoHN54UlX0ZGCzzJrRDMbjjgM9Fpqsdoih8gAYL36x3tVa_O"
    CHANNEL_NAME = "dev"

    # Path to the file to watch
    file_path = "/root/logs.txt"

    # Create a FileWatcher instance and start watching the file
    watcher = FileWatcher(WEBHOOK_URL, CHANNEL_NAME, file_path)

    watcher.run()


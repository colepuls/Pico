import requests

def read_last_devlog():
    url = "https://raw.githubusercontent.com/colepuls/devlogger/main/devlog.md"
    devlog = requests.get(url)
    devlog.raise_for_status() # check if request worked
    lines = devlog.text.splitlines(keepends=True)
    last_log = lines[-12:]
    return "".join(last_log)

if __name__ == "__main__":
    last_log = read_last_devlog()
    print(last_log)
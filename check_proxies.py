import threading
import queue
import requests

unchecked_proxies = []
q = queue.Queue()
valid_proxies = []
lock = threading.Lock()

with open("proxies.txt", "r") as file:
    proxies = file.read().split("\n")
    [unchecked_proxies.append(proxy) for proxy in proxies if proxy not in unchecked_proxies]
    [q.put(proxy) for proxy in unchecked_proxies]


def check_proxies(link, valid_file_name):
    global q
    while not q.empty():
        unchecked_proxy = q.get()
        try:
            res = requests.get(link, proxies={"http": unchecked_proxy, "https": unchecked_proxy})
        except requests.exceptions.RequestException as e:
            print(f"fail: {unchecked_proxy}")
            continue
        if res.status_code == 200:
            with lock:
                print(unchecked_proxy)
                valid_proxies.append(unchecked_proxy)
    # change the name of the file to
    with open(valid_file_name + ".txt", "w") as valid_proxies_file:
        # Writing data to a file
        for valid_proxy in valid_proxies:
            valid_proxies_file.write(valid_proxy + '\n')


# Change number of thread to process
for _ in range(5):
    threading.Thread(target=check_proxies, args=("https://www.nettruyenus.com", "valid_proxies/nettruyen_proxies",)).start()




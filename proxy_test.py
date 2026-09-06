import random
import queue
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor

PROXY_LIST = "https://raw.githubusercontent.com/proxio-io/proxy-list/main/socks5.txt"
TEST_URL = "https://api.telegram.org"
TIMEOUT = 5
WORKERS = 50

working = set()
proxy_queue = queue.Queue()
lock = threading.Lock()


def check_proxy(proxy):
    proxy = proxy.strip()
    if not proxy:
        return

    proxies = {
        "http": f"socks5h://{proxy}",
        "https": f"socks5h://{proxy}",
    }

    try:
        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)

        if r.status_code < 500:
            with lock:
                if proxy not in working:
                    working.add(proxy)
                    proxy_queue.put(proxy)
                    print(f"WORKING {proxy}")

    except Exception as e:
        print(f"DEAD {proxy}: {type(e).__name__}: {e}")


def proxy_checker():
    while True:
        try:
            text = requests.get(PROXY_LIST, timeout=10).text
            proxies = set(text.splitlines())

            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                pool.map(check_proxy, proxies)

        except Exception as e:
            print(f"LIST ERROR: {type(e).__name__}: {e}")

        # Re-check periodically
        time.sleep(30)


def display_loop():
    while True:
        with lock:
            current = list(working)

        print(f"\n--- Working proxies: {len(current)} ---")
        for proxy in current:
            print(proxy)

        time.sleep(1)


if __name__ == "__main__":
    threading.Thread(
        target=proxy_checker,
        daemon=True
    ).start()

    display_loop()

import proxy_checker
import time
import random

if __name__ == "__main__":
    proxy_checker.load_proxies()
    proxy_checker.start_thread()
    #proxy_checker.display_loop()
    while 1:
        p = proxy_checker.get_proxy()
        print(p)
        if p:
            proxy_checker.remove_proxy(p)
        time.sleep(0.1)

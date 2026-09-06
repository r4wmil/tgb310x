import proxy_checker

if __name__ == "__main__":
    proxy_checker.load_proxies()
    proxy_checker.start_thread()
    proxy_checker.display_loop()

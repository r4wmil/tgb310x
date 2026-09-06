import asyncio

import telegram
import telegram.request

import cred
import proxy_checker


def make_bot(proxy):
    request = telegram.request.HTTPXRequest(
        proxy=f"socks5h://{proxy}",
        connect_timeout=5,
        read_timeout=5,
    )
    return telegram.Bot(cred.TOKEN, request=request)


async def main():
    proxy_checker.load_proxies()
    proxy_checker.start_thread()

    offset = None

    while True:
        proxy = proxy_checker.get_proxy()

        if not proxy:
            await asyncio.sleep(1)
            continue

        try:
            bot = make_bot(proxy)

            async with bot:
                await bot.get_me()
                print(f"Bot connected through {proxy}")
                while True:
                    updates = await bot.get_updates(
                        offset=offset,
                        timeout=30,
                    )

                    for update in updates:
                        offset = update.update_id + 1

                        if update.message:
                            await bot.send_message(
                                chat_id=update.message.chat_id,
                                text=update.message.text,
                            )

        except Exception as e:
            print(f"Proxy {proxy} failed: {e}")
            proxy_checker.remove_proxy(proxy)


if __name__ == "__main__":
    asyncio.run(main())

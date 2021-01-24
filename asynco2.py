import asyncio
import aiohttp
from codetiming import Timer


async def task(page, work_queue):
    timer = Timer(text=f"Task {page} elapsed time: {{:.1f}}")
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f"Task {page} getting URL: {url}")
            timer.start()
            async with session.get(url) as response:
                t = await response.text()
            with open(f'test{page}.html', 'w', encoding='utf-8') as output_file:
                output_file.write(t)

            timer.stop()


async def main(page, profession):
    work_queue = asyncio.Queue()

    for url in [
        f'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true'
        f'&text={profession}&page={i}' for i in range(page)
    ]:
        await work_queue.put(url)

    # Запуск задач
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        for i in range(page):
            await asyncio.gather(
                asyncio.create_task(task(i, work_queue)))


if __name__ == "__main__":
    asyncio.run(main(profession='программист', page=20))

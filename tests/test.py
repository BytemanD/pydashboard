import multiprocessing
import time
import requests


from concurrent.futures import ProcessPoolExecutor

from loguru import logger

client = requests.Session()

def main():

    with ProcessPoolExecutor() as executor:
        logger.info('start')
        results = executor.map(client.get, ["http://localhost:8000/demo" for _ in range(10)])
        for result in results:
            print(result.text)
            pass
        logger.info('done')

if __name__ == '__main__':
    import multiprocessing

    multiprocessing.freeze_support()
    main()
import logging
import logging.handlers
import os
import sys
from time import sleep
import json
import requests
import argparse
import re

dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger('requests').setLevel(logging.DEBUG)

# Set up console logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Set up file logging and rotation (optional)
if (bool(os.environ.get('LOG_TO_FILE', None))):
    os.makedirs('/data/logs', exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join('/data/logs', "output.log"),
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

logger.info(f'Git Commit SHA: {os.environ.get('GIT_COMMIT_SHA', None)}')

class MyClient(object):

    classVariable = 'This is a class variable'

    titlePattern = r'<title>(?P<title_value>.*?)</title>'

    def __init__(self, some_token:str):
        self.instanceVariable = some_token

    def run(self, some_argument: str) -> None:
        logger.info(f'Starting with argument: {some_argument}')

        logger.debug(f'This is a class variable: {MyClient.classVariable}')
        logger.debug(f'This is an instance variable: {self.instanceVariable}')

        self.long_running_task()

        data = self.load_resource('data.json')
        logging.info(f'Got data: {data}')

        self.fetch_content(os.environ.get('REMOTE_EXAMPLE', None))
        
        logger.info('Finished program')

    def fetch_content(self, url: str) -> None:
        ret_code, content = self.load_remote_resource(url=url)
        if ret_code == 200:
            logger.debug(f'Got content: {content[:29]}\n......\n{content[-9:]}')
            match = re.search(self.titlePattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                logger.info(f'Title tag content: "{match.group('title_value')}"')
            else:
                logger.info("No <title> tag found.")
        else:
            logger.info(f'Could not get content...')

    def long_running_task(self) -> None:
        logger.info('Starting long running process')
        for i in range(4, 0, -1):
            logger.info(f"Run: {i}")
            sleep(1)
        logger.info('Finished running')
    
    def load_resource(self, fileName: str) -> dict[any, any]:
        logger.debug(f'Loading resource: "{fileName}"')
        filePath = os.path.join('/app/resources', fileName)
        with open(filePath, 'r') as fileHandle:
            try:
                data = json.load(fileHandle)
                logger.info(f'Loaded resource: "{fileName}"')
                return data
            except Exception as e:
                logger.error(f'Error loading "{fileName}": {e}', exc_info=True)

    def load_remote_resource(file, url: str) -> tuple[int, str]:
        response = requests.get(url)

        logger.info(f'Status Code {response.status_code} from URL: "{url}"')

        return response.status_code, response.text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Example argparse")

    parser.add_argument("--example-argument", type=str, help="An example argument", required=True)

    args = parser.parse_args()

    client = MyClient(some_token=os.environ.get('EXAMPLE_VARIABLE'))
    client.run(some_argument=args.example_argument)

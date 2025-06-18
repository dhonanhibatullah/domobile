import asyncio
from modules.logger.logger import Logger

async def main():
    logger = Logger('main', debug=True, path='log.db')

if __name__ == '__main__':
    asyncio.run(main())
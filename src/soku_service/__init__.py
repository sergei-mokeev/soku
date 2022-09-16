import asyncio
import logging
from soku_configuration import Configuration
from aiohttp.web import Application, AppRunner, TCPSite


class Service:
    def __init__(self, config: Configuration = None) -> None:
        self.__loop = asyncio.get_event_loop()
        self.__config = config or Configuration()
        self.__logger = logging.getLogger()
        self.__app = None

        log_level = logging.INFO
        if hasattr(self.config, 'LOG_LEVEL'):
            log_level = self.config.LOG_LEVEL.upper()

        logging.basicConfig(format='%(asctime)s %(levelname)-7s %(message)s', level=log_level)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self.__loop

    @property
    def config(self) -> Configuration:
        return self.__config

    @property
    def logger(self) -> logging.Logger:
        return self.__logger

    @property
    def app(self):
        return self.__app

    async def __start_aiohttp_app(self) -> None:
        if self.app:
            host, port = '0.0.0.0', 8080
            if hasattr(self.config, 'HOST'):
                host = self.config.HOST

            if hasattr(self.config, 'PORT'):
                port = self.config.PORT

            runner = AppRunner(self.app)
            await runner.setup()

            site = TCPSite(runner=runner, host=host, port=port)
            await site.start()

            self.logger.info(f'Web interface start on {host}:{port}')

    def run(self) -> None:
        if hasattr(self.config, 'NAME'):
            self.logger.info(f'Service {self.config.NAME} is started')

        else:
            self.logger.info('Service is started')

        self.loop.create_task(self.__start_aiohttp_app())

        self.loop.run_forever()

    def set_aiohttp_app(self, app: Application) -> None:
        self.__app = app

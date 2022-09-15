import asyncio
import logging
from soku_configuration import Configuration
from aiohttp.web import Application, AppRunner, TCPSite


class Service:
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)

    def __init__(self, config: Configuration) -> None:
        self.__loop = asyncio.get_event_loop()
        self.__config = config
        self.__logger = logging.getLogger()
        self.__app = None

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
        self.logger.info('Service is started')
        self.loop.create_task(self.__start_aiohttp_app())
        self.loop.run_forever()

    def set_aiohttp_app(self, app: Application) -> None:
        self.__app = app


if __name__ == '__main__':
    from aiohttp.web import json_response

    async def test(_):
        return json_response({'test': 1})

    s = Service(Configuration())
    a = Application()
    a.router.add_route('GET', '/', test)
    s.set_aiohttp_app(a)
    s.run()


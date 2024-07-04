import json



class Config:
    def __init__(self, path: str = 'config.json'):
        try:
            self.__config: dict = json.loads(path)
        except Exception as e:
            raise SystemExit(e)
        self.TOKEN = self.__config.get('TOKEN', '')
        self.HOST = self.__config.get('HOST', '')
        self.DB_HOST = self.__config.get('DB_HOST', '')
        self.DB_NAME = self.__config.get('DB_NAME', '')
        self.DB_USERNAME = self.__config.get('DB_USERNAME', '')
        self.DB_PASSWORD = self.__config.get('DB_PASSWORD', '')




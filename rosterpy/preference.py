import datetime


class Preference:
    __instance = None

    def __new__(cls):
        if Preference.__instance is None:
            Preference.__instance = object.__new__(cls)
        return Preference.__instance

    def get_usefullness(self, dienst, datum, verlauf={}):
        return 0


class RoulementPreference:
    def __init__(self, roulement, driver):
        super(RoulementPreference, self).__init__()
        self.roulement = roulement
        self.driver = driver

    def get_usefullness(self, dienst, datum, driver, verlauf={}):
        if self.roulement.get_duty(driver, datum) is dienst:
            return 1.0
        else:
            raise RoulementException


class RoulementException(Exception):
    pass


class IllPreference:
    def __init__(self, beginn, ende):
        self.beginn = datetime.datetime.strptime(beginn, '%d.%m.%Y').date()
        self.ende = datetime.datetime.strptime(ende, '%d.%m.%Y').date()

    def get_usefullness(self, dienst, datum, verlauf={}):
        raise IllException()


class IllException(Exception):
    pass

import datetime


class Preference:
    def get_usefullness(self, dienst, datum, verlauf={}):
        return 0


class RoulementPreference(Preference):
    def __init__(self, roulement, driver):
        super(RoulementPreference, self).__init__()
        self.roulement = roulement
        self.driver = driver

    def get_usefullness(self, dienst, datum, verlauf={}):
        if self.roulement.get_duty(self.driver, datum) is dienst:
            return 1.0
        raise RoulementException


class RoulementException(Exception):
    pass


class IllPreference(Preference):
    def __init__(self, beginn, ende):
        self.beginn = datetime.datetime.strptime(beginn, '%d.%m.%Y').date()
        self.ende = datetime.datetime.strptime(ende, '%d.%m.%Y').date()

    def get_usefullness(self, dienst, datum, verlauf={}):
        if dienst in ["CC", "CR"] and datum <= self.ende and datum >= self.beginn:
            return 1.0
        raise IllException()


class IllException(Exception):
    pass

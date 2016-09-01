import datetime


class Preference:
    def getUsefullness(self, dienst, datum, verlauf={}):
        if dienst.ende < dienst.beginn:
            return (0)
        return 1 - (dienst.ende - datetime.datetime.strptime("00:00:00",
                                                             "%H:%M:%S")).total_seconds() / datetime.timedelta(
                days=1).total_seconds()


class RoulementPreference(Preference):
    def __init__(self, roulement, driver):
        super(RoulementPreference, self).__init__()
        self.roulement = roulement
        self.driver = driver

    def getUsefullness(self, dienst, datum, verlauf={}):
        if self.roulement.get_duty(self.driver, datum) == dienst:
            return 1.0
        return 0.0


class IllPreference(Preference):
    def __init__(self, beginn, ende):
        self.beginn = datetime.datetime.strptime(beginn, '%d.%m.%Y').date()
        self.ende = datetime.datetime.strptime(ende, '%d.%m.%Y').date()

    def getUsefullness(self, dienst, datum, verlauf={}):
        if dienst in ["CC", "CR"] and datum <= self.ende and datum >= self.beginn:
            return 1.0
        raise WrongPreferenceException()


class WrongPreferenceException(Exception):
    pass

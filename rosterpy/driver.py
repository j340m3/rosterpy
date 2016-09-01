import datetime

from lxml import etree

import rosterpy.preference


class Driver:
    def __init__(self, nachname, vorname, preferences=[]):
        self.nachname = nachname
        self.vorname = vorname
        self.preferences = {}
        self.roulement = None
        for preference in preferences:
            for tag_shift in range((preference.ende - preference.beginn).days + 1):
                tag = (preference.beginn + datetime.timedelta(days=tag_shift))
                if tag not in self.preferences:
                    self.preferences[tag] = []
                self.preferences[tag].append(preference)

    def getPreference(self, datum):
        date = datetime.datetime.strptime(datum, '%d.%m.%Y').date()
        if date not in self.preferences:
            return rosterpy.preference.Preference()
        return self.preferences[date]

    def __repr__(self):
        return self.__class__.__name__ + " " * (7 - len(self.__class__.__name__)) + self.nachname + ", " + self.vorname


class Roulement:
    def __init__(self, date, duties, drivers=None):
        self.date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
        self._driver = {i: None for i in range(len(duties))}
        self.duties = duties
        if drivers is not None:
            for index, driver in enumerate(drivers):
                self.bind(driver, index)

    def bind(self, driver, pos):
        if pos < len(self.duties):
            if self._driver[pos] is None:
                if driver.roulement is None:
                    driver.roulement = self
                    self._driver[pos] = driver
                else:
                    raise RoulementDriverAlreadyAssignedException()
            else:
                if not self._driver[pos] == driver:
                    raise RoulementPositionAlreadyAssignedException()
        else:
            raise InvalidRoulementPositionException()

    def unbind(self, driver):
        if driver in self._driver.values():
            pos = self._get_driver_pos(driver)
            self._driver[pos] = None
            driver.roulement = None

    def _get_driver_pos(self, driver):
        for d in self._driver:
            if self._driver[d] == driver:
                return d

    def get_duty(self, driver, date):
        return self.duties[(date - self.date).days + self._get_driver_pos(driver) % len(self.duties)]


class InvalidRoulementPositionException(Exception):
    pass


class RoulementPositionAlreadyAssignedException(Exception):
    pass


class RoulementDriverAlreadyAssignedException(Exception):
    pass

class FahrerInstanceManager:
    def __init__(self, file=None):
        self.__all = []
        if file is not None:
            tree = etree.parse(file)
            for i in tree.getroot().iterchildren():
                if i.tag == "fahrer":
                    x = {"preferences": []}
                    for j in i.iterchildren():
                        if j.tag == "preferences":
                            for k in j.iterchildren():
                                kwargs = {}
                                for l in k.iterchildren():
                                    if l.tag.strip() == "policy":
                                        if l.text.strip() == "krank":
                                            pref = rosterpy.preference.KrankPreference
                                        elif l.text.strip() == "roulement":
                                            pref = rosterpy.preference.RoulementPreference
                                        else:
                                            pref = rosterpy.preference.Preference
                                    else:
                                        kwargs[l.tag] = l.text.strip()
                                x["preferences"].append(pref(**kwargs))
                        else:
                            x[j.tag] = j.text.strip()
                    self.__all.append(Driver(**x))

    def __iter__(self):
        return iter(self.__all)

    def getAll(self, tag):
        return self.__all.copy()

    def add(self, fahrer):
        self.__all.append(fahrer)

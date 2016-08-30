import datetime

from lxml import etree


class Duty:
    def __init__(self, nummer, beginn, ende):
        self.nummer = nummer
        self.beginn = datetime.datetime.strptime(beginn, "%H:%M:%S")
        self.ende = datetime.datetime.strptime(ende, "%H:%M:%S")

    def __repr__(self):
        return str(self.nummer)

    def __str__(self):
        return self.__class__.__name__ + " " * (7 - len(self.__class__.__name__)) + self.nummer + " " * (
            2 - len(str(self.nummer))) + ' von ' + self.beginn.strftime("%H:%M:%S") + " bis " + self.ende.strftime(
                "%H:%M:%S") + ": " + str(self.getArbeitsdauer()) + " (plus Pause:" + str(self.getPause()) + ")"

    def getArbeitsdauer(self):
        if self.ende - self.beginn < datetime.timedelta(days=0):
            return self.ende - self.beginn + datetime.timedelta(days=1)
        return self.ende - self.beginn

    def getPause(self):
        return datetime.timedelta(seconds=0)


class Coupe(Duty):
    def __init__(self, dienst1, dienst2):
        super(Coupe, self).__init__(dienst1.nummer, dienst1.beginn.strftime("%H:%M:%S"),
                                    dienst2.ende.strftime("%H:%M:%S"))
        self.dienst1 = dienst1
        self.dienst2 = dienst2

    def getArbeitsdauer(self):
        return (self.dienst1.ende - self.dienst1.beginn) + (self.dienst2.ende - self.dienst2.beginn)

    def getPause(self):
        return self.dienst2.beginn - self.dienst1.ende


class DienstManager:
    def __init__(self, file=None):
        wda = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        self.__all = {x: {y: {} for y in range(7)} for x in [True, False]}
        if file is not None:
            tree = etree.parse(file)
            for i in tree.getroot().iterchildren():
                if i.tag == "dienst":
                    x = {}
                    for j in i.iterchildren():
                        if j.tag == "wochentage":
                            wochentage = [k.text.strip() for k in j.iterchildren()]
                        elif j.tag == "schulzeit":
                            schulzeit = j.text.strip() in ["true", "True"]
                        else:
                            x[j.tag] = j.text.strip()
                    for wochentag in wochentage:
                        if str(int(x["nummer"]) - 50) in self.__all[schulzeit][wda.index(wochentag)].keys():
                            first = self.__all[schulzeit][wda.index(wochentag)][str(int(x["nummer"]) - 50)]
                            second = Dienst(**x)
                            self.__all[schulzeit][wda.index(wochentag)][str(int(x["nummer"]) - 50)] = Coupe(first,
                                                                                                            second)
                        else:
                            self.__all[schulzeit][wda.index(wochentag)][x["nummer"].strip()] = Dienst(**x)

    def get(self, schulzeit, wochentag, nummer):
        return self.__all[schulzeit][wochentag][nummer]

    def allMatches(self, schulzeit, wochentag):
        return self.__all[schulzeit][wochentag].keys()

    def set(self, schulzeit, wochentag, nummer, dienst):
        self.__all[schulzeit][wochentag][nummer] = dienst

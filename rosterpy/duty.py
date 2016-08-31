import datetime


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
        return self.dienst2.beginn - self.dienst1.ende + self.dienst1.getPause() + self.dienst2.getPause()


class DutyInstanceManager:
    def __init__(self, file=None):
        self._all = {x: {y: {} for y in range(7)} for x in [True, False]}
        self._dii = None

    def get(self, schulzeit, wochentag, nummer):
        return self._all[schulzeit][wochentag][nummer]

    def all_matches(self, schulzeit, wochentag):
        return self._all[schulzeit][wochentag].keys()

    def register(self, schulzeit, wochentag, dienst):
        self._all[schulzeit][wochentag][dienst.nummer] = dienst

    def import_duties(self, file):
        if self._dii is None:
            self._dii = DutyInstanceImporter()
        for schulzeit, wochentag, nummer, dienst in self._dii.import_duties(file):
            self.register(schulzeit, wochentag, nummer, dienst)


class DutyInstanceImporter:
    def __init__(self):
        self._wda = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    def import_duties(self, file):
        if file is not None:
            if file.endswith(".xml"):
                return self._xml_import(file)
            elif file.endswith((".yml", ".yaml")):
                return self._yml_import(file)

    def _xml_import(self, file):
        from lxml import etree
        tree = etree.parse(file)
        for i in tree.getroot().iterchildren():
            if i.tag == "dienst":
                x = {}
                wochentage = []
                schulzeit = None
                for j in i.iterchildren():
                    if j.tag == "wochentage":
                        wochentage = [k.text.strip() for k in j.iterchildren()]
                    elif j.tag == "schulzeit":
                        schulzeit = j.text.strip() in ["true", "True"]
                    else:
                        x[j.tag] = j.text.strip()
                for wochentag in wochentage:
                    yield (schulzeit, self._wda.index(wochentag), x["nummer"].strip(), Duty(**x))

    def _yml_import(self, file):
        pass

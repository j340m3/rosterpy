import datetime

import preference


class Fahrer:
    def __init__(self, nachname, vorname, preferences=[]):
        self.nachname = nachname
        self.vorname = vorname
        self.preferences = {}
        for preference in preferences:
            for tag_shift in range((preference.ende - preference.beginn).days + 1):
                tag = (preference.beginn + datetime.timedelta(days=tag_shift))
                self.preferences[tag] = preference

    def getTageInFolgeGearbeitet(self, datum):
        for i in range(7):
            act = datum - datetime.timedelta(days=i)
            if act in dienste and dienste[act] in ["CC", "CR"]:
                return i
        return 0

    def getPreference(self, date):
        if date not in self.preferences:
            return preference.Preference()
        return self.preferences[date]

    def __repr__(self):
        return self.__class__.__name__ + " " * (7 - len(self.__class__.__name__)) + self.nachname + ", " + self.vorname


class RoulementFahrer(Fahrer):
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
                                            pref = preference.KrankPreference
                                        elif l.text.strip() == "roulement":
                                            pref = preference.RoulementPreference
                                        else:
                                            pref = preference.Preference
                                    else:
                                        kwargs[l.tag] = l.text.strip()
                                x["preferences"].append(pref(**kwargs))
                        else:
                            x[j.tag] = j.text.strip()
                    self.__all.append(Fahrer(**x))

    def __iter__(self):
        return iter(self.__all)

    def getAll(self, tag):
        return self.__all.copy()

    def add(self, fahrer):
        self.__all.append(fahrer)

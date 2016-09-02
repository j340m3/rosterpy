import datetime
from concurrent.futures import ThreadPoolExecutor

import rosterpy.preference as preference


class Kalender:
    def __init__(self, fahrermanager):
        self.fahrermanager = fahrermanager
        self.kalender = {}
        self.__life = {fahrer: 0 for fahrer in fahrermanager.getAll(None)}
        self.__choice = {fahrer: 0 for fahrer in fahrermanager.getAll(None)}

    def getWorkInARow(self, datum, fahrer):
        if datum in self.kalender:
            if fahrer in self.kalender[datum]:
                res = 1
                while (datum - datetime.timedelta(days=res)) in self.kalender and self.kalender[
                    (datum - datetime.timedelta(days=res))]:
                    res += 1
                return res
            else:
                return 0
        return 0

    def getTag(self, datum):
        if datum not in self.kalender:
            self.kalender[datum] = {f: None for f in self.fahrermanager.getAll(datum)}
        return self.kalender[datum]

    def setValue(self, datum, fahrer, value):
        if datum not in self.kalender:
            self.kalender[datum] = {}
        else:
            if fahrer in self.kalender[datum]:
                self.__life[fahrer] -= self.__calc_life_day(fahrer, datum)
        self.kalender[datum][fahrer] = value
        self.__life[fahrer] += self.__calc_life_day(fahrer, datum)

    def getValue(self, datum, fahrer):
        if datum in self.kalender:
            if fahrer in self.kalender[datum]:
                return self.kalender[datum][fahrer]
        return None

    def getChoice(self, fahrer):
        return self.__choice[fahrer]

    def alterChoice(self, fahrer, value, cleanup=0):
        self.__choice[fahrer] += value
        if cleanup:
            if min(self.__choice.values()) >= cleanup:
                delta = min(self.__choice.values())
                for fahrer in self.__choice:
                    self.__choice[fahrer] -= delta

    def getGlobalAverage(self, f):
        summe = 0
        anzahl = 0
        for tag in self.kalender:
            for fahrer in self.kalender[tag]:
                try:
                    summe += f(self.kalender[tag][fahrer])
                except:
                    raise
                else:
                    anzahl += 1
        return 1.0 * summe / anzahl

    def getFahrerAverage(self, f, fahrer):
        summe = 0
        anzahl = 0
        for tag in self.kalender:
            try:
                summe += f(self.kalender[tag][fahrer])
            except:
                raise
            else:
                anzahl += 1
        if anzahl:
            return 1.0 * summe / anzahl
        return 1

    def getLifeBalance(self, fahrer):
        return self.__life[fahrer]

    def __calc_life_day(self, fahrer, tag):
        if fahrer in self.kalender[tag]:
            dienst = self.kalender[tag][fahrer]
            if dienst.ende < dienst.beginn:
                return (dienst.beginn - dienst.ende).seconds
            else:
                return (dienst.beginn - datetime.datetime.min).seconds + (
                datetime.datetime(1, 1, 1) - dienst.ende).seconds
        else:
            if isinstance(fahrer.getPreference(tag), preference.IllPreference):
                return 36 * 3600
            else:
                return 24 * 3600

    def getGlobalLifeBalanceAverage(self):
        return sum([self.getLifeBalance(fahrer) for fahrer in self.fahrermanager.getAll(None)]) / len(
                self.fahrermanager.getAll(None))

    def getGlobalLifeBalance(self):
        return sum([self.getLifeBalance(fahrer) for fahrer in self.fahrermanager.getAll(None)])

    def __str__(self):
        maxname = len(str(self.fahrermanager.getAll(min(self.kalender.keys()))))
        out = " " * maxname + "|"


class Schulzeitenkalender:
    def isSchulzeit(self, datum):
        return False


class Dienstplan:
    def __init__(self, fahrermanager, history, start, ende):
        self.fahrermanager = fahrermanager
        self.kalender = Kalender(fahrermanager)
        self.start = start
        self.ende = ende
        self.history = history

    def setDienst(self, datum, fahrer, dienst):
        # check correct weekday
        # check tage in folge
        # check n stunden schlaf
        self.kalender.setValue(datum, fahrer, dienst)

    def getDienst(self, datum, fahrer):
        return self.kalender.getValue(datum, fahrer)


class DienstplanManager:
    def __init__(self, dienstmanager, fahrermanager, history, schulzeitenkalender, start, ende):
        self.dienstmanager = dienstmanager
        self.fahrermanager = fahrermanager
        self.history = history
        self.schulzeitenkalender = schulzeitenkalender
        self.start = start
        self.ende = ende
        self.__executor = ThreadPoolExecutor(max_workers=1)

    def getProb(self):
        zuweisung = {}
        for tag_shift in range((self.ende - self.start).days + 1):
            tag = (self.start + datetime.timedelta(days=tag_shift))
            zuweisung[tag] = {}
            isSchultag = self.schulzeitenkalender.isSchulzeit(tag)
            scorecard = {}
            res = {fahrer: self.__executor.submit(self.getFahrerScore, tag, isSchultag, fahrer) for fahrer in
                   self.fahrermanager.getAll(tag)}
            for f in res:
                fahrer_scorecard = res[f].result()
                for score in fahrer_scorecard:
                    if score not in scorecard:
                        scorecard[score] = fahrer_scorecard[score]
                    else:
                        scorecard[score] += fahrer_scorecard[score]
            uebrig_dienste = [self.dienstmanager.get(isSchultag, tag.weekday(), dienstnr) for dienstnr in
                              self.dienstmanager.allMatches(isSchultag, tag.weekday())]
            uebrig_fahrer = self.fahrermanager.getAll(tag)
            while len(uebrig_dienste) > 0 and len(uebrig_fahrer) > 0 and len(scorecard) > 0:
                maximum = max(scorecard.keys())
                l = scorecard[maximum]
                for fahrer, dienst in l:
                    if (dienst in uebrig_dienste):
                        if (fahrer in uebrig_fahrer):
                            zuweisung[tag][fahrer] = dienst
                            uebrig_fahrer.remove(fahrer)
                            uebrig_dienste.remove(dienst)
                            self.history.setValue(tag, fahrer, dienst)
                    else:
                        if (fahrer in uebrig_fahrer):
                            self.history.alterChoice(fahrer, 1)
                scorecard.pop(maximum)
            if len(uebrig_dienste) > 0:
                raise Exception(uebrig_dienste)
        return zuweisung

    def getFahrerScore(self, tag, isSchultag, fahrer):
        scorecard = {}
        if self.history.getWorkInARow(tag, fahrer) <= 8:
            for dienstname in self.dienstmanager.allMatches(isSchultag, tag.weekday()):
                dienst = self.dienstmanager.get(isSchultag, tag.weekday(), dienstname)
                last = self.history.getValue((tag - datetime.timedelta(days=1)), fahrer)
                """
                if last.beginn > last.ende:
                  sleeptime =
                else:
                  sleeptime = (
                """
                try:
                    score = self.getScore(tag, fahrer, dienst)
                    if score not in scorecard:
                        scorecard[score] = []
                    scorecard[score].append((fahrer, dienst))
                except preference.WrongPreferenceException:
                    pass
                except WorkInARowException:
                    pass
        return scorecard

    def getScore(self, tag, fahrer, dienst):
        # return(1-(self.history.getLifeBalance(fahrer)/max(1,self.history.getGlobalLifeBalance())))
        # return fahrer.getPreference(tag).getUsefullness(dienst,tag,self.history)*(1-(self.history.getLifeBalance(fahrer)/max(1,self.history.getGlobalLifeBalance())))
        return fahrer.getPreference(tag).getUsefullness(dienst, tag, self.history) * max(self.history.getChoice(fahrer),
                                                                                         1)

    def getHistory(self):
        return self.history


class WorkInARowException(Exception):
    pass

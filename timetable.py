import random as rand
from data import *

class Timetable(Data):
    def __init__(self,periodsPerDay,noOfDays):
        super().__init__(periodsPerDay,noOfDays)
        self.periodsPerDay = periodsPerDay
        self.noOfDays = noOfDays

    def assignSpecialPeriods(self):
        
        pass

    def assignSubjects(self):
        week = self.table
        repeatedSubjects = []
        
        for dayNum in range(len(week)):
            day = week[dayNum]
            possibleIndex = [x for x in range(0,self.periodsPerDay)]
            
            for periodRef in self.periods:
                noOfPeriod = rand.choice([periodRef['minPerDay'][0]]*periodRef['minPerDay'][1] + [periodRef['maxPerDay'][0]]*periodRef['maxPerDay'][1])
                
                if periodRef['subject'] in repeatedSubjects:
                    noOfPeriod = 1
                
                for x in range(noOfPeriod):
                    index = rand.choice(possibleIndex)
                    possibleIndex.remove(index)
                    
                    week[dayNum][index] = periodRef["subject"]
                
                if noOfPeriod > 1:
                    repeatedSubjects.append(periodRef['subject'])
                    # print(periodRef['subject'])
        self.table = week

    def printTimetable(self):
        for x in self.table:
            print(x)

    def generateTimetable(self):
        # print(self.teachers[0])

        # self.createEmptyFiles()
        self.createTable()
        
        self.assignSpecialPeriods()
        # self.assignSubjects()

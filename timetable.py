import random as rand
from data import *

class Timetable(Data):
    def __init__(self,periodsPerDay,noOfDays):
        super().__init__(periodsPerDay,noOfDays)
        self.periodsPerDay = periodsPerDay
        self.noOfDays = noOfDays

    # Assigning special periods like pe
    def assignSpecialPeriods(self):
        possibleDict = {x:2 for x in range(0,self.periodsPerDay)}
        possibleIndex = []

        for x in possibleDict:
            possibleIndex.extend([x]*possibleDict[x])

        for clas in self.data:
            day = rand.randint(0,self.noOfDays-1)
            
            index = rand.choice(possibleIndex)
            self.data[clas][day][index] = "PE"
            possibleIndex.remove(index)
            pass

    # Assign period to the teacher according to the classes she/he teaches
    def assignSubjects(self):
        for day in range(0,self.noOfDays):
            self.getPossibleIndexes()
            for teacher in self.teachers:
                pickedClass = rand.choice(teacher["classes"])
                pickedPeriod = rand.choice(self.possibleIndexes[pickedClass][day])

                self.data[pickedClass][day][pickedPeriod] = teacher['subjects'][0]
                self.possibleIndexes[pickedClass][day].remove(pickedPeriod)
                print(self.possibleIndexes[pickedClass][day])
                pass


    # Print the time table along with the classes and days
    def printTimetable(self):
        days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'] 
        for x in self.data:
            print("--",x,"--")
            for i,y in enumerate(self.data[x]):
                print(days[i],y)
            print("\n")

    # Main Generating Function
    def generateTimetable(self):
        # print(self.teachers[0])

        self.assignSpecialPeriods()
        self.assignSubjects()

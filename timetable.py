import random as rand
from data import *
import copy

class Timetable(Data):
    def __init__(self,periodsPerDay,noOfDays):
        super().__init__(periodsPerDay,noOfDays)
        self.periodsPerDay = periodsPerDay
        self.noOfDays = noOfDays

    def assignPEPeriod(self):
        classes = self.getListOfSections().copy()
        temp = []

        for x in range(0,self.periodsPerDay):
            temp.extend([x])

        possibleIndex = [temp[:] for x in range(0,self.noOfDays)]
        possibleIndex = copy.deepcopy(possibleIndex)

        while len(classes) > 0:
            choice = rand.choice(classes)
            print(choice)
            classes.remove(choice)
            pass

    # Assigning special periods like pe
    def assignSpecialPeriods(self):
        self.assignPEPeriod()

    # Assign period to the teacher according to the classes she/he teaches
    def assignSubjectsAccTeachers(self):
        for day in range(0,self.noOfDays):
            self.getPossibleIndexes()
            for teacher in self.teachers:
                pickedClass = rand.choice(teacher["classes"])
                pickedPeriod = rand.choice(self.possibleIndexes[pickedClass][day])

                # self.setPeriod(pickedClass,day,pickedPeriod,teacher['subjects'][0],teacher['name'])
                self.possibleIndexes[pickedClass][day].remove(pickedPeriod)
                pass

    # Assign subject for each class according to all the available subjects
    def assignSubjectsAccPeriods(self):
        for day in range(0,self.noOfDays):
            self.getPossibleIndexes()
            for clas in self.classes:
                for pickedClass in self.getListOfSections(clas['grade'],clas['maxSection']):
                    for period in self.periods:
                        pickedPeriod = rand.choice(self.possibleIndexes[pickedClass][day])

                        self.data[pickedClass][day][pickedPeriod] = period['subject']
                        self.possibleIndexes[pickedClass][day].remove(pickedPeriod)
                        pass
    
    # Assign period to the teacher according to the subject available and the teachers
    def assignSubjectsHybrid(self):
        for day in range(0,self.noOfDays):
            self.getPossibleIndexes()
            for clas in self.classes:
                for pickedClass in self.getListOfSections(clas['grade'],clas['maxSection']):
                    for subject in self.periods:
                        pickedPeriod = rand.choice(self.possibleIndexes[pickedClass][day])
                        print(pickedPeriod)
                        print(self.data[pickedClass][day][pickedPeriod])
                        # self.possibleIndexes[pickedClass][day].remove(pickedPeriod)
                        pass

            # for teacher in self.teachers:
            #     pickedClass = rand.choice(teacher["classes"])
            #     pickedPeriod = rand.choice(self.possibleIndexes[pickedClass][day])

            #     self.data[pickedClass][day][pickedPeriod] = teacher['subjects'][0]
            #     self.possibleIndexes[pickedClass][day].remove(pickedPeriod)
            #     pass

    # Print the time table along with the classes and days
    def printTimetable(self,plain = False):
        """Prints the Generated Time Table.
        Args:
            plain::bool
                Wheather to print plain or with only the subjects
        """
        days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'] 
        for x in self.data:
            print("--",x,"--")
            temp = []
            if not plain:
                for i,y in enumerate(self.data[x]):
                    for z in y:
                        try:
                            temp.append(z['subject'])
                        except:
                            temp.append(z)
                    print(days[i],temp," -",temp.count(""))
                    temp = []
            else:
                for x in self.data:
                    for y in self.data[x]:
                        print(y," -",temp.count(""))
                    print()
            print("\n")

    # Main Generating Function
    def generateTimetable(self):
        # print(self.teachers[0])

        self.assignSpecialPeriods()
        # self.assignSubjectsAccTeachers()
        self.getPossibleIndexes()
        print(self.setPeriod('11A',0,0,'pe','Karthik'))
import random as rand
from data import *
import copy

class Timetable(Data):
    def __init__(self,periodsPerDay,noOfDays):
        super().__init__(periodsPerDay,noOfDays)

    # Assign skill period for a specific grade together
    def assignSkillPeriod(self):
        classes = self.getListClasses().copy()
        for period in self.skillSubjectPeriod:
            self.skillDay = [False for x in range(0,self.noOfDays)]
            for x in range(period['periodsPerWeek']):
                choosenPeriod = rand.choice(self.getSkillAcailablity())
                for section in self.getListOfSections(period['grade']):
                    self.data[section][choosenPeriod[0]][choosenPeriod[1]] = period['subject']
                    self.skillAvailability[choosenPeriod[0]][choosenPeriod[1]] = True
                    self.skillDay[choosenPeriod[0]] = True
                    for teacher in period['teachers']:
                        self.teacherAvailablity[teacher][self.days[choosenPeriod[0]]][choosenPeriod[1]] = section

    def assignPEPeriod(self):
        for subject in self.specialPeriods:
            for classes in subject['classes']:
                choosenPeriod = rand.choice(self.removeOccupiedPE(self.getFullGroundAvailablity(False),classes))
                for section in classes:
                    if self.data[section][choosenPeriod[0]][choosenPeriod[1]]:
                        raise Exception("Place Already taken by Skill, if this come then -4hrs by debugging")
                    self.data[section][choosenPeriod[0]][choosenPeriod[1]] = subject['subject']
                    self.teacherAvailablity[subject['teacher']][self.days[choosenPeriod[0]]][choosenPeriod[1]] = section
                    self.addGroundPeriod(choosenPeriod[0],choosenPeriod[1],2)

    # Assigning special periods like pe
    def assignSpecialPeriods(self):
        self.assignSkillPeriod()
        self.assignPEPeriod()
    
    # Print the time table along with the classes and days
    def printTimetable(self,plain = False):
        """Prints the Generated Time Table.
        Args:
            plain::bool
                Wheather to print plain or with only the subjects
        """
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
                    print(self.days[i],temp," -",temp.count(""))
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
        # self.getPossibleIndexes()
        # print(self.setPeriod('11A',0,0,'pe','Karthik'))
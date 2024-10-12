import random as rand
from data import *
import copy

class Timetable(Data):
    def __init__(self,periodsPerDay,noOfDays):
        super().__init__(periodsPerDay,noOfDays)

    # Assign skill period for a specific grade together
    def assignSkillPeriods(self):
        classes = self.getListClasses().copy()
        for period in self.skillSubjectPeriods:
            self.skillDay = [False for x in range(0,self.noOfDays)]
            for x in range(period['periodsPerWeek']):
                choosenPeriod = rand.choice(self.getSkillAcailablity())
                for section in self.getListOfSections(period['grade']):
                    self.data[section][choosenPeriod[0]][choosenPeriod[1]] = period['subject']
                    self.skillAvailability[choosenPeriod[0]][choosenPeriod[1]] = True
                    self.skillDay[choosenPeriod[0]] = True
                for teacher in period['teachers']:
                    self.teacherAvailablity[teacher][self.days[choosenPeriod[0]]][choosenPeriod[1]] = str(period['grade'])+'Skill'

    # Teacher thinky, (Availablity)
    def assignPEPeriod(self):
        """
        Assign PE periods too the 
        """
        for subject in self.PEPeriods:
            for classes in subject['classes']:
                # self.removeOccupiedPE() also removes the Teachers Coinciding
                choosenPeriod = rand.choice(self.removeOccupiedPE(self.getFullGroundAvailablity(False),classes,subject['teacher']))
                for section in classes:
                    if self.data[section][choosenPeriod[0]][choosenPeriod[1]]:
                        raise Exception("Place Already taken by Skill, if this come then -4hrs by debugging")
                    self.data[section][choosenPeriod[0]][choosenPeriod[1]] = subject['subject']
                    self.teacherAvailablity[subject['teacher']][self.days[choosenPeriod[0]]][choosenPeriod[1]] = section
                    self.addGroundPeriod(choosenPeriod[0],choosenPeriod[1],2)

    def assignLabPeriods(self):
        """
        Assign lab periods for practical classes considering availability of labs, teachers, and classes.
        """
        for practical in self.practicalPeriods:
            for classes in practical['classes']:
                for lab in practical['lab']:
                    available = self.getLabAvailability(lab)
                    for teacher in classes[1]:
                        available = self.removeLabTeacherCoinsiding(available,teacher)
                    for clas in classes[0]:
                        available = self.removeLabClassCoinsiding(available,clas)
                    available = self.removeLabSuccessive(available,practical['continuously'])
                    choosenPeriod = rand.choice(available)
                for clas in classes[0]:
                    for con in range(practical['continuously']):
                        self.data[clas][choosenPeriod[0]][choosenPeriod[1]+con] = practical['name']
                        for lab in practical['lab']:
                            self.labAvailability[lab][choosenPeriod[0]][choosenPeriod[1]+con] = True
                        for teacher in classes[1]:
                            self.teacherAvailablity[teacher][self.days[choosenPeriod[0]]][choosenPeriod[1]+con] = clas

    
    # Assigning special periods like pe
    def assignSpecialPeriods(self):
        self.assignSkillPeriods()
        self.assignPEPeriod()
        self.assignLabPeriods()
    
    def assignNormalPeriods(self):
        # Need to change this to a while Loop
        for y in range(2):
            for day in range(self.noOfDays):
                periods = self.periods
                rand.shuffle(periods)
                for period in periods:
                    for clas in period['classes']:
                        available = self.getAvailablePeriodsOfDay(clas,day)
                        teacher = self.getPossibleTeacher(clas,period['subject'])
                        available = self.removeTeacherNotAvailable(available,day,teacher)
                        try:
                            choosenPeriod = rand.choice(available)
                            self.data[clas][day][choosenPeriod] = period['subject']
                            self.teacherAvailablity[teacher][self.days[day]][choosenPeriod] = clas
                        except:
                            pass
            
                    

    # Print the time table along with the classes and days
    def printTimetable(self,plain = False):
        """
        Prints the Generated Time Table.
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
                    print(self.days[i],temp,"-",temp.count(""))
                    temp = []
            else:
                for x in self.data:
                    for y in self.data[x]:
                        print(y," -",temp.count(""))
                    print()
            print("\n")

    # Main Generating Function
    def generateTimetable(self):
        self.assignSpecialPeriods()
        self.assignNormalPeriods()
        print(self.getAvailableTeacher("Thu",8))

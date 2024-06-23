import csv
import os
import copy

class Data:
    def __init__(self,periodsPerDay,noOfDays):
        self.noOfDays = noOfDays
        self.periodsPerDay = periodsPerDay

        self.maxClassesInGround = 2
        

        self.days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']

        # Should get rid of this
        self.emptyPossiblePeriods = [x for x in range(0,periodsPerDay)]
        self.emptyPossibleDays = [x for x in range(0,self.noOfDays)]

        self.possibleIndexes = {}
    
        # List of all classes in the school
        self.classes = [
            # {'grade':7,'maxSection':'E'},
            # {'grade':8,'maxSection':'E'},
            # {'grade':9,'maxSection':'E'},
            # {'grade':10,'maxSection':'E'},
            {'grade':11,'maxSection':'E'},
            {'grade':12,'maxSection':'E'}
        ]

        # Data for creating the Time table
        self.teacherAvailablity = {
            'Karuna':{},
            'Reshma':{},
            'Shafeela':{},
            'Shrithi':{},
            'Krithika':{},
            'Vidhya':{},
            'Anuradha':{},
            'Lida':{},
            'Deepa':{},
            'Judith':{},
            'Shibu':{},
            'Anitha':{},
            'Irine':{},
            'Ameen':{},
            'Karthik':{},
            'Ashley':{},
            'Kavitha':{},
            'Ruskin':{},
        }

        # self.teachers = [
        #     {'name':'Karuna','subjects':['math'],'classes':['11A','11B','11C'],'periodsPerDay':5},
        #     {'name':'Reshma','subjects':['math'],'classes':['11A','11B','11C'],'periodsPerDay':5},

        #     {'name':'Shafeela','subjects':['chem'],'classes':['11A','11B'],'periodsPerDay':5},
        #     {'name':'Shrithi','subjects':['chem'],'classes':['11A','11C'],'periodsPerDay':5},
        #     {'name':'Krithika','subje   cts':['chem'],'classes':['11B','11C'],'periodsPerDay':5},

        #     {'name':'Vidhya','subjects':['phys'],'classes':['11A','11B'],'periodsPerDay':5},
        #     {'name':'Anuradha','subjects':['phys'],'classes':['11B','11C'],'periodsPerDay':5},
        #     {'name':'Lida','subjects':['phys'],'classes':['11A','11C'],'periodsPerDay':5},

        #     {'name':'Deepa','subjects':['comp'],'classes':['11A'],'periodsPerDay':5},
        #     {'name':'Judith','subjects':['comp'],'classes':['11A'],'periodsPerDay':5},
        #     {'name':'Shibu','subjects':['comp'],'classes':['11C'],'periodsPerDay':5},

        #     {'name':'Anitha','subjects':['engl'],'classes':['11A','11B'],'periodsPerDay':5},
        #     {'name':'Irine','subjects':['engl'],'classes':['11C'],'periodsPerDay':5},
        # ]

        self.specialPeriods = [
            # Create it so that it assignes according to the period taken py the pe teachers
            {'teacher':'Karthik','subject':'_PE_','classes':[['11A','11B'],['11C','11D','11E']],'periodsPerDay':5},
            {'teacher':'Ameen','subject':'_PE_','classes':[['12A','12B'],['12C','12D','12E']],'periodsPerDay':5},
        ]

        self.skillSubjectPeriod = [
            {'teachers':['Ameen','Ashley','Kavitha','Ruskin','Karthik'],'subject':'SKIL','grade':11,'periodsPerWeek':3},
            {'teachers':['Ameen','Ashley','Kavitha','Ruskin','Karthik'],'subject':'SKIL','grade':12,'periodsPerWeek':3}
        ]   

        self.periods = [
            {'subject':'math','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':7,'repeatPerWeek':1},
            {'subject':'chem','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':7,'repeatPerWeek':1},
            {'subject':'phys','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6,'repeatPerWeek':1},
            {'subject':'comp','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6,'repeatPerWeek':1},
            {'subject':'engl','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6,'repeatPerWeek':1},
        ]

        self.practicals = [
            {'subject':'comp','contCount':2,'weekly':1},
            {'subject':'chem/phy','contCount':2,'weekly':1},
        ]

        # self.specialPeriods = [
        #     {'subject':'pe','type':'extra','minPerDay':[1,4],'maxPerDay':[1,0],'noPerWeek':1,'atSameTime':2},
        # ]

        # Keep track of of Ground Availability to Assign PT Periods
        self.groundAvailability = [[0 for x in range(0,periodsPerDay)] for x in range(0,noOfDays)]
        self.skillDay = [False for x in range(0,noOfDays)]
        self.skillAvailability = [[False for x in range(0,periodsPerDay)] for x in range(0,noOfDays)]
        
        # print(self.groundAvalablity)

        self.data = {}

        # Initialization of Variables
        self.resetTeacherPeriods()
        self.createEmptyData()

    # Creates the empty data in the beginning
    def createEmptyData(self):
        table = []
        # print(temp)
        for dayNum in range(1,self.noOfDays+1):
            table.append(["" for x in range(self.periodsPerDay)])

        for clas in self.classes:
            for div in range(65,ord(clas['maxSection'])+1):
                self.data[str(clas['grade'])+str(chr(div))] = copy.deepcopy(table)

    # Reset the teachers Periods for each teacher for all the days  
    def resetTeacherPeriods(self):
        for teacher in self.teacherAvailablity:
            for day in range(self.noOfDays):
                self.teacherAvailablity[teacher][self.days[day]] = [False for x in range(0,self.periodsPerDay)]

    # Returns all the teachers available in a given subject, class and period
    def getAvailableTeachers(self,sub,clas,period):
        teachers = self.getSubjectTeachers(sub,clas)[:]
        temp = teachers[:]
        for x,teacher in enumerate(teachers):
            if period not in teacher['availablePeriods']:
                temp.pop(x)
        return temp

    # Returns all the teachers teaching a specific subject
    def getSubjectTeachers(self,sub,clas):
        tempTeachers = []
        for teacher in self.teachers:
            if sum in teacher['subjects'] and clas in teacher['classes']:
                tempTeachers.append(teacher)
        return tempTeachers

    def getSkillAcailablity(self):
        temp = []
        for dayIndex,day in enumerate(self.skillAvailability):
            if not self.skillDay[dayIndex]:
                for periodIndex,isOccupied in enumerate(day):
                    if not isOccupied:
                        temp.append((dayIndex,periodIndex))
        return temp

    def removeOccupiedPE(self,lst,classes):
        temp = []
        flag = 0
        for item in lst:
            flag = 0
            for sec in classes:
                if self.data[sec][item[0]][item[1]] == "":
                    flag = 1
            if flag:
                temp.append(item)
        return(temp)

    def getFullGroundAvailablity(self,only = "None"):
        temp = []

        if only == "None":
            for dayIndex,day in enumerate(self.groundAvailability):
                for periodIndex,noOfClasses in enumerate(day):
                    temp.append((dayIndex,periodIndex,noOfClasses))
            return temp

        for dayIndex,day in enumerate(self.groundAvailability):
            for periodIndex,noOfClasses in enumerate(day):
                if only == False and noOfClasses < self.maxClassesInGround:
                    temp.append((dayIndex,periodIndex,noOfClasses))
                elif only == True and noOfClasses == self.maxClassesInGround:
                    temp.append((dayIndex,periodIndex,noOfClasses)) 
        return temp 
    
    def addGroundPeriod(self,dayIndex,periodIndex,by=1):
        self.groundAvailability[dayIndex][periodIndex] += by

    def setGroundAvailability(self,dayIndex,periodIndex,to = 1):
        self.groundAvailability[dayIndex][periodIndex] = to
    
    # Returns a List of Empty Spots in the time table
    # Its crying for optimization need to optimize it
    def getPossibleIndexes(self):
        tempDict = {}
        tempWeek = []
        tempDay = []
        for clas in self.data:
            tempWeek = []
            for j,day in enumerate(self.data[clas]):
                tempDay = []
                for i,period in enumerate(self.data[clas][j]):
                    if period == "":
                        tempDay.append(i)
                tempWeek.append(tempDay.copy())

            tempDict[clas] = tempWeek.copy()
        self.possibleIndexes = tempDict
        return tempDict

    # Create Empty files to save it later
    def createEmptyFiles(self):
        # if os.path.exists('Classes'):
        #     os.remove('Classes')

        os.mkdir('Classes')
        for x in self.classes:
            os.chdir('Classes')
            os.mkdir(str(x['grade'])+"Grade")
            os.chdir('../')

            for y in range(65,ord(x['maxSection'])+1):
                filePath = "Classes/"+str(x['grade'])+"Grade/"+str(x['grade'])+str(chr(y))+".csv"

                with open(filePath, 'w', newline='') as file:
                    writer = csv.writer(file)
                    row_list = [
                        ["name", "age", "country"], 
                        ["Oladele Damilola", "40", "Nigeria"], 
                        ["Alina Hricko", "23" "Ukraine"], 
                        ["Isabel Walter", "50" "United Kingdom"],
                    ]
                    writer.writerow(row_list)
    # Create a list and return a list of all classes and sections together in the form of a string in list, ie.['11A','11B','12A','12B'].
    
    def getListClasses(self):
        classes = []
        for clas in self.classes:
            for div in range(65,ord(clas['maxSection'])+1):
                classes.append(str(clas['grade'])+str(chr(div)))
        return classes

    # Create a list and return a list of grade and sections together in the form of a string in list for a specific grade, ie.['11A','11B'].
    def getListOfSections(self,grade):
        tempList = []
        for gradeList in self.classes:
            if gradeList['grade'] == grade:
                for div in range(65,ord(gradeList['maxSection'])+1):
                    pickedClass = str(grade)+str(chr(div))
                    tempList.append(pickedClass)
        return tempList
    
    # Check is a specific teacher is available during a given period and class
    def isTeacherAvailable(self,teacher,sub,clas,period):
        teachers = self.getAvailableTeachers(sub,clas,period)
        for teach in teachers:
            if teach['name'] == teacher:
                return True
        return False
    
    # Assign a period to a teacher
    def setPeriod(self,clas,day,period,subject,teacher,check=True):
        if check:
            if self.isTeacherAvailable(teacher,subject,clas,period):
                self.data[clas][day][period] = {'teacher':teacher,'subject':subject}
                for x,teach in enumerate(self.teachers):
                    if teach['name'] == teacher:
                        self.teachers[x]['availablePeriods'].remove(period)
                        break
                return True
            else:
                return False
        else:
            self.data[clas][day][period] = {'teacher':teacher,'subject':subject}
            for x,teach in enumerate(self.teachers):
                    if teach['name'] == teacher:
                        print(self.teachers[x]['availablePeriods'])
                        self.teachers[x]['availablePeriods'].remove(period)
                        break
            return True
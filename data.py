import mysql.connector as sql
import csv
import os
import copy

class MySqlConnector:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'Lmao'
        
        self.DB = sql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database='timetable'
        )
        self.cursor = self.DB.cursor()
    
    def getConfig(self):
        self.cursor.execute("SELECT fieldName, fieldValue FROM config")
        result = self.cursor.fetchall()
        config_data = {row[0]: int(row[1]) for row in result}
        return config_data

    def updateOutput(self,data):
        self.cursor.execute('''DROP TABLE ClassSchedule''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ClassSchedule(
            ID INTEGER PRIMARY KEY AUTO_INCREMENT,
            ClassName TEXT NOT NULL,
            Day TEXT NOT NULL,
            Period INTEGER NOT NULL,
            Subject TEXT NOT NULL
        )''')
        self.DB.commit()

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        index = 1
        for class_name, weekly_schedule in data.items():
            for day_index, day_schedule in enumerate(weekly_schedule):
                day = days[day_index]
                for period, subject in enumerate(day_schedule, start=1):
                    # print(f"INSERT INTO ClassSchedule VALUES ({index},'{class_name}', '{day}', {period}, '{subject if subject else "idk"}')")
                    self.cursor.execute(f"INSERT INTO ClassSchedule VALUES ({index},'{class_name}', '{day}', {period}, '{subject if subject else "idk"}')")
                    index += 1
        self.DB.commit()
        self.DB.close()


class Data(MySqlConnector):
    def __init__(self,periodsPerDay,noOfDays):
        super().__init__()
        cofigData = self.getConfig()

        self.noOfDays = cofigData['noOfDays']
        self.periodsPerDay = cofigData['periodsPerDay']

        self.maxClassesInGround = cofigData['maxClassesInGround']

        self.days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        self.ordinals = ['First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eighth','Ninth','Tenth']

        # Should get rid of this
        self.emptyPossiblePeriods = [x for x in range(0,periodsPerDay)]
        self.emptyPossibleDays = [x for x in range(0,self.noOfDays)]

        self.possibleIndexes = {}
    
        # List of all classes in the school
        self.classes = [
            {'grade':11,'maxSection':'E'},
            {'grade':12,'maxSection':'E'},
        ]
        
        self.teachers = ['Karuna','Reshma','Moses','Shafeela','Shruthi','Krithika','Vidhya','Anuradha','Lida','Vijitha','Ashwathy','Deepa','Judith','Shibu','Anitha','Irine','Ameen','Karthik','Ashley','Kavitha','Ruskin']
        self.labs = ['Chem','Phy','Bio','Comp',"SComp"]

        # Data for creating the Time table
        self.teacherAvailablity = {}

        self.teacherDetails = [
            {'name':'Karuna','subject':'Math','classes':['11A','12A']},
            {'name':'Reshma','subject':'Math','classes':['11B','12B']},
            {'name':'Moses','subject':'Math','classes':['11C','12C']},

            {'name':'Shafeela','subject':'Chem','classes':['11A','12B']},
            {'name':'Shruthi','subject':'Chem','classes':['11B','12A']},
            {'name':'Krithika','subject':'Chem','classes':['11C','12C']},

            {'name':'Vidhya','subject':'Phy','classes':['11A','12C']},
            {'name':'Anuradha','subject':'Phy','classes':['11B','12A']},
            {'name':'Lida','subject':'Phy','classes':['11C','12B']},

            {'name':'Deepa','subject':'Comp','classes':['11A','12A']},
            {'name':'Judith','subject':'Comp','classes':['11B','11C']},
            {'name':'Shibu','subject':'Comp','classes':['12B','12C']},

            {'name':'Ashwathy','subject':'Bio','classes':['11B','12B']},
            {'name':'Vijitha','subject':'Bio','classes':['11C','12C']},

            {'name':'Anitha','subject':'Eng','classes':['11A','12A','11B','12B']},
            {'name':'Irine','subject':'Eng','classes':['11C','12C']}

        ]

        self.PEPeriods = [
            # Create it so that it assignes according to the period taken py the pe teachers
            {'teacher':'Karthik','subject':'PE','classes':[['11A','11B'],['11C','11D','11E']],'periodsPerDay':5},
            {'teacher':'Ameen','subject':'PE','classes':[['12A','12B'],['12C','12D','12E']],'periodsPerDay':5},
        ]

        self.skillSubjectPeriods = [
            {'teachers':['Ameen','Ashley','Kavitha','Ruskin','Karthik'],'subject':'Skill','grade':11,'periodsPerWeek':3},
            {'teachers':['Ameen','Ashley','Kavitha','Ruskin','Karthik'],'subject':'Skill','grade':12,'periodsPerWeek':3}
        ]

        self.practicalPeriods = [
            {'name':'P_Comp','lab':['Comp'],'subjects':['Comp'],'classes':[(['11A'],["Deepa"]),(['11B','11C'],["Shibu",'Reshma'])],"continuously":2},
            {'name':'P_Bio','lab':['Bio'],'subjects':['Bio'],'classes':[(['11B'],["Ashwathy"]),(['11C'],["Vijitha"])],"continuously":2},
            {'name':'Prac','lab':['Chem','Phy'],'subjects':['Chem','Phy'],'classes':[(['11A'],["Shruthi","Anuradha"]),(['11B'],["Shafeela","Vidhya"]),(['11C'],["Shruthi","Lida"])],"continuously":2},
            {'name':'P_Comp','lab':['Comp'],'subjects':['Comp'],'classes':[(['12A'],["Deepa"]),(['12B','12C'],["Shibu",'Reshma'])],"continuously":2},
            {'name':'P_Bio','lab':['Bio'],'subjects':['Bio'],'classes':[(['12B'],["Ashwathy"]),(['12C'],["Vijitha"])],"continuously":2},
            {'name':'Prac','lab':['Chem','Phy'],'subjects':['Chem','Phy'],'classes':[(['12A'],["Shruthi","Vidhya"]),(['12B'],["Shafeela","Anuradha"]),(['12C'],["Shruthi","Lida"])],"continuously":2},
        ]

        self.periods = [
            {'subject':'Math','classes':['11A','11B','11C','12A','12B','12C'],'maxPerDay':[2,1],'noPerWeek':7,'repeatPerWeek':1},
            {'subject':'Chem','classes':['11A','11B','11C','12A','12B','12C'],'maxPerDay':[2,1],'noPerWeek':7,'repeatPerWeek':1},
            {'subject':'Phy','classes':['11A','11B','11C','12A','12B','12C'],'maxPerDay':[2,1],'noPerWeek':6,'repeatPerWeek':1},
            {'subject':'Comp','classes':['11A','11B','11C','12A','12B','12C'],'maxPerDay':[2,1],'noPerWeek':6,'repeatPerWeek':1},
            {'subject':'Eng','classes':['11A','11B','11C','12A','12B','12C'],'maxPerDay':[2,1],'noPerWeek':6,'repeatPerWeek':1},
        ]

        # self.specialPeriods = [
        #     {'subject':'pe','type':'extra','minPerDay':[1,4],'maxPerDay':[1,0],'noPerWeek':1,'atSameTime':2},
        # ]

        
        self.skillDay = [False for x in range(0,noOfDays)]
        self.skillAvailability = [[False for x in range(0,periodsPerDay)] for x in range(0,noOfDays)]
        self.groundAvailability = [[0 for x in range(0,periodsPerDay)] for x in range(0,noOfDays)]
        self.labAvailability = {lab:[[False for x in range(0,periodsPerDay)] for x in range(0,noOfDays)] for lab in self.labs}
        
        # print(self.groundAvalablity)

        self.data = {}

        # Initialization of Variables
        self.initiateTeachers()
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

    def getListClasses(self):
        classes = []
        for clas in self.classes:
            for div in range(65,ord(clas['maxSection'])+1):
                classes.append(str(clas['grade'])+str(chr(div)))
        return classes

    def getListOfSections(self,grade):
        tempList = []
        for gradeList in self.classes:
            if gradeList['grade'] == grade:
                for div in range(65,ord(gradeList['maxSection'])+1):
                    pickedClass = str(grade)+str(chr(div))
                    tempList.append(pickedClass)
        return tempList

    # Reset the teachers Periods for each teacher for all the days  
    def initiateTeachers(self):
        '''
        Create empty data for all the teachers in the self.teachers list
        '''
        for teacher in self.teachers:
            self.teacherAvailablity[teacher] = {}
            for day in self.days:
                self.teacherAvailablity[teacher][day] = [False for x in range(0,self.periodsPerDay)]

    def getSkillAcailablity(self):
        temp = []
        for dayIndex,day in enumerate(self.skillAvailability):
            if not self.skillDay[dayIndex]:
                for periodIndex,isOccupied in enumerate(day):
                    if not isOccupied:
                        temp.append((dayIndex,periodIndex))
        return temp

    def removeOccupiedPE(self,lst,classes,teacher):
        temp = []
        flag = 0
        for item in lst:
            flag = 0
            for sec in classes:
                if self.teacherAvailablity[teacher][self.days[item[0]]][item[1]]:
                    # print(teacher,self.teacherAvailablity[teacher][self.days[item[0]]][item[1]],self.days[item[0]],item[1])
                    continue
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

    def getLabAvailability(self,lab,check = False):
        temp = []
        for dayIndex,day in enumerate(self.labAvailability[lab]):
            for periodIndex,period in enumerate(day):
                if period == check:
                    temp.append((dayIndex,periodIndex,False))
        return temp
    
    def removeLabTeacherCoinsiding(self,lst,teacher):
        temp = []
        for item in lst:
            if not self.teacherAvailablity[teacher][self.days[item[0]]][item[1]]:
                temp.append(item)
        return(temp)
    
    def removeLabClassCoinsiding(self,lst,clas):
        temp = []
        for item in lst:
            if not self.data[clas][item[0]][item[1]]:
                temp.append(item)
        return(temp)

    def removeLabSuccessive(self,lst,no=2):
        temp = []
        for item in lst:
            if (item[0],item[1]+1,False) in lst:
                temp.append(item)
        return(temp)
    

    def getAvailablePeriodsOfDay(self,clas,day):
        temp = []
        for index,period in enumerate(self.data[clas][day]):
            if not period:
                temp.append(index)
        return temp

    def getPossibleTeacher(self,clas,subject):
        temp = []
        for teacher in self.teacherDetails:
            if teacher['subject'] == subject and clas in teacher['classes']:
                temp.append(teacher['name'])
        if len(temp)>1:
            raise
        return temp[0]

    def getAvailableTeacher(self,day,period):
        temp = []
        for teacher in self.teachers:
            if not self.teacherAvailablity[teacher][day][period+1]:
                temp.append(teacher)
        return temp

    def getTeacherFreePeriodWeek(self,teacher):
        return self.teacherAvailablity[teacher]

    def getTeacherFreePeriodDay(self,teacher,day):
        return self.teacherAvailablity[teacher][day]

    def isTeacherFree(self,teacher,day,period):
        if self.teacherAvailablity[teacher][day][period+1]:
            return False
        else:
            return True

    def removeTeacherNotAvailable(self,lst,day,teacher):
        temp = []
        for period in lst:
            if not self.teacherAvailablity[teacher][self.days[day]][period]:
                temp.append(period)
        return temp
    
    def getFreeClassesDay(self,day,period):
        temp = []
        for clas in self.data:
            for subject in self.data[clas][day]:
                if subject in ['PE','Prac','P_Bio','P_Comp']:
                    temp.append(f'{clas},Day:{self.days[day]},Period={period+1}')
        return temp

    def getFreeContinuesClasses(self,day = None):
        temp = []
        continuousTemp = []

        for clas in self.data:
            if day == None:
                for day in range(self.noOfDays):
                    for period,subject in enumerate(self.data[clas][day]):
                        if subject in ['PE','Prac','P_Bio','P_Comp']:
                            temp.append((day,period,clas))
            else:
                for period,subject in enumerate(self.data[clas][day]):
                        if subject in ['PE','Prac','P_Bio','P_Comp']:
                            temp.append((day,period,clas))
            
        continuousTemp = []
        for item in temp:
            if (item[0],item[1]+1,item[2]) in temp:
                continuousTemp.append(item)
                continuousTemp.append((item[0],item[1]+1,item[2]))
            continuousTemp.append("")

        return continuousTemp

    # Create Empty files to save it later
    def saveAsCSV(self):
        # Check and create the main 'Classes' directory
        if not os.path.exists('Classes'):
            os.mkdir('Classes')
            
        for clas in self.classes:
            grade_folder = os.path.join('Classes', f"{clas['grade']}Grade")
            
            # Check and create the grade-specific folder
            if not os.path.exists(grade_folder):
                os.mkdir(grade_folder)

            for classData in self.data:
                grade = ''.join([i for i in classData if i.isdigit()])  
                
                if int(grade) == int(clas['grade']):
                    filePath = os.path.join(grade_folder, f"{classData}.csv")

                    # Create and write to the file
                    with open(filePath, 'w', newline='') as file:
                        writer = csv.writer(file)
                        
                        # Prepare the header
                        header = [classData]
                        for period in range(self.periodsPerDay):
                            header.append(period + 1)
                        writer.writerow(header)

                        # Prepare the rows
                        temp = []
                        for index, day in enumerate(self.data[classData]):
                            temp.append([self.days[index]] + day)

                        writer.writerows(temp)
    # Create a list and return a list of all classes and sections together in the form of a string in list, ie.['11A','11B','12A','12B'].
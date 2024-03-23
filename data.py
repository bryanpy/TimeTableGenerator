import csv
import os
import copy

class Data:
    def __init__(self,periodsPerDay,noOfDays):
        self.noOfDays = noOfDays
        self.periodsPerDay = periodsPerDay

        # Should get rid of this
        self.emptyPossiblePeriods = [x for x in range(0,periodsPerDay)]

        self.possibleIndexes = {}


        # Data for creating the Time table
        self.teachers = [
            {'name':'Karuna','subjects':['math'],'classes':['11A','11B','11C'],'hoursPerDay':5},
            {'name':'Reshma','subjects':['math'],'classes':['11A','11B','11C'],'hoursPerDay':5},

            {'name':'Shafeela','subjects':['chem'],'classes':['11A','11B'],'hoursPerDay':5},
            {'name':'Shrithi','subjects':['chem'],'classes':['11A','11C'],'hoursPerDay':5},
            {'name':'Krithika','subjects':['chem'],'classes':['11B','11C'],'hoursPerDay':5},

            {'name':'Vidhya','subjects':['phys'],'classes':['11A','11B'],'hoursPerDay':5},
            {'name':'Anuradha','subjects':['phys'],'classes':['11B','11C'],'hoursPerDay':5},
            {'name':'Lida','subjects':['phys'],'classes':['11A','11C'],'hoursPerDay':5},

            {'name':'Deepa','subjects':['comp'],'classes':['11A'],'hoursPerDay':5},
            {'name':'Judith','subjects':['comp'],'classes':['11A'],'hoursPerDay':5},
            {'name':'Shibu','subjects':['comp'],'classes':['11C'],'hoursPerDay':5},

            {'name':'Anitha','subjects':['engl'],'classes':['11A','11B'],'hoursPerDay':5},
            {'name':'Irine','subjects':['engl'],'classes':['11C'],'hoursPerDay':5},

        ]
        
        self.practicals = [
            {'subject':'comp','contCount':2,'weekly':1},
            {'subject':'chem/phy','contCount':2,'weekly':1},
        ]

        self.periods = [
            {'subject':'math','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':7},
            {'subject':'chem','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':7},
            {'subject':'phys','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6},
            {'subject':'comp','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6},
            {'subject':'skil','minPerDay':[0,3],'maxPerDay':[1,1],'noPerWeek':3},
            {'subject':'engl','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6},
        ]

        self.specialPeriods = [
            {'subject':'PE','minPerDay':[1,4],'maxPerDay':[1,0],'noPerWeek':1,'atSameTime':2},
        ]
        
        self.classes = [
            {'grade':11,'maxSection':'E'},
            {'grade':12,'maxSection':'E'}
        ]

        self.data = {}

        # Initialization of Variables
        self.resetTeacherPeriods()
        self.createEmptyData()

    # Creates the empty data in the beginning 
    def createEmptyData(self):
        table = []
        # print(temp)
        for dayNum in range(1,self.noOfDays+1):
            table.append(["" for x in range(self.periodsPerDay+1)])
            # print(table)

        for clas in self.classes:
            for div in range(65,ord(clas['maxSection'])+1):
                self.data[str(clas['grade'])+str(chr(div))] = copy.deepcopy(table)
    

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


    # Reset the teachers Periods for each teacher once one teacher is done
    def resetTeacherPeriods(self):
        for x in self.teachers:
            x['possiblePeriods'] = self.emptyPossiblePeriods[:]


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
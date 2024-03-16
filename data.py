import csv
import os 

class Data:
    def __init__(self,periodsPerDay,noOfDays):
        self.emptyPossiblePeriods = [x for x in range(0,periodsPerDay)]

        self.teachers = [
            {'name':'Karuna','subjects':['math'],'grades':[11,12],'hoursPerDay':5}, 
            {'name':'Shafeela','subjects':['chem'],'grades':[11,12],'hoursPerDay':5},
            {'name':'Vidhya','subjects':['phys'],'grades':[11,12],'hoursPerDay':5},
            {'name':'Deepa','subjects':['comp'],'grades':[11,12],'hoursPerDay':5},
            {'name':'Ashley','subjects':['skil'],'grades':[11,12],'hoursPerDay':5},
            {'name':'Anitha','subjects':['engl'],'grades':[11,12],'hoursPerDay':5}
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
        self.table = []

        self.resetTeacherPeriods()

    def createTable(self):
        week = self.table
        for dayNum in range(1,self.noOfDays+1):
            week.append([""]*self.periodsPerDay)
        self.table = week

    def resetTeacherPeriods(self):
        for x in self.teachers:
            x['possiblePeriods'] = self.emptyPossiblePeriods[:]

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
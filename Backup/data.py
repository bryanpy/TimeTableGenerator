import csv
import os 

class Data:    
    def __init__(self):
        self.periods = [
            {'subject':'Math','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':7},
            {'subject':'Chem','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':7},
            {'subject':'Phys','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6},
            {'subject':'Comp','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6},
            {'subject':'Skil','minPerDay':[0,3],'maxPerDay':[1,1],'noPerWeek':3},
            {'subject':'Engl','minPerDay':[1,4],'maxPerDay':[2,1],'noPerWeek':6},
        ]

        self.classes = [
            {'grade':11,'maxSection':'E'},
            {'grade':12,'maxSection':'E'}
        ]

        
    
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
import time
import random as rand   
import data
from timetable import *

start_time = time.time()

table = Timetable(8,5)
table.generateTimetable()

table.printTimetable()
table.updateSQLData()

table.saveAsCSV()

'''
  _____   _                        _____          _        
 |_   _| (_)  _ __ ___     ___    |_   _|  _ __  (_) __  __
   | |   | | | '_ ` _ \   / _ \     | |   | '__| | | \ \/ /
   | |   | | | | | | | | |  __/     | |   | |    | |  >  < 
   |_|   |_| |_| |_| |_|  \___|     |_|   |_|    |_| /_/\_\ 
 A time table Generator made for generating class time tables
 '''
  

from flask import Flask, render_template
import main
app = Flask(__name__)

timetable = main.table.getData()

@app.route('/')
def home():
    return render_template("home.html",data = timetable,table = main.table)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
    
from flask import Flask, render_template
import main
app = Flask(__name__)

timetable = main.table.getData()

@app.route('/')
def home():
    return render_template("landing.html",data = timetable,table = main.table)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
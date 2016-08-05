from flask import Flask
from flask import render_template
import simulation
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/coolDude/<name>")
def coolDude(name):
    return "Hey %s, you are kewl" % name

@app.route("/graphTest")
def graphTest():
    # somehow have the results, maybe in a DB
    labels = ["January","February","March","April","May","June","July","August","January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=labels)

@app.route("/runSim")
def runSim():
    controlData = simulation.controlExactNeeds()


    values = controlData["market"]["Sally's"]["lemon"]["profit"]
    labels = range(0,len(values))

    return render_template('chart.html', values=values, labels=labels)

@app.route('/testTemplates/<name>')
def testTemplates(name):
    return render_template("template1.html", name=name)

@app.route("/")
def chart():
    pass
    

if __name__ == "__main__":
    app.run()
from flask import Flask, jsonify
from flask import render_template
from flask import request
import simulation
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World ya dummie!"

@app.route("/coolDude/<name>")
def coolDude(name):
    return "Hey %s, you are kewl" % name

@app.route("/graphTest")
def graphTest():
    # somehow have the results, maybe in a DB
    labels = ["January","February","March","April","May","June","July","August","January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8,10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=labels)

@app.route("/plenty")
def plenty():
    return render_template('plenty.html')

@app.route("/runSim")
def runSim():
    return render_template('chart.html')

@app.route("/intro")
def intro():
    return render_template('introduction.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/prototypes")
def prototypes():
    return render_template('prototypes.html')

@app.route("/insights")
def insights():
    return render_template('insights.html')


@app.route('/resimulate', methods=['GET', 'POST'])
def resimulate():
    """
    Dynamically rerun the sim with new params, dawgie!!!!

    Sim data params...
        self.simData["profit"] = []
        self.simData["hoursWithout"] = []
        self.simData["waste"] = []
        self.simData["avgFreshness"] = []
    """

    ingredient = "lemon"
    simArgs = request.args

    simData = simulation.dynamicSim(simArgs, ingredient)

    return jsonify(results=simData)

@app.route('/testTemplates/<name>')
def testTemplates(name):
    return render_template("template1.html", name=name)

@app.route("/")
def chart():
    pass

if __name__ == "__main__":
    app.run()
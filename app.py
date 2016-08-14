from flask import Flask, jsonify
from flask import render_template
from flask import request
import simulation
import random
app = Flask(__name__)

@app.route("/")
def home():
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

    simData, controlData = simulation.runSims(simArgs, ingredient)
    
    return jsonify(results=simData, control=controlData)

if __name__ == "__main__":
    app.run()
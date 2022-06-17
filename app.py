from flask import Flask, render_template, request, redirect, url_for
from predict import *
import tensorflow.keras as tfk
import numpy as np
import os
import sys
import cassiopeia as cass
from cassiopeia import Summoner, FeaturedMatches, Champion, ChampionMastery, Queue, Position, Rank

#create app
app = Flask(__name__, template_folder='./templates')

#initialize model
model = init_model()

#home screen endpoint
@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("index.html")

@app.route("/test", methods=["POST", "GET"])
def user():
    req = request.form
    summonerName = str(req["inputName"])
    summonerRegion = str(req["inputRegion"])
    gameInfo = game_info(summonerName, summonerRegion)
    modelInput = inputFactory(gameInfo)
    prediction = predict(model, modelInput)
    return f"<h1>{prediction}</h1>"
    # req = request.form
    # userName = req["inputName"]
    # region = req["inputRegion"]
    # return f"<h1>{userName}{region}</h1>"

@app.route('/riot.txt') 
def riottxt():  
    return "<h1>{abxd}</h1>"

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    req = request.form
    summonerName = req["inputName"]
    summonerRegion = req["inputRegion"]
    gameInfo = game_info(summonerName, summonerRegion)
    prediction = predict(model, gameInfo)
    return f"<h1>{prediction}</h1>"
    #return render_template("index.html", prediction=prediction)

#run app
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)































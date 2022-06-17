import tensorflow.keras as tfk
import numpy as np
import os
import sys
import cassiopeia as cass
from cassiopeia import Summoner, FeaturedMatches, Champion, ChampionMastery, Queue, Position, Rank

sys.path.append(os.path.abspath('./model'))

#initialize model
def init_model():
    loaded_model = tfk.models.load_model("kerasModel")
    print("loaded model success")
    return loaded_model

#get live game data
def game_info(name, region):
    
    cass.set_riot_api_key(getAPI_key())
    gameInfo=[]
    summoner = Summoner(name=name, region=region)
    regionName=summoner.region
    current_match = summoner.current_match
    averageRankList = []
    
    for participant in current_match.blue_team.participants:
        
        cm=cass.get_champion_mastery(participant.summoner, participant.champion, regionName)
        try:
            entry=participant.summoner.league_entries.fives()
            tierNumber=entry.tier._order()[entry.tier]
            divisionNumber=entry.division._order()[entry.division]
            elo = elo_score(tierNumber,divisionNumber)
            averageRankList.append(elo)
        except:
            elo = -1.0
            
        gameInfo.append(participant.champion.id)
        gameInfo.append(cm.points)
        gameInfo.append(participant.summoner.level)
        gameInfo.append(elo)
        
    for participant in current_match.red_team.participants:
        
        cm=cass.get_champion_mastery(participant.summoner, participant.champion,regionName)
        try:
            entry=participant.summoner.league_entries.fives()
            tierNumber=entry.tier._order()[entry.tier]
            divisionNumber=entry.division._order()[entry.division]
            elo = elo_score(tierNumber,divisionNumber)
            averageRankList.append(elo)
        except:
            elo = -1.0
            
        gameInfo.append(participant.champion.id)
        gameInfo.append(cm.points)
        gameInfo.append(participant.summoner.level)
        gameInfo.append(elo)
        
    if len(averageRankList)==0:
        return [x if x!=-1.0 else 35.0 for x in gameInfo]
    else:
        averageRank = round(sum(averageRankList)/len(averageRankList),2)
        return [x if x!=-1.0 else averageRank for x in gameInfo]
    return gameInfo

def inputFactory(arr):
    arr = np.array(arr)
    for i in range(1,40,4):
        arr[i] = np.log2(arr[i]*0.001+1.0)*10
    return np.array(arr).reshape(1,40)

#make prediction based on input
def predict(model, gameInfo):
    return model.predict(gameInfo)


#supportive functions for game_info
def getAPI_key():
    f = open("api_key.txt", "r")
    return f.read()
def elo_score(Tier: int, Division: int):
    return Tier*10+(Division-1)*2.5
def Average(lst):
    return sum(lst) / len(lst)
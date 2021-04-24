from flask import Flask, render_template , redirect, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('ipl_score_model', 'rb'))

def get_players(players,names1):

    for i in name_bat_team : 
        try:
            for j in names1[i].index:

                    players[i].add(j)
        except:
            pass



new_df = pd.read_csv('ipl1.csv')
batsmen = pd.get_dummies(new_df.batsman)
bowlers = pd.get_dummies(new_df.bowler)
batting_team = pd.get_dummies(new_df.bat_team)
bowling_team = pd.get_dummies(new_df.bowl_team)
venue = pd.get_dummies(new_df.venue)

name_batsmen = batsmen.columns.tolist()
name_bowlers = bowlers.columns.tolist()
name_bat_team = batting_team.columns.tolist()
name_bowl_team = bowling_team.columns.tolist()
name_venue = venue.columns.tolist()

batsmen_array = [0 for i in range(len(name_batsmen))]
bowler_array = [0 for i in range(len(name_bowlers))]
bat_team_array = [0 for i in range(len(name_bat_team))]
bowl_team_array = [0 for i in range(len(name_bowl_team))]
venue_array = [0 for i in range(len(name_venue))]

players = {}

for i in name_bat_team:
    players[i] = set()

names = new_df
names1 = names.groupby('bat_team')['batsman'].value_counts()

names2 = names.groupby('bowl_team')['bowler'].value_counts()
get_players(players,names1)
get_players(players,names2)
for i in players:
	i = list(i)

@app.route('/',methods=['GET','POST'])
def first():
	ans_string = ""
	if request.method == 'POST':
		bat_team 		= request.form['bat_team']
		bowl_team 		= request.form['bowl_team']
		current_runs	= int(request.form['current_runs'])
		current_wickets	= int(request.form['current_wickets'])
		over			= float(request.form['over'])
		last_runs		= int(request.form['last_runs'])
		last_wickets	= int(request.form['last_wickets'])
		venue 			= request.form['venue']
		batsman 		= request.form['batsman']
		batsman_2 		= request.form['batsman_2']
		bowler 			= request.form['bowler']

		print(batsman,bowler,bat_team,bowl_team,venue)
		if bat_team == bowl_team:
			ans_string = "Batting and bowling team cannot be same"
			return render_template('home.html',ans = [name_batsmen,name_bowlers,name_bat_team,name_bowl_team,name_venue,ans_string ])
		batsmen_array[name_batsmen.index(batsman)]=1
		bowler_array[name_bowlers.index(bowler)]=1
		bat_team_array[name_bat_team.index(bat_team)]=1
		bowl_team_array[name_bowl_team.index(bowl_team)]=1
		venue_array[name_venue.index(venue)]=1

		vals = [current_runs,current_wickets,over,last_runs,last_wickets] +batsmen_array+bowler_array + bat_team_array + bowl_team_array + venue_array

		prediction = np.round(model.predict([vals])[0],0)

		ans_string = "Predicted Score for {} is : {} to {}".format(bat_team,prediction-10,prediction+10)
	
		return render_template('home.html',ans = [name_batsmen,name_bowlers,name_bat_team,name_bowl_team,name_venue,ans_string ])
	else:
		return render_template('home.html',ans = [name_batsmen,name_bowlers,name_bat_team,name_bowl_team,name_venue,ans_string ])

if __name__ == '__main__':
	app.run(debug=False)
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:06:18 2019

@author: Sushruth
"""

import pandas as pd
import numpy as np
match_stat = pd.DataFrame()

matchdf=pd.read_excel('match.xlsx')
#find total number of matches played by each team accross all seasons

team1lst=matchdf['Team_Name_Id'].value_counts()
team2lst=matchdf['Opponent_Team_Id'].value_counts()
tot=team1lst+team2lst
team1lst=team1lst.sort_index()
team2lst=team2lst.sort_index()
team1lst=team1lst.reset_index()
team2lst=team2lst.reset_index()
tot= tot.reset_index()


print(tot.columns)
tot=tot.rename(columns={'index':'Team_Id',0:'Match_Count_Total'})

match_stat['Team_Id'] = tot['Team_Id']


match_stat['Home_Match_Count']=team1lst['Team_Name_Id']
match_stat['Away_Match_Count']=team2lst['Opponent_Team_Id']

match_stat['Match_Count_Total'] = tot['Match_Count_Total']



nummatcheswon=matchdf['Match_Winner_Id'].value_counts()
nummatcheswon=nummatcheswon.sort_index()
nummatcheswon=nummatcheswon.reset_index()
nummatcheswon=nummatcheswon.rename(columns={'index':'Team_Id'})
match_stat['Matches_Won']=nummatcheswon['Match_Winner_Id']

winpercent= matchdf.groupby('Match_Winner_Id').agg({'Won_By':'count'})
match_stat=match_stat.set_index('Team_Id')
match_stat['Tot_Win_Percent']=winpercent['Won_By']

match_stat['Tot_Win_Percent']=match_stat['Tot_Win_Percent']/match_stat['Match_Count_Total']*100

hometeamwon=matchdf.query('Team_Name_Id==Match_Winner_Id')
awayteamwon=matchdf.query('Opponent_Team_Id==Match_Winner_Id')

homewon=hometeamwon['Match_Winner_Id'].value_counts()
homewon=homewon.sort_index().reset_index().set_index('index')

awaywon=awayteamwon['Match_Winner_Id'].value_counts()
awaywon=awaywon.sort_index().reset_index().set_index('index')

match_stat['Home_Match_Won']=homewon['Match_Winner_Id']
match_stat['Away_Match_Won']=awaywon['Match_Winner_Id']

match_stat['Home_Win_Percent']=match_stat['Home_Match_Won']/match_stat['Home_Match_Count']*100
match_stat['Away_Win_Percent']=match_stat['Away_Match_Won']/match_stat['Away_Match_Count']*100

playerdf = pd.read_excel('Player.xlsx')
bbbdf= pd.read_excel('Ball_by_Ball.xlsx')
runs=bbbdf.groupby('Striker_Id').agg({'Batsman_Scored':'sum'})
print('top 10 batsmen based on Runs')
topScorers=bbbdf.groupby('Striker_Id').agg({'Batsman_Scored':'sum'}).sort_values(by='Batsman_Scored', ascending = False).head(10)
topScorers=topScorers.reset_index()
topScorers=topScorers.rename(columns={'Striker_Id':'Player_Id'})

topScorers=pd.merge(topScorers,playerdf)

wickets = bbbdf.query('Dissimal_Type!=" " & Dissimal_Type!="run out"')
numwick = wickets.groupby('Bowler_Id').agg({'Bowler_Id':'count'}).rename(columns={'Bowler_Id':'Wicket_Num'}).sort_values(by='Wicket_Num',ascending=False).head(10)
numwick = numwick.reset_index()
numwick = numwick.rename(columns={'Bowler_Id':'Player_Id'})
topwicket = pd.merge(numwick,playerdf)

runsperbowler=bbbdf.groupby('Bowler_Id').agg({'Batsman_Scored':['sum','count']})
runsperbowler.columns = ['Runs','Balls']

runsperbowler['Economy'] = runsperbowler['Runs']/runsperbowler['Balls']
runsperbowler['Economy']=runsperbowler['Economy']*6
worstbowlers=runsperbowler.sort_values(by = 'Economy',ascending = False)
bestbowlers=runsperbowler.sort_values(by = 'Economy',ascending = True)
worstbowlers=worstbowlers.query('Balls>=120')
bestbowlers=bestbowlers.query('Balls>=120')
worstbowlers=worstbowlers.reset_index()
worstbowlers=worstbowlers.rename(columns={'Bowler_Id':'Player_Id'})
worstbowlers=pd.merge(worstbowlers,playerdf)

bestbowlers=bestbowlers.reset_index()
bestbowlers=bestbowlers.rename(columns={'Bowler_Id':'Player_Id'})
bestbowlers=pd.merge(bestbowlers,playerdf)

runsperbowlerxtra= bbbdf.query('Extra_Type == "wides" | Extra_Type == "noballs"')
runsperbowlerxtra['Extra_Runs']=runsperbowlerxtra['Extra_Runs'].fillna(0)
runsperbowlerxtra['TotalRuns']=runsperbowlerxtra['Extra_Runs']+runsperbowlerxtra['Batsman_Scored']

run1= pd.merge(bbbdf,runsperbowlerxtra,how='left')
run1['TotalRuns'] = run1['TotalRuns'].fillna(0)
run1['TotalRuns']=  run1['TotalRuns']+run1['Batsman_Scored']


runsperbowlerxtra1=run1.groupby('Bowler_Id').agg({'TotalRuns':['sum','count']})
runsperbowlerxtra1.columns = ['Runs','Balls']


runsperbowlerxtra1['Economy'] = runsperbowlerxtra1['Runs']/runsperbowlerxtra1['Balls']
runsperbowlerxtra1['Economy']=runsperbowlerxtra1['Economy']*6
worstbowlersxtra=runsperbowlerxtra1.sort_values(by = 'Economy',ascending = False)
bestbowlersxtra=runsperbowlerxtra1.sort_values(by = 'Economy',ascending = True)
worstbowlersxtra=worstbowlersxtra.query('Balls>=120')
bestbowlersxtra=bestbowlersxtra.query('Balls>=120')
worstbowlersxtra=worstbowlersxtra.reset_index()
worstbowlersxtra=worstbowlersxtra.rename(columns={'Bowler_Id':'Player_Id'})
worstbowlersxtra=pd.merge(worstbowlersxtra,playerdf)

bestbowlersxtra=bestbowlersxtra.reset_index()
bestbowlersxtra=bestbowlersxtra.rename(columns={'Bowler_Id':'Player_Id'})
bestbowlersxtra=pd.merge(bestbowlersxtra,playerdf)



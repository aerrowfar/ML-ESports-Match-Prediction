import pandas as pd
import numpy as np
import random
import csv
from itertools import islice

#PARAMETERS:

in_csv='lol_game_data_update_april_17.csv'
split = 0.9

################################################
number_lines = sum(1 for row in (open(in_csv)))
number_games=int((number_lines-1)/10)
end_row_train_split = (int(number_games*split))*10

train_df = pd.read_csv(
    in_csv,
    header=0,
    index_col=0,
    nrows=end_row_train_split

    )

test_df = pd.read_csv(
    in_csv,
    names=['date', 'game', 'playerid', 'position', 'player', 'team', 'champion','classes',
       'golddiffat10', 'golddiffat15', 'teamgolddiffat10', 'teamgolddiffat15',
       'result'],
    index_col=0,
    skiprows=end_row_train_split+1
    
    )

test_df = test_df.reset_index()


print(train_df.columns)
print(train_df.head(10))
print(train_df.tail(10))
print(test_df.head(10))
print(test_df.tail(10))

#initializes train and test dataframes
df=pd.DataFrame(columns=['index','action','cost','teams','champs1','champs2','classes1','classes2','players1','players2','teamgold10','teamgold15','gold10','gold15','result','winner','probability'])
df.set_index('index',inplace=True)

df_test=pd.DataFrame(columns=['index','teams','champs1','champs2','classes1','classes2','players1','players2','teamgold10','teamgold15','gold10','gold15','result'])
df_test.set_index('index',inplace=True)

def cleanup(input_frame,output_frame,test):
    i=0
    b=0
    while (i<(len(input_frame.index)-9)):
        player1=[]
        champ1=[]
        classes1=[]
        player2=[]
        champ2=[]
        classes2=[]
        teamgold10=[]
        teamgold15=[]
        teams=[]
        gold10=0
        gold15=0
        
        #loops through 10 at a time and appends as a list to df 
        for j in range(i,i+11):
            #first team
            if j-i<5:
                player1.append(input_frame.loc[j,'player'])
                champ1.append(input_frame.loc[j,'champion'])
                classes1.append(input_frame.loc[j,'classes'])
                teamgold10.append(input_frame.loc[j,'golddiffat10'])
                teamgold15.append(input_frame.loc[j,'golddiffat15'])
            #second team
            elif j-i<10:
                player2.append(input_frame.loc[j,'player'])
                classes2.append(input_frame.loc[j,'classes'])
                champ2.append(input_frame.loc[j,'champion'])
            #append values
            else:
                output_frame.loc[b,'champs1']= champ1
                output_frame.loc[b,'champs2']= champ2
                output_frame.loc[b,'players1']=player1
                output_frame.loc[b,'players2']=player2
                output_frame.loc[b,'classes1']= classes1
                output_frame.loc[b,'classes2']= classes2
                output_frame.loc[b,'teamgold10']=teamgold10
                output_frame.loc[b,'teamgold15']=teamgold15
                output_frame.loc[b,'gold10'] = input_frame.loc[j-1,'teamgolddiffat10']
                output_frame.loc[b,'gold15'] = input_frame.loc[j-1,'teamgolddiffat15']
                
                teams.append(input_frame.loc[j-6,'team'])
                teams.append(input_frame.loc[j-1,'team'])
                output_frame.loc[b,'teams']=teams
                
                #if test dataframe, results are 1 or 2. if train, results are 0 or 1.
                if test==True:
                    output_frame.loc[b,'result'] = int(input_frame.loc[j-1,'result'])+1
                else:
                    output_frame.loc[b,'result'] = input_frame.loc[j-1,'result']

        i=i+10
        b=b+1
        print('Finished cleaning up to row: '+str(i))
        print('going up to row: ',str(end_row_train_split))
        

cleanup(train_df,df,False)
cleanup(test_df,df_test,True)

pd.set_option('display.max_columns', 12)
print(df.head(1))
print(df_test.head(1))
print(df.tail(1))
print(df_test.tail(1))

winner=''
location=0

for index in df.index:
    #sets winning team name
    winner=df.loc[index,'teams']
    location=df.loc[index,'result']
    print('winner is'+str(winner)+' and location is '+str(location))
    df.loc[index,'winner']=winner[location]

    #sets deterministic probability for action
    df.loc[index,'probability'] = 1
    
    #sets random action
    df.loc[index,'action']=random.randrange(1,3)

    #figures out the cost for the agent based on action and result, remember we are minimizing cost
    #in vowpal wabbit library which will use this data, cost = reward
    if int(df.loc[index,'action'])==(int(df.loc[index,'result'])+1):
        df.loc[index,'cost']=-1
    else:
        df.loc[index,'cost']=1

    print('fixing actions/cost/prob at row: '+str(index))


#SAVES READY TO GO DATA:
df.to_csv('train_data.csv')
df_test.to_csv('test_data.csv')

print(df.tail(5))
print(df_test.tail(5))



from vowpalwabbit import pyvw
import pandas as pd
import numpy as np

train_data=pd.read_csv('train_data.csv')
test_data=pd.read_csv('test_data.csv')

#exploration models

vw=pyvw.vw('--cb_explore 2 --epsilon 0.2')
#vw=pyvw.vw('--cb_explore 2 --bag 3')
#vw=pyvw.vw('--cb_explore 2 --cover 3')

#non-exploration models

#vw=pyvw.vw('--cb 2')

#loop through training data
for i in range(0,len(train_data.index)-1):
    #here all the variables are grabbed for learning.
    action = train_data.loc[i,'action']
    cost= train_data.loc[i,'cost']
    probability=train_data.loc[i,'probability']
    feature1 = train_data.loc[i,'champs1']
    feature2 = train_data.loc[i,'champs2']
    feature3 = train_data.loc[i,'players1']
    feature4 = train_data.loc[i,'players2']
    feature5 = train_data.loc[i,'teamgold10']
    feature6 = train_data.loc[i,'teamgold15']
    feature7 = train_data.loc[i,'gold10']
    feature8 = train_data.loc[i,'gold15']
    feature9 = train_data.loc[i,'classes1']
    feature10 = train_data.loc[i,'classes2']
    
    #learning format is set.
    learn_example = str(action)+':'+str(cost)+':'+str(probability)+' | '+str(feature1)+' '+str(feature2)+' '+str(feature3)+' '+str(feature4)+' '+str(feature5)+' '+str(feature6)+' '+str(feature7)+' '+str(feature8)+' '+str(feature9)+' '+str(feature10)
    
    print('learning '+str(i)+'th example')

    #learning
    vw.learn(learn_example)



num_correct=0

#loop through testing data
for j in test_data.index:
    #here all the variables are grabbed for testing.
    feature1=test_data.loc[j,'champs1']
    feature2=test_data.loc[j,'champs2']
    feature3=test_data.loc[j,'players1']
    feature4=test_data.loc[j,'players2']
    feature5=test_data.loc[j,'teamgold10']
    feature6=test_data.loc[j,'teamgold15']
    feature7=test_data.loc[j,'gold10']
    feature8=test_data.loc[j,'gold15']
    feature9=test_data.loc[j,'classes1']
    feature10=test_data.loc[j,'classes2']
  
    #testing format is set.
    test_example = '| '+str(feature1)+' '+str(feature2)+' '+str(feature3)+' '+str(feature4)+' '+str(feature5)+' '+str(feature6)+' '+str(feature7)+' '+str(feature8)+' '+str(feature9)+' '+str(feature10)
   
    #prediction 
    choice=vw.predict(test_example)

    #format below is for exporation strategies.
    #switch the commented below with non-commented for non-exploration models.

    #if int(choice)== int(test_data.loc[j,'result']):
    if (np.argmax(choice)+1)== int(test_data.loc[j,'result']):
        #print('for game '+str(j)+' model predicts CORRECTLY: '+str(choice))
        print('for game '+str(j)+' model predicts CORRECTLY: '+str(np.argmax(choice)+1))
        num_correct=num_correct+1
    else: 
        #print('for game '+str(j)+' model predicts WRONG: '+str(choice))
        print('for game '+str(j)+' model predicts WRONG: '+str(np.argmax(choice)+1))

#results analysis
corect= (num_correct/(len(test_data.index)))*100
print('got this many correct: '+str(num_correct))
print('out of this many total games/predictions: '+str(len(test_data.index)))
print('percent correct is: '+str(corect))    

#save model
vw.save('cb_predictor.model')
del vw



**Predicting outcome of e-sports matches using reinforcement learning contextual bandits.** 

Academic paper link: https://drive.google.com/file/d/1c2or-AecvCPWI3LFk3dHfrw3jiNqcE-X/view?usp=sharing

This contextual bandit approach using Vowpal Wabbit library aims to predict the winner of a League of Legends professional match using 10 distinct features. My team and I spent significant time feature engineering using domain knowledge and conducting ablation studies for best possible results using a wide breadth of bandit algorithms. We were able to achieve 71.61% on 7 years of data using features 5 to 10 and Epsilon-Greedy 0.2 exploration method. We also conducted the same experiement through supervised learning, using binary classification and aiming for min log loss, to achieve 75.8% accuracy. All results and our findings are discussed in the paper linked above.

**Features:**

1)Champs1- This is a list of champions picked by the 1st team in a list formatted as a string. E.g [‘Nautilus’,’Diana’,’Xerath’,’Miss Fortune’,’Leona’]

2)Champs2- This is a list of champions picked by the 2nd team in a list formatted as a string. E.g [‘Darius’,’Lee Sin’,’Ziggs’,’Lucian’,’Thresh’]

3)Players1- This is a list of players in the 1st team in a list formatted as a string. E.g [‘Soaz’,’Xpeke’,’Cyanide’,’Rekkles’,’Yellowstar’]

4)Players2- This is a list of players in the 2nd team in a list formatted as a string. E.g [‘YoungBuck’,’Amazing’,’cowTard’,’Forg1ven’,’Unlimited’]

5)Teamgold10- This is a list of gold differences between 1st team and 2nd team at 10 minutes in the game for every position in a list formatted as a string. E.g [‘-6’,’10’,’-1500’,’35’,’100’]

6)Teamgold15- This is a list of gold differences between 1st team and 2nd team at 15 minutes in the game for every position in a list formatted as a string. E.g [‘-60’,’90’,’-1400’,’35’,’100’]

7)gold10- This is an int of total gold differences between 1st team and 2nd team at 10 minutes into the game. E.g  -400

8)gold15- This is an int of total gold differences between 1st team and 2nd team at 15 minutes into the game. E.g  1500

9)Classes1- This is a list of champion classes (an abstraction of champions) picked by the 1st team in a list formatted as a string. E.g [‘Juggernaut’,’Catcher’,’Burst’,’Marksman’,’Warden’]

10)Classes2- This is a list of champion classes (an abstraction of champions) picked by the 2nd team in a list formatted as a string. E.g [‘Skirmisher’,’Specialist’,’Burst’,’Marksman’,’Burst’]

Raw data can be obtained from https://oracleselixir.com/.

**Contextual Bandit Algorithms:**

CB2 - optimize predictor based on already collected data, or contextual bandits without exploration. ‘2’ indicates a total of 2 actions, action space does not change.

CB Epsilon 0.2 - Epsilon-Greedy exploration strategy, at each example, the prediction of the current learned policy is taken with probability 1-epsilon, and with the remaining epsilon probability an action is chosen uniformly at random. ‘0.2’ is the value for epsilon.

CB Bag 3- This exploration rule is based on an ensemble approach. It takes in an argument m and trains m different policies. The policies differ by being trained on different random subsets of the data, with each example going to a subset of the m policies. This is a simple and effective approach that rules out obviously bad actions, while exploring amongst the plausibly good ones when the variation amongst the m policies is adequate. ‘3’ in this case is m. 

CB Cover 3- This is a theoretically optimal exploration algorithm based on this paper. Like bagging, many different policies are trained, with the number specified as an argument m. Unlike bagging, the training of these policies is explicitly optimized to result in a diverse set of predictions, choosing all the actions which are not already learned to be bad in a given context. This is the most sophisticated of the available options for contextual bandit learning. ‘3’ in this case is m. 



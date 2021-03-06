# -*- coding: utf-8 -*-
"""6893_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11kjv_oxMMKtuz_ONVRuHmsIeeI462Ktd
"""

!pip install scikit-plot

from google.colab import drive
drive.mount('/content/drive')

#Data loading
import pandas as pd

DATA = "/content/drive/My Drive/E6893 Project dataset"
train = pd.read_csv(DATA+"/train.csv")
test = pd.read_csv(DATA+"/test.csv")
train_label = pd.read_csv(DATA+"/train_labels.csv")
install_list =list(train_label.installation_id.unique())
train = train[train.installation_id.isin(install_list)]

"""#Preprocessing & EDA"""

train.shape

"""Delete the installation id that didn't paticipate the assessment of **train label** for **train**
The dimension is reduced to (7734558, 11)
"""

install_list =list(train_label.installation_id.unique())
train = train[train.installation_id.isin(install_list)]

train

"""## EDA

### EDA For **train**
"""

import matplotlib.pylab as plt
import seaborn as sns

plt.rcParams.update({'font.size': 16})

fig = plt.figure(figsize=(12,10))
ax1 = fig.add_subplot(211)
ax1 = sns.countplot(y="type", data=train, color="#4682B4", order = train.type.value_counts().index)
plt.title("Number of event types (train.csv)")

ax2 = fig.add_subplot(212)
ax2 = sns.countplot(y="world", data=train, color="#4682B4", order = train.world.value_counts().index)
plt.title("Number of world (train.csv)")

plt.tight_layout(pad=0)
plt.show()

plt.rcParams.update({'font.size': 12})

fig = plt.figure(figsize=(12,10))
se = train.title.value_counts().sort_values(ascending=True)
se.plot.barh()
plt.title("Number of event title (train.csv)")
plt.xticks(rotation=0)
plt.show()

plt.rcParams.update({'font.size': 12})

fig = plt.figure(figsize=(12,10))
se = train.event_code.value_counts().sort_values(ascending=True)
se.plot.barh()
plt.title("Number of event code (train.csv)")
plt.xticks(rotation=0)
plt.show()

import numpy as np
my_pal = sns.color_palette(n_colors=10)

train['game_time'].apply(np.log1p) \
    .plot(kind='hist',
          figsize=(15, 5),
          bins=100,
          title='Log Transform of game_time (train.csv)',
          color=my_pal[0])
plt.show()

"""### EDA For **test**"""

plt.rcParams.update({'font.size': 16})

fig = plt.figure(figsize=(12,10))
ax1 = fig.add_subplot(211)
ax1 = sns.countplot(y="type", data=test, color="#4682B4", order = test.type.value_counts().index)
plt.title("Number of event types (test.csv)")

ax2 = fig.add_subplot(212)
ax2 = sns.countplot(y="world", data=test, color="#4682B4", order = test.world.value_counts().index)
plt.title("Number of world (test.csv)")

plt.tight_layout(pad=0)
plt.show()

plt.rcParams.update({'font.size': 12})

fig = plt.figure(figsize=(12,10))
se = test.title.value_counts().sort_values(ascending=True)
se.plot.barh()
plt.title("number of event title(test.csv)")
plt.xticks(rotation=0)
plt.show()

plt.rcParams.update({'font.size': 12})

fig = plt.figure(figsize=(12,10))
se = test.event_code.value_counts().sort_values(ascending=True)
se.plot.barh()
plt.title("Number of event code (test.csv)")
plt.xticks(rotation=0)
plt.show()

import numpy as np
my_pal = sns.color_palette(n_colors=10)

test['game_time'].apply(np.log1p) \
    .plot(kind='hist',
          figsize=(15, 5),
          bins=100,
          title='Log Transform of game_time (test.csv)',
          color=my_pal[0])
plt.show()

"""The distribution is similar between Train and Test.

### EDA for **train_label**

The outcomes in this competition are grouped into 4 groups (labeled accuracy_group in the data):

3: the assessment was solved on the first attempt

2: the assessment was solved on the second attempt

1: the assessment was solved after 3 or more attempts

0: the assessment was never solved

I started by visualizing some of these columns
"""

plt.rcParams.update({'font.size': 22})

plt.figure(figsize=(12,6))
sns.countplot(y="title", data=train_label, color="#4682B4", order = train_label.title.value_counts().index)
plt.title("Number of titles (train_label.csv)")
plt.show()

plt.rcParams.update({'font.size': 16})

se = train_label.groupby(['title', 'accuracy_group'])['accuracy_group'].count().unstack('title')
se.plot.bar(stacked=True, rot=0, figsize=(12,10))
plt.title("Number of accuracy group (train_label.csv)")
plt.show()

train['log1p_game_time'] = train['game_time'].apply(np.log1p)
fig, ax = plt.subplots(figsize=(15, 5))
sns.catplot(x="type", y="log1p_game_time",
            data=train.sample(10000), alpha=0.5, ax=ax);
ax.set_title('Distribution of log10(game_time) by Type (train.csv)')
plt.close()
plt.show()
fig, ax = plt.subplots(figsize=(15, 5))
sns.catplot(x="world", y="log1p_game_time",
            data=train.sample(10000), alpha=0.5, ax=ax);
ax.set_title('Distribution of log10(game_time) by World (train.csv)')
plt.close()
plt.show()

"""## Feature Engineering

1. Feature: total unique count
"""

# 1. Title count per installation_id
feature = pd.DataFrame(index=train_label.installation_id.unique()) #Create a empty dataframe
titleCount = train.groupby('installation_id')['title'].nunique()
codeCount = train.groupby('installation_id')['event_code'].nunique()
IDCount = train.groupby('installation_id')['event_id'].nunique()
WorldCount = train.groupby('installation_id')['world'].nunique()
TypeCount = train.groupby('installation_id')['type'].nunique()
GamCount = train.groupby('installation_id')['game_session'].nunique()
#Maximum duration among different ins
durMax = train.groupby('installation_id')['game_time'].max()

feature = pd.concat([feature, titleCount,codeCount,IDCount,WorldCount,TypeCount,GamCount,durMax], axis=1, sort=False)

feature.columns = ['title_Count(ins)','Event_code_Count(ins)'
,'Event_id_Count(ins)','World_Count(ins)','Type_Count(ins)','Game_Count(ins)','Max_Duration(ins)']
feature

x = train.groupby(['installation_id','type']).count()
fourCount = x['event_id']

fourCountSeries = fourCount.index.to_series()
insCountTable = [fourCountSeries.iloc[i][0] for i in range(len(fourCountSeries))]
insCountTable = list(set(insCountTable))

tempDf = pd.DataFrame(index = insCountTable, columns = ['Activity','Assessment','Clip','Game'])
for i in range(len(insCountTable)):
  Ins = insCountTable[i]
  for j in range(len(fourCount.loc[Ins])):
    Index = fourCount.loc[insCountTable[i]].index[j]
    #print(Ins)
    tempDf.loc[Ins,Index] =  fourCount.loc[insCountTable[i],Index]
# tempDf['Activity'] = [fourCount.loc[index[i]].loc['Activity'] for i in range(len(insCountTable))]

feature = pd.concat([feature, tempDf], axis=1, sort=False)

# tempDf
feature = feature.rename(columns =  {'Activity': 'Activity_num(ins)', 'Assessment':'Assessment_num(ins)', 'Clip':'Clip_num(ins)','Game':'Game_num(ins)'})
feature = feature.fillna(0)#fill nan

feature

"""Additional features:
Seperated unique count

event_code count for different code
"""

# event code
ECCT = train.event_code.unique().tolist() #EventCodeCountTable
# ECCT = ['event_code_'+ str(eventCodeCountTable[i]) for i in range(len(eventCodeCountTable))]
# eventCodeDF = pd.DataFrame(index = insCountTable, column)

eventCode = train.groupby(['installation_id','event_code']).count()

# eventCode
eventCodeCount = eventCode['event_id']
tempDf = pd.DataFrame(index = insCountTable, columns = ECCT)
for i in range(len(insCountTable)):
  Ins = insCountTable[i]
  print("Progress: {}%".format(round(i/len(insCountTable)*100,2)))
  for j in range(len(eventCodeCount.loc[Ins])):
    Index = eventCodeCount.loc[insCountTable[i]].index[j]
    #print(Ins)
    tempDf.loc[Ins,Index] =  eventCodeCount.loc[insCountTable[i],Index]
# tempDf['Activity'] = [fourCount.loc[index[i]].loc['Activity'] for i in range(len(insCountTable))]

eventCode['event_id'].loc[insCountTable[0]].index[0]

tempDf = tempDf.fillna(0)
tempDf = tempDf.add_prefix('event_code_')
feature = pd.concat([feature,tempDf], axis=1, sort=False)

"""Similarly, we could do similar jobs for world, ... and ..."""

feature.to_csv(r'/content/drive/My Drive/E6893 Project dataset/feature_1.csv')

"""Reload the feature from file."""

feature  = pd.read_csv(DATA+'feature_1.csv', index_col=0)

feature.index.name= 'installation_id'
feature.groupby('installation_id').first()

"""Title group and find unique count for other"""

eventTitle= train.groupby(['installation_id','title']).count()
eventTitleList = train.title.unique().tolist()

# Title
ETCount = eventTitle['event_id']
tempDf = pd.DataFrame(index = insCountTable, columns = eventTitleList)
for i in range(len(insCountTable)):
  Ins = insCountTable[i]
  print("Progress: {}%".format(round(i/len(insCountTable)*100,2)))
  for j in range(len(ETCount.loc[Ins])):
    Index = ETCount.loc[insCountTable[i]].index[j]
    #print(Ins)
    tempDf.loc[Ins,Index] =  ETCount.loc[insCountTable[i],Index]
# tempDf['Activity'] = [fourCount.loc[index[i]].loc['Activity'] for i in range(len(insCountTable))]

tempDf = tempDf.fillna(0)
tempDf = tempDf.add_prefix('title_')
feature = pd.concat([feature,tempDf], axis=1, sort=False)

feature

eventWorld= train.groupby(['installation_id','world']).count()
eventWorldList = train.title.unique().tolist()

# Title
EWCount = eventWorld['event_id']
tempDf = pd.DataFrame(index = insCountTable, columns = eventTitleList)
for i in range(len(insCountTable)):
  Ins = insCountTable[i]
  print("Progress: {}%".format(round(i/len(insCountTable)*100,2)))
  for j in range(len(EWCount.loc[Ins])):
    Index = EWCount.loc[insCountTable[i]].index[j]
    #print(Ins)
    tempDf.loc[Ins,Index] =  EWCount.loc[insCountTable[i],Index]
# tempDf['Activity'] = [fourCount.loc[index[i]].loc['Activity'] for i in range(len(insCountTable))]

tempDf = tempDf.fillna(0)
tempDf = tempDf.add_prefix('world_')
feature = pd.concat([feature,tempDf], axis=1, sort=False)

feature

"""Count how many assessment(type) in the job."""

eventType= train.groupby(['installation_id','type']).count()
eventTypeList = train.title.unique().tolist()
# Title
ETCount = eventType['event_id']
tempDf = pd.DataFrame(index = insCountTable, columns = eventTypeList)
for i in range(len(insCountTable)):
  Ins = insCountTable[i]
  print("Progress: {}%".format(round(i/len(insCountTable)*100,2)))
  for j in range(len(ETCount.loc[Ins])):
    Index = ETCount.loc[insCountTable[i]].index[j]
    #print(Ins)
    tempDf.loc[Ins,Index] =  ETCount.loc[insCountTable[i],Index]
# tempDf['Activity'] = [fourCount.loc[index[i]].loc['Activity'] for i in range(len(insCountTable))]
tempDf = tempDf.fillna(0)
tempDf = tempDf.add_prefix('type_')
feature = pd.concat([feature,tempDf], axis=1, sort=False)

pd.set_option('display.max_columns', 500)
feature.columns

# feature.to_csv(r'/content/drive/My Drive/E6893 Project dataset/feature_2.csv')

"""# JUMP HERE AFTER  train data loading and process"""

import pandas as pd
feature  = pd.read_csv('/content/drive/My Drive/E6893 Project dataset/feature_2.csv', index_col=0)

feature

game_time = pd.DataFrame({ 'game_session':train.game_session,'game_time':train.game_time})

game_time.index = train.installation_id

totalDuration = game_time.groupby(['installation_id','game_session']).max()

totalDuration = totalDuration.groupby('installation_id').sum()

totalDuration = totalDuration.fillna(0)
totalDuration = totalDuration.add_prefix('total_')
feature = pd.concat([feature,totalDuration], axis=1, sort=False)

feature

test.groupby('installation_id').last().title.unique()

train_label.title.unique()

small_labels = train_label[['installation_id', 'accuracy_group']].set_index('installation_id')

train_joined = feature.join(small_labels).dropna()

train_joined

AssTit = train_label.title
AssTitDict = dict(zip(list(AssTit.unique()),range(5)))
AssTitSeries = list(AssTit.map(AssTitDict))
train_joined.insert(0,'Assessment_type(input)',AssTitSeries)

AssTitDict

AssTit

train_joined.to_csv('/content/drive/My Drive/E6893 Project dataset/train_joined.csv')

"""# All front end need is here!"""

import pandas as pd
train_joined= pd.read_csv('/content/drive/My Drive/E6893 Project dataset/train_joined.csv',index_col =0)
train_joined

"""## Train"""

def cpmp_qwk(a1, a2, max_rat=3) -> float:
    """
    A ultra fast implementation of Quadratic Weighted Kappa (QWK)
    Source: https://www.kaggle.com/c/data-science-bowl-2019/discussion/114133
    
    :param a1: The ground truth labels
    :param a2: The predicted labels
    :param max_rat: The maximum target value
    
    return: A floating point number with the QWK score
    """
    assert(len(a1) == len(a2))
    a1 = np.asarray(a1, dtype=int)
    a2 = np.asarray(a2, dtype=int)

    hist1 = np.zeros((max_rat + 1, ))
    hist2 = np.zeros((max_rat + 1, ))

    o = 0
    for k in range(a1.shape[0]):
        i, j = a1[k], a2[k]
        hist1[i] += 1
        hist2[j] += 1
        o +=  (i - j) * (i - j)

    e = 0
    for i in range(max_rat + 1):
        for j in range(max_rat + 1):
            e += hist1[i] * hist2[j] * (i - j) * (i - j)

    e = e / a1.shape[0]

    return 1 - o / e

def ins_split(train_joined,seed):
  #Only split the installation id to two groups, train_ins and test_ins
  train_joined.index.name= 'installation_id'
  ins_dataset = train_joined.groupby('installation_id').first()
  train_set, test_set = train_test_split(ins_dataset, test_size=0.2, random_state = seed)
  train_ins = train_set.index
  test_ins = test_set.index
  return train_ins,test_ins

from sklearn.model_selection import train_test_split
import numpy as np
import random
def ins_extract(ins,train_joined,method, seed):
  #Select one of the assessment for each ins_id, should be random!
  target_set = train_joined[train_joined.index.isin(ins)]
  if method == 'default':
    ins_dataset = target_set.groupby('installation_id').first()
  elif method == 'random':
    random.seed(seed)
    ins_dataset = target_set.groupby('installation_id').apply(lambda x :x.iloc[random.choice(range(0,len(x)))])
  return ins_dataset  #Split train_set, test_set (with accuracy group!!)

import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import numpy as np

from sklearn.model_selection import KFold

def lgb_training(train_set, seed2 =2019):

  X = train_set.drop(columns='accuracy_group').values
  y = train_set['accuracy_group'].values

  kf = KFold(n_splits=5, random_state=seed2)
  evals_result = {}
  for train, val in kf.split(X):
    x_train, x_val , y_train, y_val= X[train],X[val],y[train],y[val]
      # y_train = train_joined.groupby[]
      # x_val_joined = x_val.join(small_labels).dropna()
    lgb_train_set = lgb.Dataset(x_train, y_train)
    lgb_val_set = lgb.Dataset(x_val, y_val)

    params = {
        'learning_rate': 0.01,
        'bagging_fraction': 0.9,
        'feature_fraction': 0.9,
        'num_leaves': 50,
        'lambda_l1': 0.1,
        'lambda_l2': 1,
        'metric': 'multiclass',
        'objective': 'multiclass',
        'num_classes': 4,
        'random_state': 2019
      }

  model = lgb.train(params, lgb_train_set, evals_result=evals_result,num_boost_round=5000,
                    early_stopping_rounds=50, valid_sets=[lgb_train_set, lgb_val_set], verbose_eval=50)
  return model, lgb_train_set, lgb_val_set ,evals_result


def prediction(model, test_set):
  X_test = test_set.drop(columns = 'accuracy_group').values
  y_test = test_set['accuracy_group'].values

  y_pred = model.predict(X_test)
  label_pred = [y_pred[i].argmax() for i in range(len(y_pred))]
  score = cpmp_qwk(y_test,label_pred)
  print('Quadratic Kappa Weighted score: {}'.format(score))
  # if kwargs.get("verbose_eval"):
  #             print("\n" + "="*50 + "\n")

  return y_pred, score

import scikitplot as skplt
import matplotlib.pyplot as plt
def aucplot(test_set, y_pred):
  y_true = test_set['accuracy_group'].values
  y_probas = y_pred
  skplt.metrics.plot_roc_curve(y_true, y_probas)
  plt.show()

def featureImportance(model,train_joined):
  featureRank = model.feature_importance()
  featureName = train_joined.columns[:-1]
  featureDict = dict(zip(featureName,featureRank))
  import heapq
  top10 = heapq.nlargest(20, featureDict, key=featureDict.get)
  top10_value = [featureDict[i] for i in top10]
  top10.reverse()
  plt.rcParams.update({'font.size': 12})
  fig = plt.figure(figsize=(12,10))
  se= pd.Series(data = top10_value).sort_values(ascending=True)
  se.index = top10
  se.plot.barh()
  plt.title("Feature importance")
  plt.xticks(rotation=0)
  plt.tight_layout()
  # plt.savefig('/content/drive/My Drive/E6893 Project dataset/fp_model_rand.png')
  plt.show()
  return 0

def curvePlot(evals_result):
  train_logloss = evals_result['training']['multi_logloss']
  valid_logloss = evals_result['valid_1']['multi_logloss']
  plt.plot(train_logloss)
  plt.plot(valid_logloss)
  plt.legend(['train_logloss','valid_logloss'])
  plt.title('Loss curve')
  plt.xlabel('Iteration')
  plt.ylabel('logloss')
  plt.tight_layout()
  # plt.savefig('/content/drive/My Drive/E6893 Project dataset/loss_model_rand.png')
  plt.show()

from sklearn.model_selection import KFold

def test_split_frontEnd(test_set,seed = 6893):
  #Spilt the testset to 5 subset to interact at front end
  test_a, test_b = train_test_split(test_set, test_size=0.5, random_state = seed)
  test1, test2 = train_test_split(test_a, test_size=0.5, random_state = seed+1)
  test3, test4 = train_test_split(test_b, test_size=0.5, random_state = seed+2)
  return test1,test2,test3,test4 #Split train_x,y and val_x,y

# test1,test2,test3,test4 = test_split_frontEnd(test_set)
# test1.to_csv('/content/drive/My Drive/test1.csv')
# test2.to_csv('/content/drive/My Drive/test2.csv')
# test3.to_csv('/content/drive/My Drive/test3.csv')
# test4.to_csv('/content/drive/My Drive/test4.csv')

"""# First thing in training, split the installation id in to two group, and regard it as a fixed target used in all the model! 

##Front end, test it with splitting test1,2,3,4
"""

train_ins, test_ins = ins_split(train_joined,1997)

train_ins

"""# ins_extraction: formalize the trainset and test set by extract one of record following some rules, and the testset always follow random and stored."""

test_set = ins_extract(test_ins,train_joined,'random', 6893)

test_ins

test_set1,test_set2,test_set3,test_set4 = test_split_frontEnd(test_set,seed = 6893)

test_set1

"""# Feature selection : Correlation and Corr as label"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
ins_attribute = train_joined.columns[1:12]
event_code_attr = train_joined.columns[13:54]
title_attr = train_joined.columns[55:98]
world_attr = train_joined.columns[99:147]
type_attr = train_joined.columns[148:]

corr1 = train_joined[ins_attribute].corr()
sns.heatmap(corr1)
plt.title('ins_attribute')

corr3 = train_joined[title_attr].corr()
sns.heatmap(corr3)
plt.title('title_attribute')

corr2 = train_joined[event_code_attr].corr()
sns.heatmap(corr2)
plt.title('event_code_attr')

"""# Baseline model: Score: 0.689 0.598, 0.692, 0.703"""

import json
train_ins, test_ins = ins_split(train_joined,1997)
#Function calling to implement training
train_set = ins_extract(train_ins,train_joined,'default', 6893)
test_set = ins_extract(test_ins,train_joined,'random', 6893)
#models:

#baseline model: 
#Training
model, lgb_train_set, lgb_val_set ,evals_result = lgb_training(train_set, seed2 =2019)
# with open('/content/drive/My Drive/E6893 Project dataset/evals_result_baseline.json', 'w') as fp:
#     json.dump(evals_result, fp)

test_set1,test_set2,test_set3,test_set4 = test_split_frontEnd(test_set,seed = 6893)

#Prediction
y_pred1, score1 = prediction(model, test_set1)
y_pred2, score2 = prediction(model, test_set2)
y_pred3, score3 = prediction(model, test_set3)
y_pred4, score4 = prediction(model, test_set4)
print([score1,score2,score3,score4])

# #AUC plot
aucplot(test_set2,y_pred2)

# #loss plot 
curvePlot(evals_result)

# #feature importance
featureImportance(model,train_joined)

# test_set1.to_csv('/content/drive/My Drive/E6893 Project dataset/test1.csv')
# test_set2.to_csv('/content/drive/My Drive/E6893 Project dataset/test2.csv')
# test_set3.to_csv('/content/drive/My Drive/E6893 Project dataset/test3.csv')
# test_set4.to_csv('/content/drive/My Drive/E6893 Project dataset/test4.csv')

"""# Model 2: with random choice (1 time)
##High variance 
## not good score 0.66 0.60 0.68, 0.69
"""

import json
#Function calling to implement training
train_ins, test_ins = ins_split(train_joined,1997)
#Function calling to implement training
train_set = ins_extract(train_ins,train_joined,'random', 6893)
test_set = ins_extract(test_ins,train_joined,'random', 6893)
#models:

#baseline model: 
#Training
model, lgb_train_set, lgb_val_set ,evals_result = lgb_training(train_set, seed2 =2019)
# with open('/content/drive/My Drive/E6893 Project dataset/evals_result_baseline.json', 'w') as fp:
#     json.dump(evals_result, fp)
test_set1,test_set2,test_set3,test_set4 = test_split_frontEnd(test_set,seed = 6893)

#Prediction

y_pred, score1 = prediction(model, test_set1)
y_pred, score2 = prediction(model, test_set2)
y_pred, score3 = prediction(model, test_set3)
y_pred, score4 = prediction(model, test_set4)
print([score1,score2,score3,score4])

# #AUC plot
aucplot(test_set4,y_pred)

# #loss plot 
curvePlot(evals_result)

# #feature importance
featureImportance(model,train_joined)

evals_result
with open('/content/drive/My Drive/E6893 Project dataset/loss_2.json', 'w') as fp:
    json.dump(evals_result, fp)

evals_result
with open('/content/drive/My Drive/E6893 Project dataset/loss_3.json', 'w') as fp:
    json.dump(evals_result, fp)

"""#Model 3: More randomness"""

import json
N=20
y_total = 0
train_ins, test_ins = ins_split(train_joined,1997)
#Function calling to implement training

train_set = ins_extract(train_ins,train_joined,'random', 6893)
test_set = ins_extract(test_ins,train_joined,'random', 6893)

seed =1
for randomstate in range(N):
#Function calling to implement training
  train_set = ins_extract(train_ins,train_joined,'random', seed)
  #train_set,test_set = train_split(train_joined,6893,'default',randomstate)
  #models:
  #Training
  model, lgb_train_set, lgb_val_set ,evals_result = lgb_training(train_set, seed2 =2019)
  # with open('/content/drive/My Drive/E6893 Project dataset/evals_result_baseline.json', 'w') as fp:
  #     json.dump(evals_result, fp
  #Prediction
  y_pred, score = prediction(model, test_set2)
  y_total = y_total+y_pred
  seed=seed+1
#AUC plot

y_pred = y_total/N
aucplot(test_set2,y_pred)

# #loss plot 
curvePlot(evals_result)

# #feature importance
featureImportance(model,train_joined)

# test_set1.to_csv('/content/drive/My Drive/test1_final.csv')
# test_set2.to_csv('/content/drive/My Drive/test2_final.csv')
# test_set3.to_csv('/content/drive/My Drive/test3_final.csv')
# test_set4.to_csv('/content/drive/My Drive/test4_final.csv')

"""# Feature importance  0.676, 0.67, 0.7368, 0.72051  N =20"""

#Train baseline model first, then use the importance to get new model
import json
train_ins, test_ins = ins_split(train_joined,1997)
#Function calling to implement training
train_set = ins_extract(train_ins,train_joined,'random', 6893)
test_set = ins_extract(test_ins,train_joined,'random', 6893)

baseline, lgb_train_set, lgb_val_set ,evals_result = lgb_training(train_set, seed2 =2019)

featureRank = baseline.feature_importance()
featureName = train_joined.columns[:-1]
featureDict = dict(zip(featureName,featureRank))
N = 100

import heapq
topX = heapq.nlargest(N, featureDict, key=featureDict.get)
topX_value = [featureDict[i] for i in topX]

train_imp = train_joined[topX]
train_imp['accuracy_group'] = train_joined['accuracy_group']
train_imp
#New model

import json
#Function calling to implement training
#train_set,test_set = train_split(train_joined,6893,'default',randomstate)
train_set = ins_extract(train_ins,train_imp,'random', 6893)
test_set = ins_extract(test_ins,train_imp,'random', 6893)
#models:
test_set1,test_set2,test_set3,test_set4 = test_split_frontEnd(test_set,seed = 6893)
 # test1,test2,test3,test4 = test_split_frontEnd(test_set)
test_set1.to_csv('/content/drive/My Drive/test1_final.csv')
test_set2.to_csv('/content/drive/My Drive/test2_final.csv')
test_set3.to_csv('/content/drive/My Drive/test3_final.csv')
test_set4.to_csv('/content/drive/My Drive/test4_final.csv')
#baseline model: 
#Training
model, lgb_train_set, lgb_val_set ,evals_result = lgb_training(train_set, seed2 =2019)
# with open('/content/drive/My Drive/E6893 Project dataset/evals_result_baseline.json', 'w') as fp:
#     json.dump(evals_result, fp)

#Prediction
y_pred, score1 = prediction(model, test_set1)
y_pred, score2 = prediction(model, test_set2)
y_pred, score3 = prediction(model, test_set3)
y_pred, score4 = prediction(model, test_set4)
print([round(score1,3),round(score2,3),round(score3,3),round(score4,3)])

# #AUC plot
aucplot(test_set4,y_pred)

# #loss plot 
curvePlot(evals_result)

# #feature importance
featureImportance(model,train_imp)

"""# Test Set Actual"""

from sklearn.externals import joblib
#lr是一个LogisticRegression模型
joblib.dump(model1, '/content/drive/My Drive/model_fp_final1.model')
# classifier2 = joblib.load('svm.model')

submit = pd.read_csv('/content/drive/My Drive/E6893 Project dataset/sample_submission.csv',index_col= 0)

submit.inse


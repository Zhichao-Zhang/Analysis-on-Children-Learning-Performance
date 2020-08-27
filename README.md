# Analysis-on-Children-Learning-Performance
Big data project: Analysis-on-Children-Learning-Performance

## Dataset: 
The data used in this project is anonymous, tabular data of interactions with an app called PBS KIDS Measure Up! These datasets are collected from Kaggle, including train set.csv，train_label.csv and test.csv. The app is a game-based learning tool for kids, and the dataset includes users' assessment scores and their records through the game.

The train dataset we used includes 11341,042 rows of different event data in Json format from 303,319 different game sessions of 17000 installation id.

## Language:
python, javascript, html, css; platform:flask

## Analytics: 
Analytics and algorithm: Basic data preprocssing and EDA methods using Pandas; Oversampling and downsampling, bagging algorithm. Train/test split and KFold cross validation methods using sklearn, tree-based machine learning model in LightGBM.

## Visualization:
In front-end, we use HTML, CSS and JavaScript to do visualization. What we show in the front-end is the performance, indicated by ROC curve, Feature Importance and Loss Curve, of different models in different datasets, which user can choose freely from the four datasets we generated randomly.

## System procedure: 
In the respect of system design, we use Flask as our framework to connect the fron-end and back-end. In back-end, we used Python as our primary language, and run the model on datasets, generate ROC cure, then send it to the web in front-end through Flask in Ajax manner.

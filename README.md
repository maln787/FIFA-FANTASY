# FIFA FANTASY

Project Summary 

Using a dataset from Kaggle containing records for each player and their attributes in the Fifa Video Game during the 2019-2022 Version, our database application will provide an interactive attribute summary aimed at FIFA enthusiasts who are interested and can use data to learn about historical comparisons of players and to create their own competitive team. The data also allows multiple comparisons for the same players across the last 3 versions of the videogame.
 
Project Description

Objectives:
- The objective of this project is to create a user-friendly website for the users to retrieve statistics of the different players or different variants of players - across the FIFA platform for the analysis and create their own competitive team and compare with others.
- To allow users to have a seamless experience when looking at all their FIFA players of interest.
- FIFA being a major attraction for today’s youth, our main aim towards taking this dataset was to ensure that our fellow classmates, TAs, and professors enjoy - -  - reading through it and compare players on multiple parameters in the last 8 versions of the videogame.
- Give users the accessibility to see all the existing FIFA players and give them reviews/recommendations/features all in one place
- At the end of this project, we plan on learning how to interact with data: the basic CRUD(Create, Read, Update and Delete) operations and visualizing the results.


Dataset: Link: https://www.kaggle.com/stefanoleone992/fifa-22-complete-player-dataset?select=players_22.csv

The Dataset has been taken from Kaggle, where it was uploaded by Stefano Leone and scraped from the publicly available website sofifa.com. We have extracted the football players' data in the Fifa 2020- 2022 game. The dataset contains a total data point of approximately 60,000.
Link: https://www.kaggle.com/stefanoleone992/fifa-22-complete-player-dataset?select=players_22.csv
In total, the dataset includes 110 attributes of a player. Some attributes are mentioned below: 
Every player available in FIFA 20, 21 and 22
URL of the scraped players
URL of the uploaded player faces, club and nation logos
Player positions, with the role in the club and in the national team
Player attributes with statistics as Attacking, Skills, Defense, Mentality, GK Skills, etc.
Player personal data like Nationality, Club, DateOfBirth, Wage, Salary, etc.
The mean age of the players is 25.2 with a standard deviation of 4.7 years.
The average player's overall rating is 65.7 with a standard deviation of 7 points.
The average player weekly wage (in EUR) is 9.15k with a standard deviation of 19.9k.
 
The dataset does contain null values in columns like club_loaned_from, player_tags, nation_logo_url, etc. and these are optional features so we can drop them or we can easily fill in for the null values. The dataset will require cleaning so that when we fetch our results and null values come up, this is going to degrade the quality of our website.




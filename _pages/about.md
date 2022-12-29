---
permalink: /
title: "Adventure Seeking on Hiking Tracks in the Central European zone: A Geospatial Analysis and Recommendation System"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

This geospatial project investigates the adventure-seeking behavior of hikers on trails in the Central European zone. The main goal is to understand the factors that influence the choice of a particular track and to develop a recommendation system for hikers based on their preferences and needs. To achieve this objective, I used a combination of spatial analysis techniques, field data collection, and machine learning algorithms. The study analyzed a wide range of variables such as track difficulty, distance and elevation gain, as well as the demographic characteristics and habits of hikers. The results provide valuable insights for the management and promotion of hiking trails in the Central European zone and can help improve the outdoor recreation experiences of hikers by suggesting suitable tracks based on their individual preferences and goals.


Project structure
------
The study was divided into two main areas: data collection and spatial analysis. In the data collection phase, I gathered a wide range of tracks coming from the website hikr.org through the License: CC0, after I cleaned and processed the data to ensure its quality and consistency. In the spatial analysis phase, I used a variety of tools and techniques in order to examine the characteristics and features of hiking tracks in the Central European zone.

Analysis workflow
------

The analysis workflow is divided into three main files: analysis_1/2/3.py.

* analysis_1.py: In this file, I used the geopandas library to perform spatial analysis on the hiking tracks. The analysis included the calculation of new columns useful to study the data, such as the season of the year or the number of tracks per user, after one example of track is shown in order to have a better understanding of the data.

![Track Example](/images/track_example.png)

* analysis_2.py: Here deeper analysis have been performed. In order to cover the larger part of the topics studied during the course I: found the circle tracks, by extracting the starting and finishing points and comparing them by distance, performed map matching, by searching for intersactions between the tracks and the reference map of GraphHopper, and finally I calculated the so called "intresting points" so the points in the same tracks where a significant number of people have stopped for a while (this can suggest us that there is a natural attraction, lakes or waterfalls, a hut or a refreshment area).

![Intresting points](/images/intresting_points.png)

* analysis_3.py: In this file I used the scikit-learn library to perform machine learning algorithms. The analysis included the calculation of the most important features for the prediction of the track difficulty. After a reccomendation system has been developed, which is based on the user's preferences and goals. Running the code the name of a existing user will be asked and the system will suggest the best tracks for him/her.
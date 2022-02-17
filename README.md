# Dissertation of Jacob M. Pearl
### Applications of Machine Learning and Network Science for the Study of Congressional Polarization in the U.S.

This dissertation uses unsupervised machine learning (topic models), supervised machine learning (classification analysis), and network science to ask multiple questions pertaining to political polarization in the U.S. House of Representatives between 1983 to 2016. In this research I use the congressional record to analyze patterns of speech within and between the Democrat and Republican parties. Questions this dissertation address include, _have the agendas expressed by the two parties become more distinct over time (agenda polarization)?, have the ways in which the parties discuss political issues become more distinct over time (frame polarization)?, and have the associations between ideas within the political parties discourse changed over time (belief network analysis/ideological polarization)?_

#### Dissertation chapters and associated notebooks
**Chapter 1: Dynamic Topic Model**    
--> `Dynamic_Topic_Models.ipynb` - build dynamic topic model  
--> `External validity check.ipynb` - checks trends in topics with real world events

**Chapter 2: Agenda Polarization**  
--> `Classification_analysis.ipynb` - runs all classification analysis models  
--> `Visualize_classification_results.ipynb` - R ggplot descriptive graphs for classification analysis  
--> `Evaluating_predictive_coefs.ipynb` - R ggplot descriptive graphs of classification coefs

**Chapter 3: Frame Polarization**  
--> `Frame_Analysis.ipynb` - Distance and Polarization measures of word choice within topics
-->  `Visualize_framing_results.Rmd`  - R ggplot descriptive graphs for framing analysis and gt tables

**Chapter 4: Belief Network Polarization**

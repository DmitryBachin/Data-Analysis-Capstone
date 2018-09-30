# The analysis of weather events.
The capstone from the course "Data Analysis and Interpretation" provided by Wesleyan University
The code is written for the final project by Dmitry Bachin
The course is organized by Wesleyan University (USA) through Courseta.org


**Variables**
The file variables.py contain variables which are used in the analysis. 
More details about the variables and the data set itself can be found in the files:<br>
data_related/Storm Event Data Codebook.pdf<br>
data_related/NWS Storm Event Data Documentation.pdf



**Data management**
As a response variable the "damage_property" was chosen. Because most values of this variables are zeros, the research was divided in two parts
1) Create a binary categorical variable which means whether some property was damaged(1) or not(0). To perform the analysis univariate, bivariate and machine learning approaches were used. From the sample were excluded all observations where the damage property was not estimated(missing variables)
2) Create a damage property variable and exclude all data where the damage property was not estimated properly or equals zero. Because of high positive skewness all values were logarithmed with a base 10. To perform the analysis univariate, bivariate and regression approaches were used. <br>

The states were united in climate categories based on the map: 
![Image](https://www.ncdc.noaa.gov/monitoring-references/maps/images/us-climate-regions.gif "icon")
The source: https://www.ncdc.noaa.gov/monitoring-references/maps/us-climate-regions.php
The dictrict of Columbia was added to Northeast climate region. Alaska was puted separately because all other places which are not from the map above, were ocean/see related and mostly located in equatorial climate. 

Other explanatory variables included the type of the event, did it took place on the county or zone level, the month when the event took place and the event duration.


**Univariate analysis**
All results will be shown if one runs the program.
Every categorical variable was examined through bar chart and the number of observation in each category was compared.<br>
To analyze quantitative variables histograms were used.

**Bivariate analysis**
All results will be shown if one runs the program.
With the categorical response variables, Chi-square test was performed. The event duration was not used as explanatory variable in this part of analysis. As a post hoc test, the Tukey test was used. THe result of post hoc test are presented in the results folder. If the difference between pairs was significant, mean difference was provided. Otherwise, nothing except the underscore written in the cell. <br>
With the quantitative response variable, the analysis of variance(ANOVA) was performed. As a post hoc test the Bonferroni adjustment was used. The result are presented in the results folder. If the difference between pairs is significant, p-value of this comparison was provided. Otherwise the underscore was written in the cell.<br>
The Pearson correlation was used to find the association between event duration and damage propery amount. However, no association was found.


**Regression analysis**
To perform the analysis of damage property, multiple regression was performed. The result will be on the screen if one runs the program.

**Machine learning**
The visualisation of decision tree performed by GraphViz. To use it, one needs not only meet the requirements.txt but install GraphViz on computer if it is not done before. Anyway the decision tree can be found in the results folder in the png file.<br>
To analyze what can be associated with the fact of damage property Random Forest and Decision Tree methods was used.
To deal with variables with many categories One Hot Encoding was performed.
The results of Random forest will be shown if one runs the program.
Because the plot of the number of tree has shown that the model is pretty precise (83-87%) even with one decision tree, the decision tree analyses was performed and the tree was pruned and visualized.

 

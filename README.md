# The analysis of weather events.
The capstone from the course "Data Analysis and Interpretation" provided by Wesleyan University
The code is written for the final project by Dmitry Bachin
The course is organized by Wesleyan University (USA) through Courseta.org

The detailed final report can be found in final-report.pdf in the root directory.


**Variables**


The file variables.py contain variables which are used in the analysis. 
More details about the variables and the data set itself can be found in the files:<br>
data_related/Storm Event Data Codebook.pdf<br>
data_related/NWS Storm Event Data Documentation.pdf



**Data management**


The property damage was chosen as a response variable. Because most values of this variables are zeros, the research was divided into two parts:
1) Create a binary categorical variable which means whether some property was damaged(1) or not(0). To perform the analysis univariate, bivariate and machine learning approaches were used. From the sample were excluded all observations where the property damage was not estimated(missing variables)
2) Create a damage property variable and exclude all data where the property damage was not estimated properly or equals zero. Because of high positive skewness, all quantitative values were logarithmic with a base 10. The analysis univariate, bivariate and regression approaches were performed with the sample.  <br>

The states were united in climate categories based on the map: 
![Image](https://www.ncdc.noaa.gov/monitoring-references/maps/images/us-climate-regions.gif "icon")
The source: https://www.ncdc.noaa.gov/monitoring-references/maps/us-climate-regions.php
The dictrict of Columbia was added to Northeast climate region. Alaska was puted separately because all other places which are not from the map above, were ocean/see related and mostly located in equatorial climate. 

Explanatory variables included the type of the event, the event type designator,  the month when it was observed,  the climate region where it happened and the event duration.


**Univariate analysis**


All results will be shown if one runs the univariate_analysis.py file. 
Every categorical variable was examined through frequency tables. To analyze quantitative variables histograms were used.

**Bivariate analysis**

All results will be shown if one runs the bivariate_analysis.py file.
With the categorical response variables, the Chi-square test was performed. The event duration was not used as an explanatory variable in this part of the analysis. As a post hoc test, the Tukey test was used. The result of posthoc test is presented in the results folder. If the difference between pairs was significant, the mean difference was provided. Otherwise, nothing except the underscore written in the cell. <br>
With the quantitative response variable, the analysis of variance(ANOVA) was performed. As a posthoc test, the Bonferroni adjustment was used. The result is presented in the results folder. If the difference between pairs is significant, a p-value of this comparison was provided. Otherwise, the underscore was written in the cell.<br>
The Pearson correlation was used to find the association between event duration and damage property amount. However, no association was found.


**Regression analysis**


To perform the analysis of property damage, multiple regression was performed. The result will be on the screen if one runs the regression_model.py file.

**Machine learning**


All results will be shown if one runs the machine_learning_tools.py file.
The visualization of decision tree performed by GraphViz. To use it, one needs not only meet the requirements.txt but install GraphViz if it is not done before. Anyway, the decision tree can be found in the results folder in the png file or in the final-report.pdf.<br>
To analyze what can be associated with the fact of damage property Random Forest and Decision Tree methods were used.
To deal with variables containing many categories One Hot Encoding was performed.
Because the plot of the number of trees has shown that the model is pretty precise (83-87%) even with one decision tree, the decision tree analyses were performed and the tree was pruned and visualized.


 

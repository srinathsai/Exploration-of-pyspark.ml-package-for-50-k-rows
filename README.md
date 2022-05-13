# Exploration-of-pyspark.ml-package-for-50-k-rows.

## Goal :- <br />
Exploration of how pyspark.ml package can be used on 50 k rows of dataset in starting from filtering null and out of range values of all columns, to apply linear and random forest regressions and in between identifying principal components( a key parts in regression). <br />

## Methodology :-<br />
The dataset that has been used in entire processes is from kaggle which is named as original_data.csv in repository.<br />
This orginal_data.csv is the raw data comprising of 50k rows and null values in 18 columns 0f 26 columns. So initially, which columns are having atleast one null value has been identified.<br />
Out of the 18 columns of having atleast one null value, 3 columns named greA, greV, greQ has been selected to fill the null values as they are very essential for predicting admit which will be discussed later.<br />
Next the selected three columns null values and out of range values are filled using **cosine similarity rule** (cosine angle between two vectors in a dot product) , here two vectors are beside columns values. That implies based on the closeness of beside columns values,null values and out of range values are filled . Here which columns are most closely assigned will be identified by defining cosine similarity function on two non null columns. These cosine angle values of two columns are stored in list and from list identifying which pair of columns are closely assigned.<br />
In dataset the combination industryExp and admit got more cosine angle value, so at first for the three selected columns identifying the range of all values. And out of these ranges,if any value is present in any of the selected columns then they are replaced by null values. And finally these null values are replaced with values of rows that are based on admit column.<br />
At this stage, in the whole dataset 3 columns are entirely filtered without null values.<br />

Next task is to predict any column on this filtered data. For that column named 'admit' has been chosen as predicting variable and input features as 'internExp', 'researchExp' and 'cgpa' have been chosen because it is a general sense that for getting good admit we need to have good profile that includes good intern experience, research experience and good cgpa.<br />
Therefore with these selection,how much possibility of getting admits is predicted by applying linear regression and random forest using pyspark.ml in which dataset is divided into 80 percent as training and 20 percent as testing. After their accuracies perfomances are validated using **rmse**.

## Another approach of above tasks:-
Another approach is by the use of pipelines.<br />
### Advantages of pipelines.:-
Pipelines are usually API'S that combine multiple algorithms in form of stages which reduces code complpexity but achieve same results. The task of pipelining is achieved for above tasks in the filename pipelining of above tasks.<br />

Lastly the important components for regression that are principal components have been identified using the same package.<br />



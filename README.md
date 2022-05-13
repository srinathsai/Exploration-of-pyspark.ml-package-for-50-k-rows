# Exploration-of-pyspark.ml-package-for-50-k-rows.

Goal :- <br />
Exploration of how pyspark.ml package can be used on 50 k rows of dataset in starting from filtering null and out of range values of all columns, to apply linear and random forest regressions and in between identifying principal components( a key parts in regression). <br />

Methodology :-<br />
The dataset that has been used in entire processes is from kaggle which is named as original_data.csv in repository.<br />
This orginal_data.csv is the raw data comprising of 50k rows and null values in 18 columns 0f 26 columns. So initially, which columns are having atleast one null value has been identified.<br />
Out of the 18 columns of having atleast one null value, 3 columns named greA, greV, greQ has been selected to fill the null values as they are very essential for predicting admit which will be discussed later.<br />
Next the selected three columns null values and out of range values are filled using **cosine similarity rule** (cosine angle between two vectors in a dot product) , here two vectors are beside columns values. That implies based on the closeness of beside columns values,null values and out of range values are filled . Here which columns are most closely assigned will be identified by defining cosine similarity function on two non null columns. These cosine angle values of two columns are stored in list and from list identifying which pair of columns are closely assigned.<br />
In our dataset 



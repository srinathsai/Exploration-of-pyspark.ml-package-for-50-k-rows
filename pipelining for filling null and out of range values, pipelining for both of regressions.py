# -*- coding: utf-8 -*-
"""Measuring accuracies of linear regression and random forest.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mPLklrqOGnLWh3uXSeJRbBEjkJBouvjI
"""

!pip install pyspark

from pyspark.sql import SparkSession 
spark = SparkSession.builder.appName("task-4").getOrCreate()
df_4 = spark.read.csv('/content/original_data.csv',header =True, inferSchema=True)
from pyspark.ml import Pipeline

#pipelining for task-1

from pyspark.sql import SparkSession  #Iimporting spark session.
spark = SparkSession.builder.appName("Task1").getOrCreate()
df = spark.read.csv('/content/original_data.csv',header =True, inferSchema=True)
from pyspark.sql import functions as F
cols = [f"any({col} is null) as {col}" for col in df.columns]
df.selectExpr(cols).show()
df.dtypes
df.show()

import pyspark.sql.functions as func

def cosine_similarity(df, col1, col2):
    df_cosine = df.select(func.sum(df[col1] * df[col2]).alias('dot'), 
                          func.sqrt(func.sum(df[col1]**2)).alias('norm1'), 
                          func.sqrt(func.sum(df[col2] **2)).alias('norm2'))
    d = df_cosine.rdd.collect()[0].asDict()
    return d['dot']/(d['norm1'] * d['norm2'])

x=cosine_similarity(df, 'industryExp', 'admit')
cache=[]
cache.append(x)
y=cosine_similarity(df,'researchExp','industryExp')
cache.append(y)
z=cosine_similarity(df,'researchExp','admit')
cache.append(z)
print(cache)
print("the maximum cosine similarity found observed is between columns 'industryExp','admit' with value",cache[0])

df1=df.select(df['greA'],df['greV'],df['greQ'])
df1.describe(['greA']).show()
df1.describe(['greV']).show()
df1.describe(['greQ']).show()
from pyspark.sql.types import NullType
from pyspark.sql.functions import isnan, when, count, col, lit
from pyspark.sql.window import Window
import sys

#MOST IMPORTANT PIPELINING PART OF TASK-1

df = df.withColumn('greA', when(df.greA<0, lit(None)).when(df.greA>1470.0, lit(None)).otherwise(df.greA))
df= df.withColumn("greA", func.last('greA', True).over(Window.partitionBy('admit').rowsBetween(-sys.maxsize, 0)))
df = df.withColumn('greV', when(df.greV<0, lit(None)).when(df.greV>5560, lit(None)).otherwise(df.greV))
df= df.withColumn("grev", func.last('greV', True).over(Window.partitionBy('admit').rowsBetween(-sys.maxsize, 0)))
df = df.withColumn('greQ', when(df.greQ<0, lit(None)).when(df.greQ>7990, lit(None)).otherwise(df.greQ))
df= df.withColumn("greQ", func.last('greQ', True).over(Window.partitionBy('admit').rowsBetween(-sys.maxsize, 0)))
df1=df.select(df['greA'],df['greV'],df['greQ'])
pipeline1=Pipeline(stages=[df,df1])

df1.select([count(when(isnan(c)| col(c).isNull(), c)).alias(c) for c in df1.columns]).show()
df.select([count(when( isnan(c)|col(c).isNull(), c)).alias(c) for c in df.columns]).show()

#pipelining for task-2 and task-3 in linear regression.

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import Imputer
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import Normalizer
from pyspark.ml.evaluation import RegressionEvaluator

df1=df_4.select(df_4['researchExp'],df_4['industryExp'],df_4['cgpa'],df_4['admit'])
df1.dtypes

assembler = VectorAssembler(
    inputCols=['researchExp','industryExp','cgpa'],outputCol="features")

assembler.setParams(handleInvalid="skip")
normalizer=Normalizer(inputCol="features", outputCol="featuresmodified", p=2)
(trainingData, testData) = df1.randomSplit([0.8, 0.2],50)

print("Number of train records are",trainingData.count())
print("Number of test records are",testData.count())

lm = LinearRegression(featuresCol="featuresmodified",labelCol='admit',)
pipeline = Pipeline(stages=[assembler,normalizer, lm])
model = pipeline.fit(trainingData)

prediction = model.transform(testData)

evaluator = RegressionEvaluator(
    labelCol="admit", metricName="rmse")
rmse = evaluator.evaluate(prediction)
print(rmse)

#pipelining for task-2 and task-3 in randomforest.

from pyspark.ml.classification import RandomForestClassifier

assembler2 = VectorAssembler(
    inputCols=['researchExp','industryExp','cgpa'],outputCol="features")

assembler2.setParams(handleInvalid="skip")
normalizer2=Normalizer(inputCol="features", outputCol="featuresmodified", p=2)
(trainingData2, testData2) = df1.randomSplit([0.8, 0.2],50)

print("Number of train records are",trainingData.count())
print("Number of test records are",testData.count())

rf_classifier=RandomForestClassifier(labelCol="admit",numTrees=50)
pipeline = Pipeline(stages=[assembler2,normalizer2, rf_classifier])
model2 = pipeline.fit(trainingData2)

prediction2 = model2.transform(testData2)

evaluator = RegressionEvaluator(
    labelCol="admit", metricName="rmse")
rmse = evaluator.evaluate(prediction2)
print(rmse)

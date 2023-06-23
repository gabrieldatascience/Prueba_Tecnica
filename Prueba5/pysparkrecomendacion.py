
#PySpark sistema de recomendación de museos
###Dataset: https://datos.gob.mx/busca/dataset/total-de-exposiciones-temporales-del-inba-en-el-ano-actual


from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import StringIndexer

spark = SparkSession.builder.appName("RecomendacionExposiciones").getOrCreate()

dataset_path = "exposiciones.csv"
data = spark.read.csv(dataset_path, header=True, inferSchema=True)

data = data.withColumn("Fecha inicio", data["Fecha inicio"].cast("date"))
data = data.withColumn("Fecha fin", data["Fecha fin"].cast("date"))

exposiciones_cols = ['Exposiciones permanentes', 'Exposiciones temporales', 'Exposiciones itinerantes nacionales',
                     'Exposiciones internacionales en México', 'Exposiciones nacionales en el extranjero',
                     'Total de exposiciones', 'Total de asistentes']

for col in exposiciones_cols:
    data = data.withColumn(col, data[col].cast("double"))

indexer = StringIndexer(inputCols=['Museo'], outputCols=['MuseoIndex'])
data_indexed = indexer.fit(data).transform(data)

(training, test) = data_indexed.randomSplit([0.8, 0.2])

als = ALS(maxIter=5, regParam=0.01, userCol="MuseoIndex", itemCol="MuseoIndex", ratingCol="Total de asistentes",
          coldStartStrategy="drop")
model = als.fit(training)

predictions = model.transform(test)

evaluator = RegressionEvaluator(metricName="rmse", labelCol="Total de asistentes", predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE) = " + str(rmse))

user_recs = model.recommendForAllUsers(5)
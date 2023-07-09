import findspark
findspark.init()                                                                                                                     
from pyspark import SparkContext                                                                                        
from pyspark.sql import SparkSession                                                                                    
from pyspark.streaming import StreamingContext                                                                          
#from pyspark.streaming.kafka import KafkaUtils                                                                          
from pyspark.sql import HiveContext
from pyspark import SparkConf
from datetime import datetime
import uuid
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import *

topic =  "mysql-connector-02.AIRFLOW_CFG.job"
# spark = SparkSession.builder \
#         .appName("PythonSparkStreamingKafka") \
#         .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")\
#         .config("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")\
#         .config("fs.gs.project.id", project_id)\
#         .config("fs.gs.auth.service.account.enable", "false")\
#         .config("fs.gs.auth.service.account.project.id",project_id)\
#         .config("fs.gs.auth.service.account.private.key.id",private_key_id)\
#         .config("fs.gs.auth.service.account.private.key",private_key)\
#         .config("fs.gs.auth.service.account.client.email",client_email)\
#         .config("fs.gs.auth.service.account.email",client_email)\
#         .config("fs.gs.auth.service.account.client.id",client_id)\
#         .config("fs.gs.auth.service.account.auth.uri",auth_uri)\
#         .config("fs.gs.auth.service.account.token.uri",token_uri)\
#         .config("fs.gs.auth.service.account.auth.provider.x509.cert.url",auth_provider_x509_cert_url)\
#         .config("fs.gs.auth.service.account.client_x509_cert_url",client_x509_cert_url)\
#         .config("google.cloud.auth.service.account.json.keyfile", "/Users/hungnp14/Desktop/DE/Terraform/dataproc-terraform/credentials/sawyer-work-1804-65e64232ab96.json")\
#         .master("local[*]") \
#         .getOrCreate()

spark = SparkSession.builder \
        .appName("PythonSparkStreamingKafka") \
        .master("local[*]") \
        .getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

conf = spark.sparkContext._jsc.hadoopConfiguration()
conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
conf.set("google.cloud.auth.service.account.enable", "true")
conf.set("google.cloud.auth.service.account.json.keyfile", path)


schema_main = StructType() \
            .add('id', IntegerType()) \
            .add('dag_id', StringType()) \
            .add('state', StringType()) \
            .add('start_date', TimestampType()) \
            .add('end_date', TimestampType()) \
            .add('latest_heartbeat', TimestampType()) \
            .add('hostname', StringType()) \
            .add('unixname', StringType()) \

df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("startingOffsets", "earliest") \
            .option("subscribe", topic) \
            .load() \
            .selectExpr("CAST(value AS STRING) as value")

message_schema_2 = StructType([
     StructField('before', MapType(StringType(), StringType(), True), True),
     StructField('after', MapType(StringType(), StringType(), True), True), 
     StructField('source', MapType(StringType(), StringType(), True), True),
     StructField('op', MapType(StringType(), StringType(), True), True),
     StructField('ts_ms', MapType(StringType(), StringType(), True), True),
     StructField('transaction', MapType(StringType(), StringType(), True), True)
     ]
)

# rddData = spark.sparkContext.parallelize(eg_schema)
# eg_df = spark.read.json(rddData)

after_fields = ['id', 'dag_id', 'state', 'job_type', 'start_date', 'end_date', 'latest_heartbeat','executor_class', 'hostname', 'unixname']

df = df.withColumn('msg', from_json(col("value"), message_schema_2)) \
               .select(*[F.col('msg.after').getItem(f).alias(f) for f in after_fields])

df = df.withColumn('start_date', to_timestamp(col('start_date')))\
         .withColumn('end_date', to_timestamp(col('end_date')))\
         .withColumn('latest_heartbeat', to_timestamp(col('latest_heartbeat')))\
         .withColumn('id', col('id').cast(IntegerType()))\

df = df(*columns,\
        date_format(col("start_date"), 'yyyy').alias("year"), \
        date_format(col("start_date"), 'MM').alias("month"), \
        date_format(col("start_date"), 'dd').alias("day"), \
        date_format(col("start_date"), 'HH').alias("hour"))

df.printSchema()

# df = df \
#         .writeStream \
#         .partitionBy("year", "month", "day", "hour") \
#         .format("csv") \
#         .option("checkpointLocation", "hdfs://localhost:9000//spark-write-kafka/"+topic+"/") \
#         .trigger(processingTime="5 seconds") \
#         .option("path", "hdfs://localhost:9000//spark-write-kafka/"+topic+"/") \
#         .start()

df = df  \
    .writeStream \ 
    .partitionBy("year", "month", "day", "hour") \
    .format('parquet') \
    .option('path', "gs://spark-bq-pipeline/data/"+topic+"/") \
    .option('checkpointLocation', 'gs://spark-bq-pipeline/checkpoint/') \
    .start()

df.awaitTermination()

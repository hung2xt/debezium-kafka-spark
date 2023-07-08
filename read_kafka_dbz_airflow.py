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

project_id = "sawyer-work-1804"
private_key_id = "65e64232ab965211722e3513fdcded158c559ba6"
private_key = '-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDqj61YIThkbxRf\nLzrhMLOD1wc33iaRaNb6Mm5qHO9xRIGZC1ronS39YYRTDoseaQb7kkEWIxiJfPiw\nVszJEfdYmPRtGgy3PkgM9zW1SWmghDDiz7XQZJEgvOPQwUZsXvdAYFhHh3oSuWsZ\n+UjrgiLXBfr3b4GMszH0Zaiazyyax6ybhCo9zyKcpRscT5v+IpeYG/6iYx21g51Y\n2fACDvoLbrOspG0pCHtP+s/kzVTjHz+QN76WlZMzF4FoAaeO953jOHGEBShgv854\nOZUd0MQJDEgtv40CtYdIBlh4eE8hpVNhZfZyJPyu7NntFMxiUCbygnFdoyNDl7VT\nDR+sPFJ9AgMBAAECggEAC+v/kIInvpsSuv/Ii1eRWDsep81Hwo5ElvTnPcd4uBYW\nTDQSi84pXz6MnjgYBBSsgS7e1gQ0pBBRB41x3Spnmv4zNjRjvxCQUvBhr3QqxTjS\nz0RlZlEmOza+kYaxUKLHCGOdOQ1+u+Lmuaw885Nqt+ka52aofAFDobtlBXFQQBGb\nHhLKXXB+3bdC+PyfCBdAH8z7EThv9LS15pzrVZrjYh0IjahIESZ75vKkvoo8YUYI\nhbOLoPbacnPezmxFaJJo4EGU2LrwNRocGUwsso9fGS7B+QJEaE1KKZP+NRDbjRAR\n0nUxjFxRokQ/jBX4uHaxVKWPuNt9ua/aosm5rl6GlQKBgQD7tVKyKbGdWzT2IGMK\n1aiGJsZ/hq7VaBSKJL3E6rbhsv+xZxtdhu/1EzJQ2XZXt6hi5TvMxIFgkca4siGb\nAOn4b0c2q1ho/I4P7mGyEX8uzJ69sDtMKuwliew9VNBDAicAaGYpdiFUtiOkDiPk\necP7/jetUV14UPaWFH02quW8ywKBgQDuj4Jcxx5XqkG/q/NUKIgxVUY2d0Zx3o86\n6X+ysqYGl5NPOd3Gb2gkD9vPa1Trh/bqhaDFSHk6mXO7i8Db/s/SSMrLicMxl9DQ\n87oRaU51TJQIZQ8E7hj3dsULnDwsj7qpxuOr+LhDU0CAeGDR5Q6ubM6eW3308b1N\ndgXYPmvM1wKBgQCGoc/ft+lmz1gepegT7YA8cRUPNQzi3M7PrSNL5nd3dXTKgOnk\nNr62iVQKZqaj+Ho6m35G4nyJGLAALldHP0/mMC8ZEMEzNpMN9mWPB0jN0Wi+8Tpm\nXTb+RS11CJ50mPwffbfXSXY+h0W9BEsyc+beLHW/YJvsNPIQCFmJGhPTzQKBgQC2\ngNFxWt+Kn3THRqvTsWJno14gouUgjewzXJjVw7giCOmoTZOtkGMyW3OE3g7MVWr/\nhZU1+DjOLMEONF8prmmc7RU/2zeaBBO7Fwo88bwVHq2NMorn8aLmBlW+iRq72IUs\nBzz7vj5xOwp4fh9L1BmENTdojIPy1NFGpkjYYwCjZwKBgQCr2pJ+AMN6yoSt0q54\naaVPme88W7MhJHpW9v3sy10xxtiKDJaaf+RrDaYxMnfnkQMtQL/vnP0Uxljd+x7n\noyXMF5SkYbUkDtLmTtDbAOMYJpjEJR+nD5Gb4alvHUUs51mN/yyBn9Kh5DBLOEI2\nIj06o7LA5RBcbmYkYZs/JdT5/g==\n-----END PRIVATE KEY-----\n'
client_id = '113095879717410609645'
client_email = 'terraform-gcp@sawyer-work-1804.iam.gserviceaccount.com'
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = 'https://oauth2.googleapis.com/token'
auth_provider_x509_cert_url = 'https://www.googleapis.com/oauth2/v1/certs'
client_x509_cert_url = 'https://www.googleapis.com/robot/v1/metadata/x509/terraform-gcp%40sawyer-work-1804.iam.gserviceaccount.com'
path = "/Users/hungnp14/Desktop/DE/Terraform/dataproc-terraform/credentials/sawyer-work-1804-65e64232ab96.json"
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
            .option("subscribe", "mysql-connector-02.AIRFLOW_CFG.job") \
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
    
df.printSchema()

df = df  \
    .writeStream \
    .format('parquet') \
    .option('path', 'gs://spark-bq-pipeline/data/') \
    .option('checkpointLocation', 'gs://spark-bq-pipeline/checkpoint/') \
    .start()

df.awaitTermination()

## debezium-kafka-spark
##### Table of Contents  
- [Step 1 - Resource requirements](#step-1-resource-requirements)
- [Step 6 — Operation](#step-6-operation)
### Step 1 - Resource requirements

1. Login to VM Instance

2. From Create an Instance Menu, select New VM Instances

3. From the Machine configuration section, select N1 Series (n1-standard-2; 2 vCPU, 7.5 GB memory). Then you might select the “Boost disk” section, in this blog post, I choose Ubuntu as an operating system with version: Ubuntu 20.04 LTS and Size 50GB SSD. Then from the Advances options, you might create 01 VPC Network with 01 Subnetwork — You might see there

4. Then let everything default and Create

5. Wait for instance to launch completely until State is Running

6. Then we will access the VM instance. We might have different ways to access the Ubuntu machine created above. Connect to VM instances via ssh command:

```bash
gcloud compute ssh - zone <your_zone_here> <your_vm_instance_name_here> -- project <project_id>
```

### Step 2 — Installing and Configuring MySQL Server

Connect to your MySQL-Server using ssh and follow the steps below to create a Source Database in MySQL for our purpose:

1. Update Repo & install MySQL:
```bash
sudo apt-get update
sudo apt-get install mysql-server
```
2. Login to MySQL & create user ‘debezium’ with password ‘dbz’ 
```sql
sudo mysql -u root -p
GRANT ALL PRIVILEGES ON *.* TO ‘debezium’@’%’ IDENTIFIED BY ‘dbz’;
FLUSH PRIVILEGES;

SHOW variables LIKE'log_bin';

#If the query result is OFF, then you can enable it by:

SET @@binlog_rows_query_log_events=ON;

```
For more information, you can Logout of the MySQL shell and edit the MySQL configuration file:
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```
And change these properties:
```bash

[mysqld]

log_bin = ON
log-bin = mysql-bin
binlog_row_image = FULL
binlog-format = ROW
server-id = 223344

binlog_rows_query_log_events = ON
expire_logs_days = 90
gtid_mode = ON
enforce_gtid_consistency = ON
performance_schema=ON
```
Then search for the row that contains bind-address and comment it out as follows and save the file. This will enable our MySQL service to be accessed from anywhere.

```bash
bind-address = 0.0.0.0
port = 3306
mysqlx-bind-address = 127.0.0.1
```
Restart MySQL service for changes to take effect

```bash
sudo service mysql restart
```
### Step 3 — Installing Zookeeper
1. Install Java-8:
```bash
sudo apt-get install openjdk-8-jdk
```
2. Download Zookeeper from the Apache Zookeeper site:
```bash
wget https://archive.apache.org/dist/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2.tar.gz
```
3. Extract the Zookeeper file
```bash
tar -xvzf apache-zookeeper-3.6.2-bin.tar.gz
mv apache-zookeeper-3.6.2-bin.tar.gz zookeeper

```
### Step 4 — Installing Kafka
Download & Extract Kafka from the Apache Kafka site. I use version 2.6.3 with Scala 2.12
```bash
wget https://archive.apache.org/dist/kafka/2.6.3/kafka_2.12-2.6.3.tgz
tar -xvzf kafka_2.12-2.6.3.tgz

mv kafka_2.12-2.6.3 kafka
```
### Step 5 — Setting Up the Debezium MySQL Connector

1. Download Debezium Connector Jar files from Maven Central. I use stable version 1.8 for this demo.

```shell
cd kafka
wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-mysql/1.8.0.Final/debezium-connector-mysql-1.8.0.Final-plugin.tar.gz
tar -xvzf debezium-connector-mysql-1.8.0.Final-plugin.tar.gz

#Debezium Connector acts as a Kafka Connector and Kafka stores its connector jars in a specific directory — /kafka/plugins. 
mv debezium-connector-mysql-1.8.0.Final-plugin plugins
```
2. Next, we make the required configurations on Kafka side
We let Kafka know that its Connect Service should load our Debezium-MySQL-Connector from /kafka/plugins. For this let’s edit the connect-standalone.properties file (I also attached file in repo) in kafka/config directory. Remove the # from the last line:
```shell
nano kafka/config/connect-standalone.properties
```
3. Copy all jars files in /kafka/plugins to /kafka/libs in order to make things work correctly
```bash
cp -p /plugins/*.jar ./libs/
```
4. Configure Debezium MySQL connector
Create a new properties file named connect-debezium-mysql.properties and paste the contents below into that file. Change highlighted properties to suit your sample data and Save the file in kafka/config directory.
```bash
name=mysql-connector-02
connector.class=io.debezium.connector.mysql.MySqlConnector
tasks.max=1
database.hostname=localhost
database.port=3306
database.user=debezium
database.password=dbz
database.server.id=223344
database.history.kafka.topic=msql.history
database.server.name=mysql-connector-02
database.dbname=classicmodels
database.history.kafka.bootstrap.servers=localhost:9092
key.converter=org.apache.kafka.connect.json.JsonConverter
```
Note that: in order to make this demo work correctly, you need to recreate a Kafka topic before. Let’s say, for example, I create a “msql.history” topic.
```bash
bin/kafka-topics.sh - create - bootstrap-server localhost:9092 - replication-factor 1 - partitions 1 - topic msql.history
```
### Step 6 — Operation

We are now ready to test Debezium MySQL Connector. For the best learning experience, I suggest that you open multiple Terminal (Say 5) and connect to your Debezium Server instance from each of these:

#### Terminal 1 — Start Zookeeper Service
```bash
bin/zookeeper-server-start.sh kafka/config/zookeeper.properties
```
#### Terminial 2 — Start Kafka Service
```bash
bin/kafka-server-start.sh kafka/config/server.properties
```
#### Terminal 3 — Monitor Topics and Messages
```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092 

#Use following commands to Watch messages published in a topic:

bin/kafka-console-consumer.sh — bootstrap-server localhost:9092 --topic <topic-name> --from-beginning
```
#### Terminal 4 — Start Kafka Connect Service with Debezium-MySQL-Connector
```bash
kafka/bin/connect-standalone.sh kafka/config/connect-standalone.properties kafka/config/connect-debezium-mysql.properties

#You might check whether or not the connection is runing

curl -s localhost:8083/connectors/mysql-connector/status | jq
```
#### Terminal 5 — Login to MySQL To Make Database Changes
If we wish to filter the message of the metadata (e.g, we wish to capture data from ‘payload’, make the following two changes in the connect-debezium-mysql.properties and connect-standalone.properties file:
```bash
key.converter.schemas.enable=false
value.converter=org.apache.kafka.connect.json.JsonConverter
value.converter.schemas.enable=false
schemas.enable=false
```
### Step 7 - Using Apache Spark to read streaming data from Kafka
In this step, we might use Spark to read our streaming data and process it if any. Therefore, I use a small table from MySQL:
```bash
AIRFLOW_CFG.job
# AIRFLOW_CFG is a dataset and the job is simply a table
```
To make these things work correctly, we might use spark-sql-kafka package to submit our spark jobs.
```bash
--packages "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0"
```
If we need to write our data to Google Bucket as a storage layer:
1. we have to use a gcs-connector:
```bash
--packages "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.10"
```
2. A service account (JSON file) to have enough credentials in order to write data to GCS.

3. Write our spark application to read & process kafka streaming data
I updated a small application, which you might reference in this repo.
#### Noted that
If you want to write data to HDFS, you might edit:
```python
df = df  \
    .writeStream \ 
    .partitionBy("year", "month", "day", "hour") \
    .format('parquet') \
    .option('path', "gs://spark-bq-pipeline/data/"+topic+"/") \
    .option('checkpointLocation', 'gs://spark-bq-pipeline/checkpoint/') \
    .start()
```
to
```python
df = df \
        .writeStream \
        .partitionBy("year", "month", "day", "hour") \
        .format("parquet") \
        .option("checkpointLocation", "hdfs://localhost:9000//spark-write-kafka/"+topic+"/") \
        .trigger(processingTime="5 seconds") \
        .option("path", "hdfs://localhost:9000//spark-write-kafka/"+topic+"/") \
        .start()
```
Thank you for reading.
Happy learning!

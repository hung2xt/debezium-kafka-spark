## debezium-kafka-spark

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

Download Debezium Connector Jar files from Maven Central. I use stable version 1.8 for this demo.

```shell
cd kafka
wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-mysql/1.8.0.Final/debezium-connector-mysql-1.8.0.Final-plugin.tar.gz
tar -xvzf debezium-connector-mysql-1.8.0.Final-plugin.tar.gz

#Debezium Connector acts as a Kafka Connector and Kafka stores its connector jars in a specific directory — /kafka/plugins. 
mv debezium-connector-mysql-1.8.0.Final-plugin plugins
```

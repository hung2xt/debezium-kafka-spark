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

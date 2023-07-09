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




# Running Topologies and Controllers on Mininet

## What is Mininet?

Mininet emulates a complete network of hosts, links, and switches
on a single machine.  To create a sample two-host, one-switch network,
just run:

  `sudo mn`

Mininet is useful for interactive development, testing, and demos,
especially those using OpenFlow and SDN.  OpenFlow-based network
controllers prototyped in Mininet can usually be transferred to
hardware with minimal changes for full line-rate execution.


## This project is a 3-part program. See Part A,B and C.

# Assignment 
In this task, you will learn about Software Defined Networking (SDN).
Using Virtualbox, Mininet, and Pox as the implementers of the OpenFlow protocol, you will build simple networks using SDN primitives.

1.	First, you will learn to use mininet, an SDN-enabled network emulator.
2.	Then, you will be using POX to implement a simple L2 firewall.
3.	Here you will be building an entire network, with multiple switches capable of handling ARP and other traffic.
4.	Lastly, you will be modifying your part 3 solution to implement an actual L3 IP router that handles ARP and routes traffic.

## Part A

### Problem Statement

The network topology depicted in Fig.1 consists of 1 core switch (CS), 4 switches (s1, s2, s3, and s4), 4 hosts (h1, h2, h3, and h4), and one server (Server). All traffic arriving on a switch is forwarded to the controller. It learns the mapping between MAC addresses and ports and installs a flow rule on the switch to handle future packets. So, the only packets that should arrive at the controller are those the switch doesn’t have a flow entry.

![mininetassign](https://user-images.githubusercontent.com/28300200/175469119-9d43cb56-cf17-4449-aee8-915fd6f22475.png)


### Deliverables
1. Have h1 ping h2 and h3 ping SERVER. How much time it took to ping?
2. Run iperf h1 h2 and iperf h3 SERVER. What is the throughput?
3. Run pingall to verify connectivity and dump the output. (Attah the Screenshot)
4. Dump the output of the flow rules using ovs-ofctl dump-flows. (Attach the Screenshot)
5. Topology file (topoa) and Controller file (contola).

### Steps
#### STEP 1: 
Copy topoa.pyfile to “~/mininet/custom” directory directly by creating a new file using nano topoa.py OR use this command in window cmd to copy this file to vm mininet
```
scp mininet@192.168.56.103 ./topoa.py ~/mininet/custom/
```
#### STEP 2: 
Copy controla.py file to “~/pox/pox/forwarding” directory directly by creating a new file using nano controla.py OR use this command in window cmd to copy this file to vm mininet
```
scp mininet@192.168.56.103 ./controla.py ~/pox/pox/forwarding
```
RUN COMMANDS IN UBUNTU TERMINAL
#### STEP 3:  
Open a terminal to run controller file and in ~/pox  directory  run this command 
```
mininet@mininet-vm: ~ /pox$./pox.py log. level --DEBUG forwarding. controla
```
#### STEP 4: 
Open new terminal to run topology file and in ~/ mininet/custom directory run this command
```
mininet@mininet-vm: ~/mininet/custom$sudo python topoa.py
```
#### STEP 5:  
Run this command in same mininet terminal
```
mininet>h1 ping -c5 h2
mininet>h3 ping -c5 SERVER
```
#### STEP 6:  
Run this command in same mininet terminal
```
mininet>iperf h1 h2
mininet>iperf h3 SERVER
```
#### STEP 7: 
Run this command in same mininet terminal
```
mininet>pingall
```




#### STEP 8: 
Now open another new terminal and run this commands one by one 
```
mininet@mininet-vm:~$ sudo ovs-ofctl dump-flows s1
mininet@mininet-vm:~$ sudo ovs-ofctl dump-flows s2
mininet@mininet-vm:~$ sudo ovs-ofctl dump-flows s3
mininet@mininet-vm:~$ sudo ovs-ofctl dump-flows s4
mininet@mininet-vm:~$ sudo ovs-ofctl dump-flows s5
```

## Part B

### Problem Statement

Modify the topology so that the host h1, h2, h3, and h4 have IP addresses 10.0.1.10/24, 10.0.1.20/24, 10.0.1.30/24, and 10.0.2.10/24 respectively. The SERVER has the IP address 10.0.4.10/24. Install IP-matching flow rules on switch CS. Let S1, S2, S3, and S4 stay as a MAC learning switch.

### Deliverables
1. Have h1 ping h2 and h3 ping SERVER. How much time it took to ping? How is it different from the previous controller?
2. Run iperf h1 SERVER and iperf h4 SERVER. What is the throughput?
3. Run pingall to verify connectivity and dump the output. (Attach the Screenshot)
4. Dump the output of the flow rules using ovs-ofctl dump-flows for all switches. (Attach the Screenshot)
5. Topology file (topob) and Controller file (controlb).

### Steps

#### STEP 1: 
Copy topob.pyfile to “~/mininet/custom” directory directly by creating a new file using nano topoa.py or use this command in window cmd to copy this file to vm mininet
```
scp mininet@192.168.56.103 ./topob.py ~/mininet/custom/
```
#### STEP 2: 
Copy controlb.py file to “~/pox/pox/forwarding” directory directly by creating a new file using nano controla.py or use this command in window cmd to copy this file to vm mininet
```
scp mininet@192.168.56.103 ./controlb.py ~/pox/pox/forwarding
```
RUN COMMANDS IN UBUNTU TERMINAL
#### STEP 3:
Open a terminal to run controller file and in  ~/pox  directory  run this command 
```
mininet@mininet-vm:~   /pox$./pox.py log.level --DEBUG forwarding.controlb
```
#### STEP 4: 
Open new terminal to run topology file and in  ~/ mininet/custom  directory  run this command
```
mininet@mininet-vm:~/mininet/custom$sudo python topob.py
```
#### STEP 5:
Run this command in same mininet terminal
```
mininet>h1 ping -c5 h2
mininet>h3 ping -c5 server
```
#### STEP 6:
Run this command in same mininet terminal
```
mininet>iperf h1 server
mininet>iperf h4server
```
#### STEP 7:

Run this command in  mininet terminal
```
mininet>pingall
```


#### STEP 8:
Now open another new terminal and run this commands one by one 
```
mininet@mininet-vm:~$ sudo ovs-ofctl dump-flows s1
mininet@mininet-vm:~$sudo ovs-ofctl dump-flows s2
mininet@mininet-vm:~$sudo ovs-ofctl dump-flows s3
mininet@mininet-vm:~$sudo ovs-ofctl dump-flows s4
mininet@mininet-vm:~$sudo ovs-ofctl dump-flows cs12
```

## Part C

### Problem Statement

Create a simple firewall at the switch CS. The firewall should allow arp and icmp traffic. Any other traffic should be dropped except IP traffic from h4. The IP addresses assigned to the hosts and server are same as previous problem (i.e., B).
### Deliverables
1. Run pingall to verify connectivity and dump the output. (Attach the Screenshot)
2. Run iperf h1 SERVER and iperf h4 SERVER. What is the throughput for both cases?
3. A screenshot of the output of the dpctl dump-flows for the switch CS.
4. Controller file (controlc).

### Steps

#### STEP1: 
Copy controlc.py file to “~/pox/pox/forwarding” directory directly by creating a new file using nano controla.py or use this command in window cmd to copy this file to vm mininet
```
scp mininet@192.168.56.103 ./controlc.py ~/pox/pox/forwarding
```
RUN COMMANDS IN UBUNTU TERMINAL
#### STEP 2:
Open a terminal to run controller file and in  ~/pox  directory  run this command 
```
mininet@mininet-vm:~   /pox$./pox.py log.level --DEBUG forwarding.controlc
```
#### STEP 3: 
Open new terminal to run topology file and in  ~/ mininet/custom  directory  run this command(topology file is same as part 2)
```
mininet@mininet-vm:~/mininet/custom$sudo python topob.py
```
#### STEP 4:
Run this command in  mininet terminal
```
mininet> pingall
```
#### STEP 5:
Run this command in same mininet terminal
```
mininet>iperf h1 server
mininet>iperf h4 server
```
#### STEP 6:
Run this command in same mininet terminal
mininet>dpctl dump-flows


## Feedback
For any Information and Feedback, please do not hesitate to email me at: **1107khyati@gmail.com**

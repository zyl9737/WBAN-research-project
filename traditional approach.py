# class normal node is the first type of node that is used in the hetorogeneous clustering involving WBAN
# 类普通节点是在涉及WBAN的异构集群中使用的第一类节点
import math as ma
import numpy as np
import cmath as ca
class normalnode:
# This is the constructor that initializes every default node with initial values and sets the value of residual energy as 100.
# 这是构造函数，它使用初始值初始化每个默认节点，并将剩余能量的值设置为100。
    def __init__(self,node_id):
        self.node_id=node_id
        self.packet='This is the heart rate'
        self.residual_energy=100
        self.type='normal'
# The funtion update_node is used to reduce the residual energy of each node at each transfer cycle the value of the token is
# decided by the kind of work the node is doing.
# 功能更新节点用于减少每个传输周期中每个节点的剩余能量，选中节点的值由节点正在执行的工作类型决定。
    def update_node(self,token):
        self.residual_energy=self.residual_energy-token
# It is used to return the residual energy to use in loops to evaluate dead nodes and to calculate forwarding function.
# 它用于返回剩余能量以用于循环中以评估死节点并计算转发功能。
    def return_energy(self):
        return self.residual_energy
# This function is used to send the data that is to be transmitted to the sink
# 此功能用于将要传输的数据发送到接收器
    def packet_sent(self):
        package=[self.node_id,self.packet]
# now we create the advanced node class that has all the qualities of the normal node class
# in normal node the value was 100 but the difference between both these is that advanced nodes have more return_energy
# That way they can read and transmit values to the forwarder node for longer duartions and not end up dead
# 现在，我们创建具有普通节点类所有特性的高级节点类
# 在正常节点中，该值为100，但两者之间的区别是高级节点具有更多的return_energy
# 这样，它们可以读取值并将其传输到转发器节点以获取更长的期限，并且不会最终失效
class advancednode:
# This is the constructor which initializes an advanced node object
    def __init__(self,node_id):
        self.node_id=node_id
        self.packet='This is the heart rate'
        self.residual_energy=150
        self.type='adv'
# This is the update node function that updates the residual energy of the nodes depending on the type o operation performed.
    def update_node(self,token):
        self.residual_energy=self.residual_energy-token
# This function is used to return the residual node energy for eavaluation purposes
# 此函数用于返回剩余节点能量以进行评估

    def return_energy(self):
        return self.residual_energy
# This function is used to send the data that is to be transmitted to the sink

    def packet_sent(self):
        package=[self.node_id,self.packet]

# Now we create a class for sink node that will have only one object.

class sinknode:
#We create a constructor that has the various parameters of the sink node initialized
# For research purposes we are going to assume that t
    def __init__(self):
        self.id='sink007'
        self.rounds=0
        self.packets_recieved=0
# dictionary that stores the values of the distance of each nod efrom the sink node. here the node id is used as the index for the distance element.
# 字典，用于存储每个节点到宿节点的距离值。 这里，节点ID用作距离元素的索引
        self.normdist={'node1':5,'node2':5.5,'node3':5.25,'node4':4.29}
# dictionary that stores the advanced nod edistance from the sink node and the advanced node id is used as the index
        self.advdist={'avnode1':9.25,'avnode2':10.5}
# function to aknowledge message packet_sent 确认发送的消息包
    def arrived(self):
        return 1


# function to calculate the forwarding function.
# 函数计算转发功能
def calc_ff(currentnode,sinky):
    if currentnode.residual_energy==100:
        denom1=ma.pow(currentnode.residual_energy,5)
        if currentnode.type=='normal':
            denom2=denom1*ma.pow(sinky.normdist[currentnode.node_id],7)
        else:
            denom2=denom1*ma.pow(sinky.advdist[currentnode.node_id],7)
        ff=1/denom2

    else:
        loca=100-currentnode.residual_energy
        denom1=ma.pow(loca,5)
        if currentnode.type=='normal':
            denom2=denom1*ma.pow(sinky.normdist[currentnode.node_id],7)
        else:
            denom2=denom1*ma.pow(sinky.advdist[currentnode.node_id],7)
        ff=1/denom2
    return ff


# function that selects the forwarder node:
def select_forwarder(normlist,advlist,sinky):
# calculating the ff of each normal node and storing this value in the list named below
# 计算每个普通节点的ff并将此值存储在下面命名的列表中
    normfflist=[]
    #advfflist=[]
    nodenamenorm=[]
    nodenameadv=[]
    for node in normlist:
        value=calc_ff(node,sinky)
        normfflist.append(value)
        nodenamenorm.append(node)
#  calculating the ff of each advanced node and storing the value in the list named below
    advfflist=[]
    for node in advlist:
        value=calc_ff(node,sinky)
        advfflist.append(value)
        nodenameadv.append(node)
# now finding the minimum value of each list and comparing the two values to find the node with the least value of ff
# 现在找到每个列表的最小值并将两个值进行比较以找到ff值为最小值的节点
    comp1=min(normfflist)
    comp2=0
    try:
        comp2=min(advfflist)
    except:
        valueff=comp1
        for element in nodenamenorm:
            flop=calc_ff(element,sinky)
            if flop==valueff:
                forwarder=element
    if comp1<comp2:
        valueff=comp1
        for element in nodenamenorm:
            flop=calc_ff(element,sinky)
            if flop==valueff:
                forwarder=element

    else:
        valueff=comp2
        for element in nodenameadv:
            flop=calc_ff(element,sinky)
            if flop==valueff:
                forwarder=element

    return forwarder
#this function is used to add stuff to the required csv file
def appendrow(list_of_elem):
    # Open file in append mode
    with open('proposed6.csv','a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
# The main execution part of the programstarts now:


import random
import sympy
from csv import writer
# to esentially count the number of rounds or cycles. I was thinking 20 to start with.
# 从本质上计算轮数或循环数。 我以20为开始
sink_packets=0
rounds=0
timeinstant=0
# this variable is for the skipping nodes. Essentially if this is prime we will skip writing the entry into the dataset so that attenuation can be represented aptly
# 此变量用于跳过节点。 本质上，如果这是素数，我们将跳过将条目写入数据集的过程，以便可以适当地表示衰减
flag=0
#failed nod evariable is going to count the total number of packets that got lost due to attenuation
# 失败的节点变量将计算由于衰减而丢失的数据包总数
failed_node=0
#transaction number counter
transno=0
# now i am going to create an object of the sink type node class. This is going to be the only object of this type.
sinky=sinknode()
#here we create objects of the normal node class and initialize them with the unique node ids
normalnodelist=[]
firstone=normalnode('node1')
normalnodelist.append(firstone)
firstone=normalnode('node2')
normalnodelist.append(firstone)
firstone=normalnode('node3')
normalnodelist.append(firstone)
firstone=normalnode('node4')
normalnodelist.append(firstone)
# here we create a list of objects of the advanced node class and initialize them with unique node ids
advnodelist=[]
firstone=advancednode('avnode1')
advnodelist.append(firstone)
firstone=advancednode('avnode2')
advnodelist.append(firstone)
sinky=sinknode()
# we are now going to start logical coding
# What is need to do is call the calculation ff function and decide the forwarding node
# Once that is done i need to establish a random order to forward data to the forwarding node
# Once that is done i need to write create a csv file. In the csv file, i write a timestamp id, the random node identifier and the other data columns
# 完成后，我需要建立随机顺序以将数据转发到转发节点
# 完成后，我需要编写一个csv文件。 在csv文件中，我写了一个时间戳ID，随机节点标识符和其他数据列
primelist=[]
for num in range(2,5000):
    if all(num%i!=0 for i in range(2,num)):
        primelist.append(num)
for i in range(450):
    timeinstant=timeinstant+1
    allnodelist=normalnodelist+advnodelist
    for node in allnodelist:
        if node.residual_energy<=0:
            allnodelist.remove(node)
            timeinstant=timeinstant+1
            if node.type=='normal':
                normalnodelist.remove(node)
                timeinstant=timeinstant+1
            else:
                advnodelist.remove(node)
                timeinstant=timeinstant+1
        else:
            continue
            timeinstant=timeinstant+1
    required_node=select_forwarder(normalnodelist,advnodelist,sinky)
    rounds=rounds+1
    timeinstant=timeinstant+1
    for node in allnodelist:
        if node==required_node:
            continue
            timeinstant=timeinstant+1
        else:
            if flag in primelist:
                failed_node=failed_node+1
                node.update_node(0.5)
                required_node.update_node(0.5)
                transno=transno+1
                timeinstant=timeinstant+1
                writable_contents=[required_node.node_id,node.node_id,rounds,transno,sinky.packets_recieved,required_node.residual_energy,node.residual_energy,timeinstant]
                # 需要节点的id，节点的id，轮数，交易号，接收器收到包的数量，需要节点剩余能量，节点剩余能量，时间戳
                appendrow(writable_contents)
                flag=flag+1
            else:
                sinky.packets_recieved=sinky.packets_recieved+1
                flag=flag+1
                transno=transno+1
                node.update_node(0.5)
                required_node.update_node(0.5)
                timeinstant=timeinstant+1
                writable_contents=[required_node.node_id,node.node_id,rounds,transno,sinky.packets_recieved,required_node.residual_energy,node.residual_energy,timeinstant]
                appendrow(writable_contents)

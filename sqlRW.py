# -*- coding: utf-8 -*-
import psutil
import time
import datetime
import threading
import pymysql

def getInfo():
    G=1024*1024*1024
    cpuCount=psutil.cpu_count(logical=False)
    cpuPercent=str(psutil.cpu_percent(1))#+"%"
    
    memoryTotalG=psutil.virtual_memory().total
    memoryFreeG=psutil.virtual_memory().free
    memoryTotal=round(psutil.virtual_memory().total/G*1024,2)
    memoryUsed=round(psutil.virtual_memory().used/G*1024,2)
    memoryFree=round(psutil.virtual_memory().free/G*1024,2)
    memoryPer=str(round(((memoryTotalG-memoryFreeG)/memoryTotalG)*100))#+"%"
    
    partiInfo=psutil.disk_partitions()
    partiCount=len(partiInfo)
    partiInfos=[]
    for par in partiInfo:
        mem=psutil.disk_usage(par.mountpoint)
        diskTotal=round(mem.total/G*1024,2)
        diskUsed=round(mem.used/G*1024,2)
        diskFree=round(mem.free/G*1024,2)
        partiInfos.append([par.device.split('/')[-1],diskTotal,diskUsed,diskFree])
    
    net=psutil.net_io_counters()
    netRecvData=round(net.bytes_recv/G*1024,2)
    netSenData=round(net.bytes_sent/G*1024,2)
    
    userList=psutil.users()
    userCount=len(userList)
    userName=[]
    for user in userList:
        userName.append(user.name)

    process=[]
    pid=psutil.pids()
    processCount=len(pid)
    for ids in pid:
        try:
            ps=psutil.Process(ids)
            processName=ps.name()
    #         processMem=ps.memory_percent()
            processStatus=ps.status()
            t1=ps.create_time()
    #         t2=time.localtime(t1)
    #         processCreate=time.strftime('%Y-%m-%d %H:%M:%S ',t1)
            processCreate=datetime.datetime.fromtimestamp(t1)
            process.append([ids,processName,processStatus,str(processCreate)])
        except:
            continue
        
    content={
        'cpu':[cpuCount,cpuPercent],
        'mem':[memoryTotal,memoryUsed,memoryFree,memoryPer],
        'parti':[partiCount,partiInfos],
        'net':[netRecvData,netSenData],
        'users':[userCount,userName],
        'process':[processCount,process],
    }
    return content


def writeSQL(times):
    
    
    contents=getInfo()
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="psutils",charset="utf8")
    cur=conn.cursor()
    cpuInfo=contents['cpu']
    
    cpuCount=cpuInfo[0]#1
    cpuPercent=cpuInfo[1]#2
    
    memory=contents['mem']
    memoryTotal=memory[0]#3
    memoryUsed=memory[1]#4
    memoryFree=memory[2]#5
    memoryPercent=memory[3]#6
    
    parti=contents['parti']
    partiCount=parti[0]#7
    partilis=parti[1]####lis[[]]
    
    net=contents['net']
    netRecvData=net[0]#8
    netSenData=net[1]#9
    
    users=contents['users']
    userCount=users[0]#10
    userLis=users[1]####lis[]
    
    process=contents['process']
    processCount=process[0]#11
    processLis=process[1]####lis[[]]
    insertInfo="""
        INSERT INTO info(`time`,cpuCount,cpuPercent,memoryTotal,memoryUsed,memoryFree,memoryPercent,partiCount,netRecvData,netSenData,userCount,processCount) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
    """
    cur.execute(insertInfo%(times,cpuCount,cpuPercent,memoryTotal,memoryUsed,memoryFree,memoryPercent,partiCount,netRecvData,netSenData,userCount,processCount))
    insertDisk="""
                INSERT INTO disk(`time`,device,diskTotal,diskUsed,diskFree) VALUES('%s','%s','%s','%s','%s')
    """
    for par in partilis:
        try:
            cur.execute(insertDisk%(times,par[0],par[1],par[2],par[3]))
        except:
            continue
    
    insertUser="""
    INSERT INTO user(`time`,`username`) VALUES('%s','%s')
    """
    for username in userLis:
        try:
            cur.execute(insertUser%(times,username))
        except:
            continue
    insertProcess="""
    INSERT INTO process(`time`,id,name,status,createTime) VALUES('%s','%s','%s','%s','%s')
    """
    for pro in processLis:
        try:
            cur.execute(insertProcess%(times,pro[0],pro[1],pro[2],pro[3]))
        except:
            continue
    try:
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    
    
    
    
def readSQL(times):
    contents=getInfo()
    content={}
    conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="psutils",charset="utf8")
    cur=conn.cursor()
    insertInfo="""
        SELECT * FROM  info WHERE time = '%s'
    """
    cur.execute(insertInfo%times)
    infoList=cur.fetchall()
    if len(infoList)==0:
        return False
    lis1=infoList[0]
    
    
    cpuCount=int(lis1[1])#1
    cpuPercent=float(lis1[2])#2
    
    memoryTotal=float(lis1[3])#3
    memoryUsed=float(lis1[4])#4
    memoryFree=float(lis1[5])#5
    memoryPercent=float(lis1[6])#6
    
    partiCount=int(lis1[7])#7
    
    netRecvData=float(lis1[8])#8
    netSenData=float(lis1[9])#9
    
    userCount=int(lis1[10])#10

    processCount=int(lis1[11])#11
    
    
    
    
        
        
        
    insertDisk="""
                SELECT * FROM  disk WHERE time = '%s'
    """
    cur.execute(insertDisk%times)
    diskList=cur.fetchall()
    if len(diskList)==0:
        return False
    diskLis=[]
    for lis2 in diskList:
        device=lis2[1]
        diskTotal=float(lis2[2])
        diskUsed=float(lis2[3])
        diskFree=float(lis2[4])
        diskLis.append([device,diskTotal,diskUsed,diskFree])
    
    insertUser="""
    SELECT * FROM  user WHERE time = '%s'
    """
    cur.execute(insertUser%times)
    userList=cur.fetchall()
    if len(userList)==0:
        return False
    userLis=[]
    for lis3 in userList:
        username=lis3[1]
        userLis.append(username)
    
    
    
    insertProcess="""
    SELECT * FROM  process WHERE time = '%s'
    """
    cur.execute(insertProcess%times)
    processList=cur.fetchall()
    if len(processList)==0:
        return False
    processLis=[]
    for lis4 in processList:
        try:
            ids=lis4[1]
            names=lis4[2]
            statuss=lis4[3]
            createTimes=lis4[4]
            processLis.append([ids,names,statuss,createTimes])
        except:
            continue
    
    
    content={
        'cpu':[cpuCount,cpuPercent],
        'mem':[memoryTotal,memoryUsed,memoryFree,memoryPercent],
        'parti':[partiCount,diskLis],
        'net':[netRecvData,netSenData],
        'users':[userCount,userLis],
        'process':[processCount,processLis],
    }
    return content

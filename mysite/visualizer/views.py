from django.http import HttpResponse
import json
# import json
from .models import Counter
import os
from django.utils import timezone
import pandas as pd
import sqlite3
import datetime
import random
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import seaborn as sns
from django.template import loader
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import render
import urllib


def convert_to_seconds(x):
    d = datetime.strptime(x, "%d/%m/%Y %H:%M:%S")
    d =  time.mktime(d.timetuple())
    print("this is d")

def process_url(f, link):
    t = timezone.now()
    
    datastore = json.loads(f)
    print(datastore)
    counter = datastore
   
    for key, value in counter.iteritems():
        print(key, value)
        counter = Counter(key=str(key), value=int(value), pub_date=t, server=link)

        counter.save()
    
    return datastore

def process_data(file_path):
    t = timezone.now()
    with open(file_path, 'r') as f:
        datastore = json.load(f)
        counter = datastore
        for key, value in counter.iteritems():
            print(key, value)
            counter = Counter(key=str(key), value=int(value), pub_date=t, server="local")
            counter.save()
    
    return datastore

def get_test_data():
    print("GET_TEST_DATA")
    module_dir = os.path.dirname(__file__)
    file = os.path.join(module_dir, 'TestData3.csv')
    print(file)
    testData = pd.read_csv(file)
    testData.dropna(axis=1, inplace=True)
    testData['pub_date'] = pd.to_datetime(testData['Time Stamp'], unit='s')
    print(testData)
    testData["key"] = testData["Key"] 
    testData["value"] = testData["Value"] 
    testData["server"] = testData["Server"] 
    return testData

def get_graphs_2(testData):
    keys = "key" #Holds the string names of the keys
    serv = "server" #Holds the string names of the server location
    vlaues = "value" #Holds the values of the counts
    time = "pub_date" #Holds the time stamps
    testData = get_test_data()
    #Values to get plots with an x limit (last few time intervals)
    xlimPlot = True
    xlim = 30 #The number of the last few time peices to graph

    showPlot = True #Runs the plt.show() command if this is True (should be set false)
    testData.sort_values("pub_date", inplace=True)
    graphNum = 0
    print(59)
    for k in testData.key.unique():
        #Gets the aggragate values for all servers per key
        aggra = np.zeros(len(testData[(testData[keys] == k) 
                    & (testData[serv] == testData.server.unique()[0])][vlaues].values))
        #Get the change in values for the aggragate
        change = np.zeros(len(aggra))
        #An array to hold the values (seperate per server)
        locArr = []
        #An array to hold the change in values (serperate per server)
        changeLocArr = []
        #Get the time stamp to use for the x axis
        timeAxis = testData[(testData[keys] == k) & (testData[serv] == testData.server.unique()[0])][time]
        timeAxisLen = len(timeAxis)
        print(73)
        for L in testData.server.unique():
            section = testData[(testData[keys] == k) & (testData[serv] == L)]
            #Add plot line to seperated values
            locArr.append(section[vlaues])
            #Update the aggragate change in values and change in values (the temp arr)
            a = section[vlaues].values
            change[0] = change[0] + a[0]
            changeTemp = np.zeros(len(a))
            changeTemp[0] = a[0]
            for i in range(1, len(change)):
                change[i] = change[i] + (a[i] - a[i-1])
                changeTemp[i] = a[i] - a[i-1]
            changeLocArr.append(changeTemp)
            #Get the aggragate values
            aggra = aggra + a
        
        L = testData.server.unique()
        print(91)
        #Plot the seperated values
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        for i in range(0, len(locArr)):
            plt.plot(timeAxis, locArr[i], label=L[i])

        print(98)
        plt.title("Counts for " + str(k) + " per Server")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig("static/"+ str(k) +"aaCountsPerServerKey_" + str(k) + ".png", bbox_inches='tight')
        print(106)
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(108)
        if(xlimPlot == True):
            plt.figure(graphNum)
            graphNum = graphNum+1
            minY = np.inf
            maxY = -np.inf
            for i in range(0, len(locArr)):
                plt.plot(timeAxis, locArr[i], label=L[i])
                minY = min(minY, min(locArr[i][timeAxisLen-1 - xlim:]))
                maxY = max(maxY, max(locArr[i][timeAxisLen-1 - xlim:]))
        
                plt.title("Counts for " + str(k) + " per Server" +
                          "\nOver Last " + str(xlim) + " Time Intervals")
                plt.xlabel("Time")
                plt.ylabel("Count")
                plt.xticks(rotation=45)
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                plt.ylim((minY * 0.998), (maxY * 1.002))
                plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
                plt.savefig("static/"+str(k)+"aCountsPerServerLimKey_" + str(k) + ".png", bbox_inches='tight')
                # if(showPlot == True):
                #     plt.show()
                plt.close()
        print(131)
        #Plot the aggragate
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        plt.plot(timeAxis, aggra)
        plt.title("Aggregate of Counts for " + str(k)
                  + " Over All Servers")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.savefig("static/"+ str(k) +"bAggCountsKey_" + str(k) + ".png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(146)
        if(xlimPlot == True):
            plt.figure(graphNum)
            graphNum = graphNum+1
            
            plt.plot(timeAxis, aggra)
            plt.title("Aggregate of Counts for " + str(k) + " Over All Servers"
                 + "\nOver Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.ylim((min(aggra[timeAxisLen-1-xlim:]) * 0.998), (max(aggra[timeAxisLen-1-xlim:]) * 1.002))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"bAggCountsLimKey_" + str(k) + ".png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
        print(163)
        #Plot the change in values
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        for i in range(0, len(changeLocArr)):
            plt.plot(timeAxis, changeLocArr[i], label=L[i])
        print(170)
        plt.title("Change in Counts for " + str(k) + " per Server")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig("static/"+ str(k) +"aChangeCountPerServerKey_" + str(k) + ".png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(180)
        if(xlimPlot == True):
            plt.figure(graphNum)
            graphNum = graphNum+1
            minY = np.inf
            maxY = -np.inf
            for i in range(0, len(changeLocArr)):
                plt.plot(timeAxis, changeLocArr[i], label=L[i])
                minY = min(minY, min(changeLocArr[i][timeAxisLen-1-xlim:]))
                maxY = max(maxY, max(changeLocArr[i][timeAxisLen-1-xlim:]))
                
            plt.title("Change in Counts for " + str(k) + " per Server"
                     + "\nOver Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.ylim((minY * 0.995), (maxY * 1.005))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"aChangeCountPerServerLimKey_" + str(k) + ".png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
        print(203)
        #Plot the aggragate change in values
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        plt.plot(timeAxis, change)
        plt.title("Aggregate of the Change in Counts \nfor " 
                  + str(k) + " Over All Servers")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.savefig("static/"+ str(k) +"bAggChangeCountKey_" + str(k) + ".png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        
        if(xlimPlot == True):
            plt.figure(graphNum)
            graphNum = graphNum+1
            plt.plot(timeAxis, change)
            plt.title("Aggregate of the Change in Counts for " + str(k)
                     + "\nOver All Servers Over Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Counts")
            plt.xticks(rotation=45)
            plt.ylim((0.995 * min(change[timeAxisLen-1-xlim:])), (1.005 * max(change[timeAxisLen-1-xlim:])))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"bAggChangeCountLimKey_" + str(k) + ".png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()

def get_graphs_url(testData):
    keys = "key" #Holds the string names of the keys
    serv = "server" #Holds the string names of the server location
    vlaues = "value" #Holds the values of the counts
    time = "pub_date" #Holds the time stamps
    #testData = get_test_data()
    #Values to get plots with an x limit (last few time intervals)
    xlimPlot = True
    xlim = 30 #The number of the last few time peices to graph
    print("this is test")
    print(testData)
    showPlot = True #Runs the plt.show() command if this is True (should be set false)
    testData.sort_values("pub_date", inplace=True)
    graphNum = 0
    print(59)
    print(testData)
    print("server")
    print(testData["server"])
    #testData = testData.fillna(0)
    
    for k in testData.key.unique():
        print("k")
        print(k)
        #Gets the aggragate values for all servers per key
        aggra = np.zeros(len(testData[(testData[keys] == k) 
                    & (testData[serv] == testData.server.unique()[0])][vlaues].values))
        #Get the change in values for the aggragate
        change = np.zeros(len(aggra))
        #An array to hold the values (seperate per server)
        locArr = []
        #An array to hold the change in values (serperate per server)
        changeLocArr = []
        #Get the time stamp to use for the x axis
        timeAxis = testData[(testData[keys] == k) & (testData[serv] == testData.server.unique()[0])][time]
        timeAxisLen = len(timeAxis)
        print(73)
        print(testData["server"])
        for L in testData.server.unique():
            section = testData[(testData[keys] == k) & (testData[serv] == L)]
            if section.empty:
                continue
    
            #Add plot line to seperated values
            locArr.append(section[vlaues])
            #Update the aggragate change in values and change in values (the temp arr)
            a = section[vlaues].values
            print("here")
            print("section")
            # if len(change) == 0 or len(a) == 0:
            #   break;
            print(section)
            print("k")
            print(L)
            print(len(aggra))
            
            # if len(aggra) == 0:
            #     continue

            change[0] = change[0] + a[0]
            changeTemp = np.zeros(len(a))
            changeTemp[0] = a[0]
            for i in range(1, len(change)):
                change[i] = change[i] + (a[i] - a[i-1])
                changeTemp[i] = a[i] - a[i-1]
            changeLocArr.append(changeTemp)
            #Get the aggragate values
            aggra = aggra + a
        
        L = testData.server.unique()
        print(322)
        #Plot the seperated values
        plt.figure(graphNum)
        graphNum = graphNum+1
        print(326)
        for i in range(0, len(locArr)):
            plt.plot(timeAxis, locArr[i], label=L[i])
            #plt.close()
        print(98)
        plt.title("Counts for " + str(k) + " per Server")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig("static/"+ str(k) +"_1CountsPerServerKey.png", bbox_inches='tight')
        print(106)
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(108)
        if(xlimPlot == True and xlim < timeAxisLen):
            plt.figure(graphNum)
            graphNum = graphNum+1
            minY = np.inf
            maxY = -np.inf
            for i in range(0, len(locArr)):
                plt.plot(timeAxis, locArr[i], label=L[i])
                minY = min(minY, min(locArr[i][timeAxisLen-1 - xlim:]))
                maxY = max(maxY, max(locArr[i][timeAxisLen-1 - xlim:]))
          
            plt.title("Counts for " + str(k) + " per Server" +
                      "\nOver Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.ylim((minY * 0.998), (maxY * 1.002))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+str(k)+"_2CountsPerServerLimKey.png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
        print(131)
        #Plot the aggragate
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        plt.plot(timeAxis, aggra)
        plt.title("Aggregate of Counts for " + str(k)
                  + " Over All Servers")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.savefig("static/"+ str(k) +"_3AggCountsKey.png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(146)
        if(xlimPlot == True and xlim < timeAxisLen):
            plt.figure(graphNum)
            graphNum = graphNum+1
            
            plt.plot(timeAxis, aggra)
            plt.title("Aggregate of Counts for " + str(k) + " Over All Servers"
                 + "\nOver Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.ylim((min(aggra[timeAxisLen-1-xlim:]) * 0.998), (max(aggra[timeAxisLen-1-xlim:]) * 1.002))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"_4AggCountsLimKey.png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
        print(163)
        #Plot the change in values
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        for i in range(0, len(changeLocArr)):
            plt.plot(timeAxis, changeLocArr[i], label=L[i])
        print(170)
        plt.title("Change in Counts for " + str(k) + " per Server")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig("static/"+ str(k) +"_5ChangeCountPerServerKey.png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(180)
        if(xlimPlot == True and xlim < timeAxisLen):
            plt.figure(graphNum)
            graphNum = graphNum+1
            minY = np.inf
            maxY = -np.inf
            for i in range(0, len(changeLocArr)):
                plt.plot(timeAxis, changeLocArr[i], label=L[i])
                minY = min(minY, min(changeLocArr[i][timeAxisLen-1-xlim:]))
                maxY = max(maxY, max(changeLocArr[i][timeAxisLen-1-xlim:]))
                
            plt.title("Change in Counts for " + str(k) + " per Server"
                     + "\nOver Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.ylim((minY * 0.995), (maxY * 1.005))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"_6ChangeCountPerServerLimKey.png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
        print(203)
        #Plot the aggragate change in values
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        plt.plot(timeAxis, change)
        plt.title("Aggregate of the Change in Counts \nfor " 
                  + str(k) + " Over All Servers")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.savefig("static/"+ str(k) +"_7AggChangeCountKey.png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        
        if(xlimPlot == True and xlim < timeAxisLen):
            plt.figure(graphNum)
            graphNum = graphNum+1
            plt.plot(timeAxis, change)
            plt.title("Aggregate of the Change in Counts for " + str(k)
                     + "\nOver All Servers Over Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Counts")
            plt.xticks(rotation=45)
            plt.ylim((0.995 * min(change[timeAxisLen-1-xlim:])), (1.005 * max(change[timeAxisLen-1-xlim:])))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"_8AggChangeCountLimKey.png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
def get_graphs_url_2(testData):
    keys = "key" #Holds the string names of the keys
    serv = "server" #Holds the string names of the server location
    vlaues = "value" #Holds the values of the counts
    time = "pub_date" #Holds the time stamps
    #testData = get_test_data()
    #Values to get plots with an x limit (last few time intervals)
    xlimPlot = True
    xlim = 30 #The number of the last few time peices to graph
    print("this is test")
    print(testData)
    showPlot = True #Runs the plt.show() command if this is True (should be set false)
    testData.sort_values("pub_date", inplace=True)
    graphNum = 0
    print(59)
    print(testData)
    print("server")
    print(testData["server"])
    #testData = testData.fillna(0)
    
    for k in testData.key.unique():
        print("k")
        print(k)
        #Gets the aggragate values for all servers per key
        aggra = np.zeros(len(testData[(testData[keys] == k) 
                    & (testData[serv] == testData.server.unique()[0])][vlaues].values))
        #Get the change in values for the aggragate
        change = np.zeros(len(aggra))
        #An array to hold the values (seperate per server)
        locArr = []
        #An array to hold the change in values (serperate per server)
        changeLocArr = []
        #Get the time stamp to use for the x axis
        timeAxis = testData[(testData[keys] == k) & (testData[serv] == testData.server.unique()[0])][time]
        timeAxisLen = len(timeAxis)
        print(73)
        #print(testData["server"])
        for L in testData.server.unique():
            section = testData[(testData[keys] == k) & (testData[serv] == L)]
            if section.empty:
                continue

            #Add plot line to seperated values
            locArr.append(section[vlaues])
            #Update the aggragate change in values and change in values (the temp arr)
            a = section[vlaues].values
            
            change[0] = change[0] + a[0]
            changeTemp = np.zeros(len(a))
            changeTemp[0] = a[0]
            for i in range(1, len(change)):
                change[i] = change[i] + (a[i] - a[i-1])
                changeTemp[i] = a[i] - a[i-1]
            changeLocArr.append(changeTemp)
            #Get the aggragate values
            aggra = aggra + a
        
        L = testData.server.unique()
        print(322)
        #Plot the seperated values
        plt.figure(graphNum)
        graphNum = graphNum+1
        print(326)
        for i in range(0, len(locArr)):
            plt.plot(timeAxis, locArr[i], label=L[i])
            #plt.close()
        print(98)
        plt.title("Counts for " + str(k) + " per Server")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig("static/"+ str(k) +"aaCountsPerServerKey_" + str(k) + ".png", bbox_inches='tight')
        print(106)
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(108)
        if(xlimPlot == True and xlim < timeAxisLen):
            plt.figure(graphNum)
            graphNum = graphNum+1
            minY = np.inf
            maxY = -np.inf
            for i in range(0, len(locArr)):
                plt.plot(timeAxis, locArr[i], label=L[i])
                minY = min(minY, min(locArr[i][timeAxisLen-1 - xlim:]))
                maxY = max(maxY, max(locArr[i][timeAxisLen-1 - xlim:]))
          
            plt.title("Counts for " + str(k) + " per Server" +
                      "\nOver Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.ylim((minY * 0.998), (maxY * 1.002))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+str(k)+"aCountsPerServerLimKey_" + str(k) + ".png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
        print(131)
        #Plot the aggragate
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        plt.plot(timeAxis, aggra)
        plt.title("Aggregate of Counts for " + str(k)
                  + " Over All Servers")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.savefig("static/"+ str(k) +"bAggCountsKey_" + str(k) + ".png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(146)
        if(xlimPlot == True and xlim < timeAxisLen):
            plt.figure(graphNum)
            graphNum = graphNum+1
            
            plt.plot(timeAxis, aggra)
            plt.title("Aggregate of Counts for " + str(k) + " Over All Servers"
                 + "\nOver Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.ylim((min(aggra[timeAxisLen-1-xlim:]) * 0.998), (max(aggra[timeAxisLen-1-xlim:]) * 1.002))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"bAggCountsLimKey_" + str(k) + ".png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
        print(163)
        #Plot the change in values
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        for i in range(0, len(changeLocArr)):
            plt.plot(timeAxis, changeLocArr[i], label=L[i])
        print(170)
        plt.title("Change in Counts for " + str(k) + " per Server")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.savefig("static/"+ str(k) +"aChangeCountPerServerKey_" + str(k) + ".png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        print(180)
        if(xlimPlot == True and xlim < timeAxisLen):
            plt.figure(graphNum)
            graphNum = graphNum+1
            minY = np.inf
            maxY = -np.inf
            for i in range(0, len(changeLocArr)):
                plt.plot(timeAxis, changeLocArr[i], label=L[i])
                minY = min(minY, min(changeLocArr[i][timeAxisLen-1-xlim:]))
                maxY = max(maxY, max(changeLocArr[i][timeAxisLen-1-xlim:]))
                
            plt.title("Change in Counts for " + str(k) + " per Server"
                     + "\nOver Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.ylim((minY * 0.995), (maxY * 1.005))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"aChangeCountPerServerLimKey_" + str(k) + ".png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()
        print(203)
        #Plot the aggragate change in values
        plt.figure(graphNum)
        graphNum = graphNum+1
        
        plt.plot(timeAxis, change)
        plt.title("Aggregate of the Change in Counts \nfor " 
                  + str(k) + " Over All Servers")
        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.savefig("static/"+ str(k) +"bAggChangeCountKey_" + str(k) + ".png", bbox_inches='tight')
        # if(showPlot == True):
        #     plt.show()
        plt.close()
        
        if(xlimPlot == True and xlim < timeAxisLen):
            plt.figure(graphNum)
            graphNum = graphNum+1
            plt.plot(timeAxis, change)
            plt.title("Aggregate of the Change in Counts for " + str(k)
                     + "\nOver All Servers Over Last " + str(xlim) + " Time Intervals")
            plt.xlabel("Time")
            plt.ylabel("Counts")
            plt.xticks(rotation=45)
            plt.ylim((0.995 * min(change[timeAxisLen-1-xlim:])), (1.005 * max(change[timeAxisLen-1-xlim:])))
            plt.xlim(timeAxis.values[timeAxisLen-1 - xlim],timeAxis.values[timeAxisLen-1])
            plt.savefig("static/"+ str(k) +"bAggChangeCountLimKey_" + str(k) + ".png", bbox_inches='tight')
            # if(showPlot == True):
            #     plt.show()
            plt.close()

def process_configuration(file):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, file)
    f = open(file_path, "r")

    #Get the time between scrapes
    line = f.readline().strip()
    while(line == "\n"):
        line = f.readline().strip()
    line = f.readline().strip()
    while(line == "\n"):
        line = f.readline().strip()
    try:
        scrapeTime = int(line[47:].strip())
    except ValueError:
        print("ERROR - Time Between Scrapes was not given an int,\n"
             + "Given:" + line[47:].strip() + "Use example line-\n"
             + "Time Between Scrapes (integer in milliseconds): 30000")
    if(scrapeTime <= 0):
        print("ERROR - Time Between Scrapes given invalid number (<=0)\n"
              + "Set automatically to 30000 (30 seconds)")
        scrapeTime = 30000

    #Get the time intervals shown (xlim)
    line = f.readline().strip()
    while(line == "\n"):
        line = f.readline().strip()
    try:
        xlim = int(line[38:].strip())
    except ValueError:
        print("ERROR - Time Intervals Shown was not given an int,\n"
             + "Given:" + line[38:].strip() + "Use example line-\n"
             + "Time Intervals Shown (integer number): 30")
    if(xlim <= 0):
        print("ERROR - Time Intervals Shown given invalid number (<=0)\n"
              + "Set automatically to 30")
        scrapeTime = 30

    #Save the server URLs
    line = f.readline()
    while(line == "\n"):
        line = f.readline()
    line = f.readline()
    while(line == "\n"):
        line = f.readline()
    servers = []
    serverNum = 0
    while(line != ""):
        line = line.strip()
        line = line.rstrip('\n')
        if(line == ""):
            line = f.readline()
            while(line == "\n"):
                line = f.readline()
            continue
        serverNum = serverNum + 1
        servers.append(line)
        line = f.readline()
        while(line == "\n"):
            line = f.readline()
    if(serverNum <= 0):
        print("ERROR - No servers Were Given, list the servers (one per line with no empty lines)\n"
             + "were indicated in Configuration.txt")

    return {"scrapeTime": scrapeTime, "serverNum": serverNum, "servers": servers, "xlim":xlim}

def url_to_text(link):
    f = urllib.urlopen(link)
    myfile = f.read()
    return myfile

def scrape():
    print("Scrape")

    context = process_configuration("Configuration.txt")
    live = 1
    if live == 1:
        link = context["servers"][0]
        myfile = url_to_text(link)
        datastore = process_url(myfile, link)
        link = context["servers"][1]
        
        myfile = url_to_text(link)
        datastore = process_url(myfile, link)
        df = pd.DataFrame(list(Counter.objects.all().values()))
        df = pd.DataFrame(list(Counter.objects.all().values('key', 'value', 'pub_date', 'server')))
        get_graphs_url(df)
        context = process_configuration("Configuration.txt")
    elif live == 0:
        datastore = process_data(file_path)


def home(request):
    print("home")
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'data.txt')

    context = process_configuration("Configuration.txt")
    path = "static"  # insert the path to your directory   
    img_list =os.listdir(path)
    img_list = sorted(img_list)
    if ".DS_Store" in img_list:
        img_list.remove(".DS_Store")
    context['graphs'] = img_list
    return render(request, 'visualizer/test.html', context)
    
def tests(request):
    latest_question_list = Counter.objects.order_by('pub_date')[:5]
    path="static"  
    img_list =os.listdir(path)
    context = {'graphs': img_list}
    return render(request, 'visualizer/test.html', context)


def run_scraper_in_background():
    context_file = process_configuration("Configuration.txt")
    sched = BackgroundScheduler()
    sched.add_job(scrape, 'interval', seconds=context_file["scrapeTime"])
    sched.start()
run_scraper_in_background()
"""
read killMap.csv, get the info that which method kills the mutant
read killed.csv, get the mutant status info

run selective mutation testing and output the result
"""

import os
import random

def read_subject_name(input_file_path):
    #store project path in subject_name[]
    myfile = open(input_file_path)

    while True:
        line = myfile.readline()
        if not line:
            break
        if (line[-2] == '\n') or (line[-2] == '\r'):
            subject_name.append(line[:-2])
        elif (line[-1] == '\n') or (line[-1] == '\r'):
            subject_name.append(line[:-1])
        else:
            subject_name.append(line)

def analysisMutStatusInfo(fileAddr):
    f = open(fileAddr)
    mapMutStatus = dict()
    cnt = 0
    
    # how many mutants have been killed
    cntKilled = 0

    while True:
        cnt += 1
        line = f.readline()
        if not line:
            break

        # remove the change line character
        if line[-2] == "\r":
            line = line[:-2]
        elif line[-1] == "\n":
            line = line[:-1]

        ele = line.split(",")
        
        mutID = (int)(ele[0])
        
        mutStatus = ele[1]
        if mutStatus == "KILLED":
            cntKilled += 1

        # add this mutant to dict
        mapMutStatus[mutID] = mutStatus

    f.close()
    return (mapMutStatus,cntKilled)

def analysisMutKiller(path):
    mapKiller = dict()
    for i in range(500000):
        mapKiller[i] = []

    f = open(path)
    cnt = 0
    while True:
        cnt += 1
        line = f.readline()
        if not line:
            break
        # remove the change line character
        if line[-2] == "\r":
            line = line[:-2]
        elif line[-1] == "\n":
            line = line[:-1]
          
        # begin to process and a line looks like this:
        # 4,KILLED,8,13,10,9
        ele = line.split(",")
        mutID = (int)(ele[0])
        killerNum = len(ele)-2
        
        for i in range(killerNum):
            testID = (int)(ele[i+2])
            mapKiller[mutID].append(testID)

    f.close()
    return mapKiller

def getSampleID(sampleSize, mapMutStatus):
    keys = mapMutStatus.keys()
    random.shuffle(keys)

    ids = []
    cnt = 0
    for i in keys:
        if mapMutStatus[i] == "KILLED":
            ids.append(i)
            cnt += 1
        if cnt == sampleSize:
            break
    return ids

def getTestNum(path):
    """
    simply calculate how many lines are there in testMap.csv and the test number is line-1
    """
    f = open(path)
    cnt = 0
    
    while True:
        cnt += 1
        line = f.readline()
        if not line:
            break
    f.close()
    return cnt-1

def buildAdequateTestSuite(sampleMutIDs,testNum, mapKiller):
    cover = dict()
    testID = []
    # initialize test ID array
    for i in range(1,testNum+1):
        testID.append(i)
    random.shuffle(testID)
    
    # initialize cover map
    for i in sampleMutIDs:
        cover[i] = False

    cntCovered = 0
    sampleSize = len(sampleMutIDs)
    
    adequateTestSuite = []
    for curTestID in testID:
        adequateTestSuite.append(curTestID)
        # for each test id, check every mutant that haven't been covered if this test can cover them
        for mutID in sampleMutIDs:
            if cover[mutID]:
                continue
            else:
                killer = mapKiller[mutID]
                # mark this element if the test can kill this mutant
                if curTestID in killer:
                    cntCovered += 1
                    cover[mutID] = True
        # jump out of the loop after finishing building adequate test suite
        if cntCovered == sampleSize:
            break
    return adequateTestSuite

def cntMutationScore(adequateMethodIDs, mapMutStatus, mapKiller):
    # all mutant ids
    keys = mapMutStatus.keys()
    
    # total number of killed mutant
    failCnt = 0
    
    # how many adequate test suite can kill
    cover = 0

    for i in keys:
        if mapMutStatus[i] == "KILLED":
            failCnt += 1
            killer = mapKiller[i]
            # whether test suite can kill this mutant
            killed = False
            for methodID in adequateMethodIDs:
                if methodID in killer:
                    killed = True
                    break
            if killed:
                cover += 1
    return (float)(cover)/(float)(failCnt)


def output(resultMetric1Addr, info):
    f = open(resultMetric1Addr,"a")
    f.write(info)
    f.close()



def getRandomTestSuite(size, testNum):
    testID = []
    for i in range(1, testNum+1):
        testID.append(i)
    random.shuffle(testID)

    selectedID = []

    for i in range(size):
        selectedID.append(testID[i])
    return selectedID

def calMS(sampleMutIDs, testIDs, mapMutStatus, mapKiller):

    total = 0    # total FAIL mutant number
    cover = 0    # mutant killed by tests 

    for i in sampleMutIDs:
        if mapMutStatus[i] == "KILLED":
            total += 1
            killer = mapKiller[i]
            
            killed = False    # whether test suite can kill this mutant
            for methodID in testIDs:
                if methodID in killer:
                    killed = True
                    break
            if killed:
                cover += 1
    return (float)(cover)/ total

def initialzeFile(resultMetric1Addr,resultMetric2Addr):
    f = open(resultMetric1Addr,"w")
    f.write("name,ms,percent,adequateTestSize\n")
    f.close()
    f = open(resultMetric2Addr,"w")
    f.write("name,msSubset,msAllset,percent,size\n")
    f.close()

subject_name = []

if __name__ =="__main__":
    # where to find the input major files
    dir = "pitProInfo"

    read_subject_name("../namelist.txt")
    
    resultMetric1Addr = "experimentResult/rawSMT_M1_rtemp.csv"
    resultMetric2Addr = "experimentResult/rawSMT_M2_rtemp.csv"
    
    # clean the output file
    initialzeFile(resultMetric1Addr,resultMetric2Addr)
    
    subNo = 0
    
    # how many projects used for each proportion?
    projectNumOfDiffProportion = [0,0,0,0,0,0]

    # mutant sample ranges from 1%~5%
    # instance order: 1%~5%, for each proportion: according to list
    for percent in range(1,2):
        print ("------------------------")
        print ("percent",percent)
        no = 0
        for i in subject_name:
            no += 1
            print no
            # for each subject , doing following procedure
            
            if i != "apache-httpclient":
                continue
            fileName = dir + "/" + i + "/"+ "killMap.csv"
            # get status map
            (mapMutStatus,killedMutNum) = analysisMutStatusInfo(fileName)
            
            # get killer map
            fileName = dir + "/" + i + "/"+ "killMap.csv"
            mapKiller = analysisMutKiller(fileName)

            # get test num
            fileName = dir + "/" + i + "/"+ "testMap.csv"
            testNum = getTestNum(fileName)

            # do metric1
            # calculate sample size, at least one
            sampleSize = killedMutNum * percent / 100

            # set a boundary to delete small projects
            if sampleSize < 0:
                continue
            # update the counter if the project has sample larger than boundry
            projectNumOfDiffProportion[percent] += 1

            if sampleSize == 0:
                sampleSize = 1
                
            # repeat 20 times for each percentage
            for repeat in range(50):
                # get id of sample mutants
                sampleMutIDs = getSampleID(sampleSize, mapMutStatus)

                # do metric 1
                # create 20 adequate test suite for each mutant sample
                for testSuiteNum in range(20):
                    adequateMethodIDs = buildAdequateTestSuite(sampleMutIDs,testNum,mapKiller)
                    # print (adequateMethodIDs)
                    adequateMethodNum = len(adequateMethodIDs)
                    metricScore = cntMutationScore(adequateMethodIDs,mapMutStatus,mapKiller)
                    
                    info = i+","+(str)(metricScore)+","+(str)(percent)+","+(str)(adequateMethodNum)+"\n"
                    # print (mutationScore)
                    output(resultMetric1Addr, info)


                # do metric2
                # create 100 test suites with random size
                for testSuiteNum in range(100):
                    # randomly decide the test size
                    size = random.randint(1, testNum)
                    testIDs = getRandomTestSuite(size, testNum)
                    msSubset = calMS(sampleMutIDs, testIDs, mapMutStatus, mapKiller)

                    allIDs = mapMutStatus.keys()
                    msAllset = calMS(allIDs, testIDs, mapMutStatus, mapKiller)
                    # print (msSubset)
                    # print (mutationScore)
                    "name,msSubset,msAllset,percent,size\n"
                    info = info = i+","+(str)(msSubset)+","+(str)(msAllset)+","+(str)(percent)+","+(str)(size)+"\n"
                    output(resultMetric2Addr,info)

    # count the total project number
    totalProjectNum = 0
    for percent in range(1,6):
        totalProjectNum += projectNumOfDiffProportion[percent]
    projectNumOfDiffProportion[0] = totalProjectNum
    
    # output the projcet number array to csv
    out = open("experimentResult/projectInfo.csv","w")
    out.write("totalProjectNum,1,2,3,4,5\n")
    info = ""
    for i in range(0,6):
        if i != 0:
            info += ","
        info += (str)(projectNumOfDiffProportion[i])
    info += "\n"
    out.write(info)
    print ("finished")





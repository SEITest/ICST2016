"""
Use m2 correlation result and other static info to generate a full csv

cmd:
python generateBMetricFull.py inputFilePath outputFilePath
"""
import sys
import math
import os

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

def analysisMutKilledInfo(fileAddr):
    f = open(fileAddr)
    # line cnt
    cnt = 0
    # number of mutants that can be killed
    killCnt = 0
    # number of mutants of type FAIL LIVE TIME
    totalCnt = 0
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
        
        totalCnt += 1
        if mutStatus == "KILLED":
            killCnt += 1

    return (killCnt,totalCnt)

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
    testNum = cnt -1
    f.close()
    return testNum

def analysisMutTotal(path):
    f = open(path)
    f.readline()    #ignore the first line
    info = f.readline()    # this line contains information needed
    mutTotal = (int)(info.split(",")[0])
    f.close()
    return mutTotal

def getSLOCMap(path):
    mapSLOC = dict()
    f = open(path)
    line = f.readline()
    while True:
        line = f.readline()
        if not line:
            break
        if line[-2] == "\r":
            line = line[:-2]
        else:
            line = line[:-1]

        ele = line.split(",")
        name = ele[0]
        sloc = (int)(ele[1])
        mapSLOC[name] = sloc
    f.close()
    return mapSLOC

def getAverageTestSize(fATS):
    sum = 0
    for i in range(2000):
        line = fATS.readline()
        if line[-2] == "/r":
            line = line[:-2]
        else:
            line = line[:-1]
        "name,msSubset,msAllset,percent,size"
        curTestSize = (int)(line.split(",")[4])
        sum += curTestSize
    ats = (float)(sum)/2000
    return ats


def expand(outputFilePath,fullFilePath,projectNum, instanceNum):
    # i for input file
    i = open(outputFilePath)
    # o for output file
    o = open(fullFilePath,"w")
    title = "name,y,x1,x2,x3,x4,x5,x6,x7,x8,lnx2,lnx3,lnx4,lnx5,lnx6,lnx7,lnx8,neginvx2,neginvx3,neginvx4,neginvx5,neginvx6,neginvx7,neginvx8\n"
    o.write(title)

    i.readline() # ignore the first line

    for lineNo in range(instanceNum):
        line = i.readline()
        if line[-2] == "\r":
            line = line[:-2]
        else:
            line = line[:-1]
        ele = line.split(",")
        
        fullLine = ""
        # add name,y,x1~x8
        for j in range(10):
            if j != 0:
                fullLine += ","
            fullLine += ele[j]
        # add lnx2~lnx8
        for j in range(3,10):
            fullLine += ","
            xj = (float)(ele[j])
            fullLine += (str)(math.log(xj))
        # add neginvx2~neginvx8
        for j in range(3,10):
            fullLine += ","
            xj = (float)(ele[j])
            fullLine += (str)(-1/xj)
        fullLine += "\n"
        o.write(fullLine)
    o.close()
    i.close()




subject_name = []

if __name__ == "__main__":

    # inputFilePath = "experimentResult/yM1.csv"
    # outputFilePath = "experimentResult/M1Title.csv"
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
    fullFilePath = sys.argv[3]

    # where to find the input pitest files
    dir = "pitProInfo"

    read_subject_name("../namelist.txt")
    
    # get SLOC map
    mapSLOC = getSLOCMap("SLOC.csv")
    
    # name of output file
    out = open(outputFilePath,"w")
    out.write("name,y,proportion,ms,mutTotal,mutKilled,testMethodNum,SLOC,testPer100Mut,averageTestSuiteSize\n")
    
    # fy = file contains y value
    fy = open(inputFilePath)
    fy.readline() # ignore the first line

    
    # get how many loops for each proportion
    f = open("experimentResult/projectInfo.csv")
    f.readline() # ignore the first line
    line = f.readline() # the second line has the information we need
    ele = line.split(",")
    loopTimePercent = []
    for i in range(0,6):
        loopTimePercent.append((int)(ele[i]))
    
    for percent in range(1,6):
        loopTime = loopTimePercent[percent]
        for i in range(loopTime):

            # read a line from yM1.csv
            line = fy.readline()
            if line[-2] == "\r":
                line = line[:-2]
            else:
                line = line[:-1]

            element = line.split(",")
            # line contains correlation for this proportion
            # name,ms,percent,adequateTestSize
            name = element[0]
            corStr = element[1]
            averageSuiteSize = element[3]

        
            # get mutation score of this project
            fileAddr = dir + "/" + name + "/"+ "killMap.csv"
            (mutKilled,mutTotal) = analysisMutKilledInfo(fileAddr)
            
            # calculate ms
            ms = (float)(mutKilled) / mutTotal

            # get test method num
            fileAddr = dir + "/" + name + "/"+ "testMap.csv"
            testNum = getTestNum(fileAddr)

            # get SLOC
            sloc = mapSLOC[name]

            "name,y,proportion,ms,mutTotal,mutKilled,testMethodNum,SLOC,testPer100Mut\n"
            outputInfo = name + "," + corStr + "," + (str)(percent)
            outputInfo += "," + (str)(ms) + "," + (str)(mutTotal) + "," + (str)(mutKilled)  
            outputInfo += "," + (str)(testNum) + "," + (str)(sloc) + "," + (str)((float)(testNum)*100/mutTotal)

            outputInfo += "," + (str)(averageSuiteSize)
            outputInfo += "\n"
            out.write(outputInfo)
    fy.close()
    out.close()

    
    # expand x2~x8, lnx2~lnx8, neginvx2~neginvx8
    expand(outputFilePath,fullFilePath, len(subject_name), loopTimePercent[0])
    
    # delete the file used
    # os.system("rm " + inputFilePath)
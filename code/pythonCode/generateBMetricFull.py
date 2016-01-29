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

def getAverageTestSize(fATS, lineNum):
    # lineNum: how many lines to calculate average
    sum = 0
    for i in range(lineNum):
        line = fATS.readline()
        if line[-2] == "/r":
            line = line[:-2]
        else:
            line = line[:-1]
        "name,msSubset,msAllset,percent,size"
        curTestSize = (int)(line.split(",")[4])
        sum += curTestSize
    ats = (float)(sum)/lineNum
    return ats

def rearrange(outputFilePath, projectNum):
    projectInfoNumber = projectNum * 5

    f = open(outputFilePath)
    title = f.readline()
    
    content = []
    for i in range(projectInfoNumber):
        line = f.readline()
        content.append(line)
    f.close()
    
    f = open(outputFilePath,"w")
    f.write(title)
    for proportion in range(5):
        curLineNo = proportion
        for j in range(projectNum):
            f.write(content[curLineNo])
            curLineNo += 5
    f.close()


def expand(outputFilePath,fullFilePath,projectNum):
    # i for input file
    i = open(outputFilePath)
    # o for output file
    o = open(fullFilePath,"w")
    title = "name,y,x1,x2,x3,x4,x5,x6,x7,x8,lnx2,lnx3,lnx4,lnx5,lnx6,lnx7,lnx8,neginvx2,neginvx3,neginvx4,neginvx5,neginvx6,neginvx7,neginvx8\n"
    o.write(title)

    i.readline() # ignore the first line

    instanceNum = projectNum*5
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

    # inputFilePath = "experimentResult/yKendall.csv"
    # outputFilePath = "experimentResult/M2KenTitle.csv"
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
    fullFilePath = sys.argv[3]
    
    # get instance number info
    f = open("experimentResult/projectInfo.csv")
    f.readline() # ignore the first line
    line = f.readline() # the second line has the information we need
    ele = line.split(",")
    loopTimePercent = []
    for i in range(0,6):
        loopTimePercent.append((int)(ele[i]))
    f.close()
    
    # fy = file contains y value
    fy = open(inputFilePath)


    # elements regarless of y x8, lnx8, neginvx8 are the same
    f = open("experimentResult/M1Full.csv")
    title = f.readline()
    
    # open a file to calculate averageTestSuiteSize
    # ignore the first line of the file
    fATS = open("experimentResult/rawSMT_M2.csv")
    fATS.readline()


    # name of output file
    out = open(fullFilePath,"w")
    out.write(title)

    totalLine = loopTimePercent[0]

    for i in range(totalLine):
        # get y value for this line
        line = fy.readline()
        if line[-2] == "\r":
            line = line[:-2]
        else:
            line = line[:-1]
        y = line

        # get x8 for this line
        x8 = getAverageTestSize(fATS,5000)
        lnx8 = math.log(x8)
        neginvx8 = -1/x8

        # original line
        # name,y,x1,x2,x3,x4,x5,x6,x7,x8,lnx2,lnx3,lnx4,lnx5,lnx6,lnx7,lnx8,neginvx2,neginvx3,neginvx4,neginvx5,neginvx6,neginvx7,neginvx8
        line = f.readline()
        ele = line.split(",")

        ele[1] = (str)(y)  # update y
        ele[9] = (str)(x8)
        ele[16] = (str)(lnx8)
        ele[23] = (str)(neginvx8)
        
        newLine = ""
        for j in range(24):
            if j != 0:
                newLine += ","
            newLine += ele[j]
        newLine += "\n"

        out.write(newLine)

    out.close()
    f.close()
    fATS.close()
    fy.close()


    
    

    

    
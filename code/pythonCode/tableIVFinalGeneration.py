"""
Input four kind of correlation matrixes and get the final table
i.e. M1RS, M2Ken, M2RS, M2Pearson
"""
import os

def get20times7Matrix(path):
    f = open(path)

    matrix = []
    for i in range(10):
        line = f.readline()
        if line[-2] == "\r":
            line = line[:-2]
        else:
            line = line[:-1]
        if i%2 == 0:
            continue
        else:
            # get project information
            info = line.split(",",1)[1]
            # split to 4*7 parts
            ele = info.split(",")
            for part in range(4):
                start = part * 7
                end = (part+1)*7
                tempLine = ""
                for eleNo in range(start,end):
                    if eleNo != start:
                        tempLine += ","
                    tempLine += ele[eleNo]
                matrix.append(tempLine)
    f.close()
    return matrix

def rearrange(array):
    for proportion in range(5):

        lineX = proportion * 4
        lineLn = proportion * 4 + 1
        # print(lineX,lineLn)
        # switch
        t = array[lineX]
        array[lineX] = array[lineLn]
        array[lineLn] = t
    return array

def columnRearrange(curTable):
    """
    ms,mutTotal,mutKilled,testMethodNum,SLOC,testPer100Mut,averageTestSuiteSize

    """
    finalTable = []
    names = ["ms","mutTotal","mutKilled","testMethodNum","SLOC","testPer100Mut","averageTestSuiteSize"]
    symbol = dict()
    for i in range(7):
        symbol[names[i]] = i
    
    lineNo = len(curTable)
    for i in range(lineNo):
        originLine = curTable[i]
        element = originLine.split(",")
        newLine = ""
        
        # SLOC
        newLine += element[symbol["SLOC"]]
        # Mtotal
        newLine += "," + element[symbol["mutTotal"]]
        # Mne
        newLine += "," + element[symbol["mutKilled"]]
        #MnePro
        newLine += "," + element[symbol["ms"]]
        #Ttotal
        newLine += "," + element[symbol["testMethodNum"]]
        #Tpm
        newLine += "," + element[symbol["testPer100Mut"]]
        #Tc
        newLine += "," + element[symbol["averageTestSuiteSize"]]
        
        # store the rearranged line into table
        finalTable.append(newLine)
    return finalTable

def roundToThree(curTable):
    lineNo = len(curTable)
    finalTable = []

    cnt = 0
    for i in range(lineNo):
        cnt += 1
        # print cnt
        originLine = curTable[i]
        # print originLine
        element = originLine.split(",")
        newLine = ""
        for j in range(7):
            if j != 0:
                newLine += ","
            number = (float)(element[j])
            number = round(number,3)
            newLine += (str)(number)
        # store the rearranged line into table
        finalTable.append(newLine)
    return finalTable


if __name__ == "__main__":
    # original sequence is x, lnx, neginvx, x^2
    # but the table requires order lnx, x, neginvx, x^2 
    # so we need to rearrange

    m120_7 = get20times7Matrix("experimentResult/tableIVM1.csv")
    m120_7 = rearrange(m120_7)

    ken20_7 = get20times7Matrix("experimentResult/tableIVKendall.csv")
    ken20_7 = rearrange(ken20_7)

    rs20_7 = get20times7Matrix("experimentResult/tableIVRS.csv")
    rs20_7 = rearrange(rs20_7)

    pearson20_7 = get20times7Matrix("experimentResult/tableIVPearson.csv")
    pearson20_7 = rearrange(pearson20_7) 
    
    finalTable = []  # each element is a line
    for proportion in range(5):
        lineStart = proportion * 4
        lineEnd = (proportion+1)*4
        
        # add metric 1 lines
        for lineNo in range(lineStart, lineEnd):
            finalTable.append(m120_7[lineNo])
        # add RS lines
        for lineNo in range(lineStart, lineEnd):
            finalTable.append(rs20_7[lineNo])
        # add Kendall lines
        for lineNo in range(lineStart, lineEnd):
            finalTable.append(ken20_7[lineNo])
        # add Pearson lines
        for lineNo in range(lineStart, lineEnd):
            finalTable.append(pearson20_7[lineNo])

    finalTable = columnRearrange(finalTable)
    
    finalTable = roundToThree(finalTable)
    # output final table as tableIV
    tableIV = "experimentResult/[final]TableIV.csv"
    o = open(tableIV,"w")
    for i in finalTable:
        o.write(i+"\n")
    o.close()
    
    #delete middle results
    os.system("rm experimentResult/tableIVM1.csv")
    os.system("rm experimentResult/tableIVRS.csv")
    os.system("rm experimentResult/tableIVPearson.csv")
    os.system("rm experimentResult/tableIVKendall.csv")





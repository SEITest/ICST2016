
# do linear regression and then store k, R^2, adjusted R^2
d = read.csv("experimentResult/rawSMT_M2.csv")

# get loop info
d1 = read.csv("experimentResult/projectInfo.csv")
loopTime = d1[1,1]

# how many instances do we need to calculate correlation?
numberOfInstance = 5000
x = 0
for (i in 1:loopTime)     
{
	start = (i-1)*numberOfInstance+1
	end = i*numberOfInstance
    start
    end
	tempData = d[start : end,]
    result = cor(tempData$msAllset, tempData$msSubset, "everything", "kendall")
    x[i] = result
}
write.csv(x, "experimentResult/corrM2Kendall.csv", FALSE)


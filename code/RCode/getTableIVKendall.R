
# do linear regression on y ~ x2,x3,x4,x5,x6,x7, column 4~9 10~15 16~21, get adjR^2


d = read.csv("experimentResult/M2KenFull.csv")

d1 = read.csv("experimentResult/projectInfo.csv")

start = 1
end = d1[1,2]

x = 0
for (i in 1:5)     
{
    # projectName = d[start,1]
    # proportion = d[start,5]
	start
	end
    tempData = d[start : end,]

    x = 0
    
    for(j in 4:24) # after loop we have x[1]~x[21]
    {

	    result = summary(lm( y ~ tempData[,j], data = tempData))
	    rr = result$r.squared
	    adjrr = result$adj.r.squared
	    # k = (result$coefficients)[2,1]
	    
	    x[j-3] = adjrr

	}
	# get x[22]~x[28]
	for(j in 4:10)
	{
		result = summary(lm( y ~ I(tempData[,j]^2) + tempData[,j], data = tempData))
		adjrr = result$adj.r.squared
		x[j+18] = adjrr
	}
	x = t(x)
	write.csv(x, "experimentResult/tableIVKendall.csv", TRUE)
	start = end + 1
	end = end + d1[1,i+2]
}

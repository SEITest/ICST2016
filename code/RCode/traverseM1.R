# traverse the all the combination and find out the highest R^2

d = read.csv("../experimentResult/M1Full.csv")

con = file("cmd.txt", "r")

line=readLines(con,n=1)
maxAdjrr = 0
maxLine = ""
while( length(line) != 0 ) {
     #print(line)
     result = summary(lm(line,data=d))
     adjrr = result$adj.r.squared
     if(adjrr > maxAdjrr)
     {
        maxAdjrr = adjrr
        maxLine = line
     }
      
     line=readLines(con,n=1)   
}
print(maxLine)
print(maxAdjrr)
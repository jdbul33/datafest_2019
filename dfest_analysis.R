library(lme4)
library(Formula)
library(e1071)
library(imputeTS)
library(randomForest)
library(AER)


data = Jellybean
data$GameID = NULL
data$PlayerID = NULL
data$TeamPoints = NULL
data$TeamPointsAllowed = NULL
data$Date = NULL

data$AcuteLoad = na.mean(data$AcuteLoad, option = "mean")
data$ChronicLoad = na.mean(data$ChronicLoad, option = "mean")
data$AcuteChronicRatio = na.mean(data$AcuteChronicRatio, option = "mean")


ind <- sample(2, nrow(data), replace=TRUE, prob=c(0.7, 0.3))
trainDataRF <- data[ind==1,]
testDataRF <- data[ind==2,]

rf <- randomForest(Victory ~ ., data=trainDataRF, ntree=1000, proximity=TRUE)
table(predict(rf), trainDataRF$Victory)
print(rf)
attributes(rf)


plot(rf)

importance(rf)
varImpPlot(rf)

rf <- randomForest(Victory ~ Soreness + MonitoringScore + AccelZ_skew_2 + Accel_3D_skew_2 + 
                      + Desire, data=trainDataRF, ntree=1000, proximity=TRUE)

table(predict(rf), trainDataRF$Victory)
print(rf)
attributes(rf)

importance(rf)
varImpPlot(rf)



datalogistic <- glm(Victory ~ Soreness + AccelZ_std_1 + AccelZ_skew_2 + 
                      AccelY_skew_2  + AccelImpulse_std_2
                      + Desire + AccelLoad_skew_2
                      + AccelX_skew_1
                      + AccelZ_skew_1, data = data, family = "binomial")

summary(datalogistic)


Tacklingindex = ivreg(Victory ~ Soreness + Desire + MonitoringScore | AccelZ_skew_2 + Accel_3D_skew_2 + 
                        AccelY_skew_2 + AccelZ_std_1 + AccelImpulse_std_2 + AccelX_skew_1 + AccelLoad_skew_2
                      + AccelZ_skew_1, data = data)

summary(Tacklingindex, vcov = sandwich, diagnostics = TRUE)

data$tacklingindexfirst = (data$AccelZ_std_1 + data$AccelZ_skew_1 + data$AccelY_skew_1 + data$AccelLoad_skew_1)
data$tacklingindexsecond = (data$AccelZ_std_2 + data$AccelZ_skew_2 + data$AccelY_skew_2 + data$AccelLoad_skew_2)

data$tacklingindexfirstz = scale(data$tacklingindexfirst, center = TRUE, scale = TRUE)
data$tacklingindexsecondz = scale(data$tacklingindexsecond, center = TRUE, scale = TRUE)

datalogistic <- glm(Victory ~
                     tacklingindexsecond
                    + AcuteLoad
                    + ChronicLoad
                    + Soreness
                    + RPE, data = data, family = "binomial")
summary(datalogistic)

datawithindex = data

ind <- sample(2, nrow(datawithindex), replace=TRUE, prob=c(0.7, 0.3))
trainDataRF <- datawithindex[ind==1,]
testDataRF <- datawithindex[ind==2,]


rf <- randomForest(Victory ~ Soreness + tacklingindexsecond
                   + 
                   +, data=trainDataRF, ntree=1000, proximity=TRUE)
table(predict(rf), trainDataRF$Victory)
print(rf)
attributes(rf)
importance(rf)
varImpPlot(rf)


firstindexregression = lm(data$tacklingindexfirst ~ data$RPE + data$ChronicLoad + data$AcuteLoad + data$Soreness)
summary(firstindexregression)

secondindexregression = lm(data$tacklingindexsecond ~ data$RPE + data$ChronicLoad + data$AcuteLoad + data$Soreness)
summary(secondindexregression)


datalogistic <- glm(Victory ~
                      tacklingindexsecond
                    + AcuteLoad
                    + ChronicLoad
                    + Soreness, data = datawithindex, family = "binomial")
summary(datalogistic)

secondlm = lm(tacklingindexsecond ~ AcuteLoad + ChronicLoad, data = datawithindex)
summary(secondlm)


Tacklingindexiv = ivreg(Victory ~ Soreness + tacklingindexsecond + RPE | tacklingindexsecond + AcuteLoad + ChronicLoad, data = datawithindex)
summary(Tacklingindexiv, vcov = sandwich,  diagnostics = TRUE)


victorybitches = lm(data$Victory ~ data$Soreness + data$tacklingindexsecond)
plot(victorybitches)

plot(Victory~tacklingindexsecond, data=datawithindex, col="red4")
lines(Victory ~ Soreness, newdat, col="green4", lwd=2)

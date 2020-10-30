# need to install package first: install.packages("CausalImpact")
library(CausalImpact)
library(foreach)
library(doParallel)
library(mgcv)
library(car)
library(ggplot2)
library(lattice)
library(spdep)
library(sf)
library(tmap)
library(scales)
library(reshape2)
library(forecast)


# cross-validation loop
bsts.cv.loop <- function(data, horizon, number_of_folds, niter = 1000, seed = 1232, burn = 250,
                         do.plot = FALSE, verbose = TRUE, debug = TRUE) {
  # clean the data
  #data <- dat[dat$station_id == 40070,]
  response <- zoo(data$rides, data$date)
  response_cl <- tsclean(response, replace.missing = TRUE, lambda = NULL)
  data$rides <- coredata(response_cl)
  #rmse_v <- c()
  #mape_v <- c()
  #mase_v <- c()
  truth_v <- c()
  pre_v <- c()
  date_v <- c()
  for (fold in 1:number_of_folds) {
    print(fold)
    # construct data_train/data_test
    l <- nrow(data) - fold * horizon
    if (debug) print(l)
    data_train <- data[1:l,]
    data_test <- data[(l + 1):(l + horizon),]
    response <- zoo(data_train$rides, data_train$date)
    ss <- AddSemilocalLinearTrend(list(), response)
    ss <- AddSeasonal(ss, response, nseasons = 7)
    ss <- AddMonthlyAnnualCycle(ss, response)

    # fit model & predict
    model <- bsts(response, state.specification = ss, niter = 2000, seed = 1232, ping = 0)
    pred <- predict(model, horizon = horizon, burn = burn)
    if (do.plot) {
      # plot
      plot(pred, plot.original = 36)
      lines(data[(l + 1):(l + horizon), 'date'], data_test$rides, col = "red", type = "l")
    }
    # evaluation
    truth_v <- c(truth_v, data_test$rides)
    pre_v <- c(pre_v, pred$mean)
    date_v <- c(date_v, as.character(data_test$date))
    #errors <- data_test$rides - pred$mean
    #rmse <- sqrt(mean(errors^2))
    #rmse_v <- c(rmse_v, rmse)
    #mape <- mean(abs(errors) / data_test$rides) * 100
    #mape_v <- c(mape_v, mape)
    #naive_prediction_errors <- diff(data$rides, 1)
    #mase <- mean(abs(errors)) / mean(abs(naive_prediction_errors))
    #mase_v <- c(mase_v, mase)
    if (verbose) print(paste0("fold ", fold, ": mape ", mape, " / mase ", mase)) }
  return(data.frame(truth = truth_v, pred = pre_v, date = date_v)) }

dat <- read.csv('D:\\Transit\\Daily_Lstaion_Final.csv') # Daily_Lstaion_Final_0806.csv
dat$date <- as.Date(dat$date)
dat <- dat[dat$date < "2020-01-01",]
AllCounty <- unique(dat$station_id)

horizon <- 30
number_of_folds <- 12

#res <- bsts.cv.loop(dat[dat$station_id == 40010,], horizon = 30,
#                    number_of_folds = 1, do.plot = TRUE, debug = FALSE, verbose = FALSE)

# Setup parallel backend
cores <- detectCores()
cl <- makeCluster(cores[1] - 1)
registerDoParallel(cl)
finalMatrix <- data.frame()


finalMatrix <-
  foreach(
    ccount = 1:length(AllCounty), # length(AllCounty)
    .combine = rbind, .errorhandling = 'remove',
    .packages = c("CausalImpact", "reshape2", "lattice", "ggplot2", "forecast")
  ) %dopar%
  {
    eachstation <- AllCounty[ccount]
    # eachstation <- 40440
    # eachstation <- 40090
    print(ccount)
    dat_Each <- dat[dat$station_id == eachstation,]
    rownames(dat_Each) <- NULL
    res <- bsts.cv.loop(dat_Each, horizon = horizon,
                        number_of_folds = number_of_folds,
                        do.plot = FALSE, debug = FALSE, verbose = FALSE)
    res$CTNAME <- eachstation
    res
    #write.csv(components.withreg, 'finalMatrix_Transit_temp.csv')
  }

stopCluster(cl)
write.csv(finalMatrix, 'finalMatrix_Transit_1030_1.csv')


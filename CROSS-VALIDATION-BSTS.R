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
  rmse_v <- c()
  mape_v <- c()
  mase_v <- c()
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
      lines(data[(l + 1):(l + horizon),'date'], data_test$rides, col = "red", type = "l")
    }
    # evaluation
    errors <- data_test$rides - pred$mean
    rmse <- sqrt(mean(errors^2))
    rmse_v <- c(rmse_v, rmse)
    mape <- mean(abs(errors) / data_test$rides) * 100
    mape_v <- c(mape_v, mape)
    naive_prediction_errors <- diff(data$rides, 1)
    mase <- mean(abs(errors)) / mean(abs(naive_prediction_errors))
    mase_v <- c(mase_v, mase)
    if (verbose) print(paste0("fold ", fold, ": mape ", mape, " / mase ", mase)) }
  return(data.frame(rmse = rmse_v, mape = mape_v, mase = mase_v)) }

dat <- read.csv('D:\\Transit\\Daily_Lstaion_Final.csv') # Daily_Lstaion_Final_0806.csv
dat$date <- as.Date(dat$date)
AllCounty <- unique(dat$station_id)

horizon <- 30
number_of_folds <- 12

res <- bsts.cv.loop(dat[dat$station_id == 40010,],
                    horizon = horizon,
                    number_of_folds = number_of_folds,
                    do.plot = TRUE,
                    debug = FALSE,
                    verbose = FALSE)
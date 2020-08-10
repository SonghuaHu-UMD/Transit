library(car)
library(mgcv)
library(psych)
library(dplyr)
library(mgcViz)
library(spdep)
library(sf)
library(tmap)
library(leaps)
library(MASS)
library(glmnet)
library(mdatools)

# Read data
dat <- read.csv('D:/Transit/All_final_Transit_R2.csv')
dat$rides <- round(dat$rides)

# Stepwise
tmp_Impact <- step(lm(
  Relative_Impact ~ COMMERCIAL + # rides
    INDUSTRIAL +
    INSTITUTIONAL +
    OPENSPACE +
    RESIDENTIAL +
    Cumu_Cases +
    Pct.Male +
    Pct.Age_0_24 +
    Pct.Age_25_40 +
    Pct.Age_40_65 +
    Pct.White +
    Pct.Black +
    Income +
    PopDensity +
    Freq +
    Num_trips +
    Pct.WJob_Utilities +
    Pct.WJob_Goods_Product +
    WTotal_Job_Density,
  data = dat), direction = "both")
summary(tmp_Impact)

tmp_Rides <- step(glm.nb(
  rides ~ COMMERCIAL + # rides
    INDUSTRIAL +
    INSTITUTIONAL +
    OPENSPACE +
    RESIDENTIAL +
    Cumu_Cases +
    Pct.Male +
    Pct.Age_0_24 +
    Pct.Age_25_40 +
    Pct.Age_40_65 +
    Pct.White +
    Pct.Black +
    Income +
    PopDensity +
    Freq +
    Num_trips +
    Pct.WJob_Utilities +
    Pct.WJob_Goods_Product +
    WTotal_Job_Density, data = dat), direction = "both")
summary(tmp_Rides)

# Use the selection to build gam
dat$station_id <- as.factor(dat$station_id)
colnames(dat)
GAM_RES1 <-
  mgcv::gam(Relative_Impact ~
              COMMERCIAL + # rides
                INDUSTRIAL +
                INSTITUTIONAL +
                OPENSPACE +
                RESIDENTIAL +
                Cumu_Cases +
                Pct.Male +
                Pct.Age_0_24 +
                Pct.Age_25_40 +
                Pct.Age_40_65 +
                Pct.White +
                Pct.Black +
                Income +
                PopDensity +
                Freq +
                Num_trips +
                Pct.WJob_Utilities +
                Pct.WJob_Goods_Product +
                WTotal_Job_Density +
                ti(LAT, LNG),
            data = dat, family = c("gaussian"), method = "REML")
summary(GAM_RES1)
concurvity(GAM_RES1, full = FALSE)

GAM_RES2 <-
  mgcv::gam(rides ~
              COMMERCIAL + # rides
                INDUSTRIAL +
                INSTITUTIONAL +
                OPENSPACE +
                RESIDENTIAL +
                Cumu_Cases +
                Pct.Male +
                Pct.Age_0_24 +
                Pct.Age_25_40 +
                Pct.Age_40_65 +
                Pct.White +
                Pct.Black +
                Income +
                PopDensity +
                Freq +
                Num_trips +
                Pct.WJob_Utilities +
                Pct.WJob_Goods_Product +
                WTotal_Job_Density +
                ti(LAT, LNG),
            data = dat, family = 'nb', method = "REML")
summary(GAM_RES2)


# LASSO/RIDGE
lambdas <- 10^seq(5, -5, by = -.1)
x <- dat %>%
  dplyr::select(COMMERCIAL, INDUSTRIAL, INSTITUTIONAL, OPENSPACE, RESIDENTIAL,
                Cumu_Cases, Pct.Male, Pct.Age_0_24, Pct.Age_25_40, Pct.Age_40_65,
                Pct.White, Pct.Black, Income, PopDensity, Freq, Num_trips, Pct.WJob_Utilities, Pct.WJob_Goods_Product,
                WTotal_Job_Density) %>%
  data.matrix()

## For impact
y <- dat$Relative_Impact
# RIDGE
cv_fit <- cv.glmnet(x, y, alpha = 0, lambda = lambdas)
plot(cv_fit)
opt_lambda <- cv_fit$lambda.min
# Rebuilding the model with optimal lambda value
best_ridge <- glmnet(x, y, alpha = 0, lambda = cv_fit$lambda.min)
coef(best_ridge)

# LASSO
cv_fit <- cv.glmnet(x, y, alpha = 1, lambda = lambdas)
plot(cv_fit)
opt_lambda <- cv_fit$lambda.min
# Rebuilding the model with optimal lambda value
best_lasso <- glmnet(x, y, alpha = 1, lambda = cv_fit$lambda.min)
coef(best_lasso)

## For ride
y <- dat$rides
# RIDGE
cv_fit <- cv.glmnet(x, y, alpha = 0, lambda = lambdas, family = "poisson")
plot(cv_fit)
opt_lambda <- cv_fit$lambda.min
# Rebuilding the model with optimal lambda value
best_ridge <- glmnet(x, y, alpha = 0, lambda = cv_fit$lambda.min, family = "poisson")
coef(best_ridge)

# LASSO
cv_fit <- cv.glmnet(x, y, alpha = 1, lambda = lambdas, family = "poisson")
plot(cv_fit)
opt_lambda <- cv_fit$lambda.min
# Rebuilding the model with optimal lambda value
best_lasso <- glmnet(x, y, alpha = 1, lambda = cv_fit$lambda.min)
coef(best_lasso)


# Use the selection to build gam
dat$station_id <- as.factor(dat$station_id)
colnames(dat)
GAM_RES1 <-
  mgcv::gam(Relative_Impact ~
              COMMERCIAL +
                INDUSTRIAL +
                Pct.Age_25_40 +
                Pct.Age_40_65 +
                Pct.White +
                Pct.Black +
                Income +
                PopDensity +
                Pct.WJob_Utilities +
                WTotal_Job_Density +
                ti(LAT, LNG),
            data = dat, family = c("gaussian"), method = "REML")
summary(GAM_RES1)

GAM_RES2 <-
  mgcv::gam(rides ~
              COMMERCIAL +
                INDUSTRIAL +
                Pct.Age_25_40 +
                Pct.Age_40_65 +
                PopDensity +
                Freq +
                Num_trips +
                Pct.White +
                Pct.Black +
                Income +
                WTotal_Job_Density +
                Pct.WJob_Utilities +
                ti(LAT, LNG),
            data = dat, family = c("nb"), method = "REML")
summary(GAM_RES2)


# PCA/PLS
m <- pls(x, y, 7, cv = 4, scale = TRUE, info = "Shoesize prediction model")
summary(m)
plotRegcoeffs(m)
show(m$coeffs$values[, 3, 1])
summary(m$coeffs)
m <- selectCompNum(m, 3)
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
  Relative_Impact ~
    COMMERCIAL +
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
      Pct.Asian +
      Income +
      College +
      PopDensity +
      Freq +
      Num_trips +
      WJob_OtherServices_Density +
      WJob_Utilities_Density +
      WJob_Goods_Product_Density +
      WTotal_Job_Density,
  data = dat),
                   direction = "both")
summary(tmp_Impact)

tmp_Rides <- step(glm.nb(
  rides ~
    COMMERCIAL +
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
      Pct.Asian +
      Income +
      College +
      PopDensity +
      Freq +
      Num_trips +
      WJob_OtherServices_Density +
      WJob_Utilities_Density +
      WJob_Goods_Product_Density +
      WTotal_Job_Density, data = dat), direction = "both")
summary(tmp_Rides)

# Use the selection to build gam
dat$station_id <- as.factor(dat$station_id)
colnames(dat)
GAM_RES1 <-
  mgcv::gam(Relative_Impact ~
              COMMERCIAL +
                RESIDENTIAL +
                Cumu_Cases +
                Pct.Male +
                Pct.Age_0_24 +
                Pct.Age_25_40 +
                Pct.Age_40_65 +
                Pct.Black +
                Income +
                PopDensity +
                Freq +
                Num_trips +
                WJob_OtherServices_Density +
                WJob_Utilities_Density +
                WJob_Goods_Product_Density +
                ti(LAT, LNG),
            data = dat, family = c("gaussian"), method = "REML")
summary(GAM_RES1)

GAM_RES2 <-
  mgcv::gam(rides ~ COMMERCIAL +
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
    Pct.Asian +
    Income +
    College +
    PopDensity +
    Freq +
    Num_trips +
    WJob_OtherServices_Density +
    WJob_Utilities_Density +
    WJob_Goods_Product_Density +
    ti(LAT, LNG),
            data = dat, family = "nb", method = "REML")
summary(GAM_RES2)

vif_test <-
  lm(
    rides ~ COMMERCIAL +
      INDUSTRIAL +
      INSTITUTIONAL +
      OPENSPACE +
      RESIDENTIAL +
      Cumu_Cases +
      Pct.Age_0_24 +
      Pct.White +
      PopDensity,
    data = dat
  )
vif(vif_test)
summary(vif_test)


# LASSO/RIDGE
lambdas <- 10^seq(5, -5, by = -.1)
x <- dat %>%
  dplyr::select(COMMERCIAL, INDUSTRIAL, INSTITUTIONAL, OPENSPACE, RESIDENTIAL,
                Cumu_Cases, Pct.Male, Pct.Age_0_24, Pct.Age_25_40, Pct.Age_40_65,
                Pct.White, Pct.Black, Pct.Indian, Pct.Asian, Income,
                PopDensity, Freq, Num_trips, WJob_OtherServices_Density, WJob_Utilities_Density,
                WJob_Goods_Product_Density, WTotal_Job_Density) %>%
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

## For ride
y <- dat$rides
# RIDGE
cv_fit <- cv.glmnet(x, y, alpha = 0, lambda = lambdas, family = "poisson")
plot(cv_fit)
opt_lambda <- cv_fit$lambda.min
# Rebuilding the model with optimal lambda value
best_ridge <- glmnet(x, y, alpha = 0, lambda = cv_fit$lambda.min, family = "poisson")
plot(best_ridge)
coef(best_ridge)

# PCA/PLS
m <- pls(x, y, 7, cv = 4, scale = TRUE, info = "Shoesize prediction model")
summary(m)
plotRegcoeffs(m)
show(m$coeffs$values[, 3, 1])
summary(m$coeffs)
m <- selectCompNum(m, 3)

# LASSO
cv_fit <- cv.glmnet(x, y, alpha = 1, lambda = lambdas)
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
                Pct.Age_25_40 +
                Pct.Age_40_65 +
                Pct.White +
                Pct.Black +
                Pct.Asian +
                Income +
                PopDensity +
                ti(LAT, LNG),
            data = dat, family = c("gaussian"), method = "REML")
summary(GAM_RES1)

## For rides
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
best_lasso <- glmnet(x, y, alpha = 1, lambda = cv_fit$lambda.min, family = "poisson")
coef(best_lasso)

# VIF/ALIAS
colnames(dat)
alias(
  lm(
    Relative_Impact ~ Primary +
      Secondary +
      Minor +
      COMMERCIAL +
      INDUSTRIAL +
      INSTITUTIONAL +
      OPENSPACE +
      RESIDENTIAL +
      LUM +
      Cumu_Cases +
      Pct.Male +
      Pct.Age_0_24 +
      Pct.Age_25_40 +
      Pct.Age_40_65 +
      Pct.White +
      Pct.Black +
      Pct.Indian +
      Pct.Asian +
      Pct.Unemploy +
      Income +
      College +
      Pct.Car +
      Pct.Transit +
      Pct.WorkHome +
      PopDensity +
      EmployDensity,
    data = dat
  )
)

vif_test <-
  lm(
    Relative_Impact ~
      COMMERCIAL +
        INDUSTRIAL +
        INSTITUTIONAL +
        OPENSPACE +
        RESIDENTIAL +
        LUM +
        Cumu_Cases +
        Pct.Male +
        Pct.Age_0_24 +
        Pct.Age_25_40 +
        Pct.Age_40_65 +
        Pct.White +
        Pct.Black +
        Pct.Indian +
        Pct.Asian +
        Pct.Unemploy +
        Income +
        College +
        Pct.Car +
        Pct.Transit +
        Pct.WorkHome +
        PopDensity,
    data = dat
  )
vif(vif_test)
summary(vif_test)
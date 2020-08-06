# A model to check transit causal impact in Chicago
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
library(reshape2)

dat <- read.csv('C:/Users/Songhua Hu/Desktop/Transit/Daily_Lstaion_Final.csv')
dat$date <- as.Date(dat$date)

# Get one station data
eachstation <- 40010
dat_Each <- dat[dat$station_id == eachstation,]
rownames(dat_Each) <- NULL
# We only consider the days after 03-02
# TEST 2 YEARS
dat_Each <- dat_Each[dat_Each$Year>=2019,]
rownames(dat_Each) <- NULL
first_enforce_day <- as.numeric(rownames(dat_Each[dat_Each$date==as.Date('2020-03-02'),]))
pre.period <- c(1, first_enforce_day - 1)  
post.period <- c(first_enforce_day, nrow(dat_Each))
# We keep a copy of the actual observed response in "post.period.response
post.period.response <- dat_Each$rides[post.period[1]:post.period[2]]
dat_Each$rides[post.period[1]:post.period[2]] <- NA
response <- zoo(dat_Each$rides, dat_Each$date)


# Build a bsts model
# ss <- AddLocalLevel(list(), dat_Each$rides)
# ss <- AddLocalLinearTrend(list(), dat_NY$Trips_person)
ss <- AddSemilocalLinearTrend(list(), response)
ss <- AddSeasonal(ss, response, nseasons = 7)
ss <- AddMonthlyAnnualCycle(ss, response)
# ss <- AddDynamicRegression(ss, Trips_person ~ National_Cases + PRCP + New_cases + TMAX + Adj_New_cases +Avg_Y,data = dat_NY)

bsts.model1 <- bsts(
  response ~ PRCP + TMAX + IsWeekend + Holidays, 
  state.specification = ss, niter = 2000, data = dat_Each, expected.model.size = 2)

### Get the number of burn-ins to discard
burn <- SuggestBurn(0.1, bsts.model1)

### Get the components for no variables
components.withreg <- cbind.data.frame(
  colMeans(bsts.model1$state.contributions[-(1:burn),"trend",]),
  colMeans(bsts.model1$state.contributions[-(1:burn),"seasonal.7.1",]),
  colMeans(bsts.model1$state.contributions[-(1:burn),"Monthly",]),
  colMeans(bsts.model1$state.contributions[-(1:burn),"regression",]),
  as.Date((dat_Each$date)))  
names(components.withreg) <- c("Trend", "Seasonality", "Monthly","Regression", "Date")
components.withreg <- melt(components.withreg, id.vars="Date")
names(components.withreg) <- c("Date", "Component", "Value")

ggplot(data=components.withreg, aes(x=Date, y=Value)) + geom_line() + 
  theme_bw() + theme(legend.title = element_blank()) + ylab("") + xlab("") + 
  facet_grid(Component ~ ., scales="free") + guides(colour=FALSE) + 
  theme(axis.text.x=element_text(angle = -90, hjust = 0))
# Coefficient
colMeans(bsts.model1$coefficients)
plot(bsts.model1, "coef")

# Estimating counterfactual and compare with actual post period response
impact <- CausalImpact(
  bsts.model = bsts.model1,
  post.period.response = post.period.response,
  model.args = list(nseasons = 7, season.duration = 1, dynamic.regression = TRUE))
summary(impact)
summary(impact, "report")
plot(impact)
impact$series
impact$summary



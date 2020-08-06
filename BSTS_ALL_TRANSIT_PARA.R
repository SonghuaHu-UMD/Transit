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

dat <-
  read.csv('C:/Users/hsonghua/Desktop/CausualImpact/Daily_Lstaion_Final.csv')
dat$date <- as.Date(dat$date)
AllCounty <- unique(dat$station_id)


# Setup parallel backend
cores <- detectCores()
cl <- makeCluster(cores[1] - 1)
registerDoParallel(cl)
finalMatrix <- data.frame()

# length(AllCounty)-1800
finalMatrix <-
  foreach(
    ccount = 1:length(AllCounty),
    .combine = rbind,
    .packages = c("CausalImpact")
  ) %dopar%
  {
    eachstation <- AllCounty[ccount]
    # eachstation <- 36061
    print (ccount)
    dat_Each <- dat[dat$station_id == eachstation,]
    rownames(dat_Each) <- NULL
    # Sometimes there is no stay-at-home
    # We only consider the days before the reopen guidelines
    first_enforce_day <- as.numeric(rownames(dat_Each[dat_Each$date==as.Date('2020-03-02'),]))
    pre.period <- c(1, first_enforce_day - 1)  
    post.period <- c(first_enforce_day, nrow(dat_Each))
    # We keep a copy of the actual observed response in "post.period.response
    post.period.response <- dat_Each$rides[post.period[1]:post.period[2]]
    dat_Each$rides[post.period[1]:post.period[2]] <- NA
    response <- zoo(dat_Each$rides, dat_Each$date)

    # Build a bsts model
    ss <- AddSemilocalLinearTrend(list(), response)
    ss <- AddSeasonal(ss, response, nseasons = 7)
    ss <- AddMonthlyAnnualCycle(ss, response)
    bsts.model1 <- bsts(
      response ~ PRCP + TMAX + IsWeekend + Holidays, 
      state.specification = ss, niter = 2000, data = dat_Each, expected.model.size = 2)
    # plot(bsts.model)
    # plot(bsts.model, "components")
    # plot(bsts.model, "coef")
    
    # Estiamting counterfactual and compare with actual post period response
    impact <- CausalImpact(
      bsts.model = bsts.model1,
      post.period.response = post.period.response)
    impact.plot <- plot(impact) + theme_bw(base_size = 20)+ 
      scale_x_date(date_breaks = "1 month",  labels=date_format("%b-%Y"),
                   limits = as.Date(c('2019-01-01','2020-05-01')))
    plot(impact.plot)
    # summary(impact)
    # summary(impact, 'report')
    temp_impact <- impact$summary
    temp_impact$CTFIPS <- eachstation
    tem_pred <- data.frame(impact$series)
    tem_pred$time <- (row.names(tem_pred))
    tem_pred$CTNAME <- eachstation
    tem_pred
  }
stopCluster(cl)
write.csv(finalMatrix,'finalMatrix_Transit.csv')

# xyplot(point.effect ~ time, groups=finalMatrix$CTNAME, data = finalMatrix)

finalMatrix_cut <- finalMatrix[seq(1, nrow(finalMatrix), 2), ]
finalMatrix_cut_pvalue <- finalMatrix_cut[finalMatrix_cut$p < 0.1, ]
summary(finalMatrix_cut)
summary(finalMatrix_cut_pvalue)


# Plot spatial
s1 <- st_read("C:/Users/hsonghua/Desktop/CausualImpact/National_County_4326.shp")
s1$GEOID <- as.integer(s1$GEOID)
colnames(s1)[4] <- "CTFIPS"
total_res <- sp::merge(s1, finalMatrix_cut_pvalue, by = "CTFIPS")
png("Causual-effect1.png", units="px", width=2400, height=1200, res=500)
tm_shape(total_res,projection = "EPSG:5070") +
  tm_polygons(
    style = "quantile",
    col = "AbsEffect",
    title = '',
    border.alpha = 0
  ) + tm_shape(s1,projection = "EPSG:5070") + tm_borders("Black", lwd = 0.5) +
  tm_layout(legend.title.size = 0.65, legend.text.size = 0.55)
dev.off()


# Merge with county
# Fit the casual effect
# Whether the soci-demographic of county is related to the casual effect
mean_dat_sub <-
  merge(x = mean_dat,
        y = finalMatrix_cut_pvalue,
        by = 'CTFIPS',
        all.y = TRUE)

alias(
  lm(
    AbsEffect ~ Pct_Male + Pct_Age_0_24 + Pct_Age_25_40 + Pct_Age_40_65  + Pct_White + Pct_Black + Pct_Asian +
      Population_density + Med_House_Income,
    data = mean_dat_sub
  )
)

vif_test <-
  lm(
    AbsEffect ~  Pct_Male + Pct_Age_0_24 + Pct_Age_25_40 + Pct_Age_40_65   + Pct_Black + Pct_Asian +
      Population_density + Med_House_Income,
    data = mean_dat_sub
  )
summary(vif_test)
vif(vif_test)

GAM_RES1 <-
  gam(
    AbsEffect ~ New_cases  + Adj_New_cases + Pct_Male + Pct_Age_0_24 + Pct_Age_25_40 + Pct_Age_40_65  + Pct_White + Pct_Black + Pct_Asian +
      Population_density + Med_House_Income ,
    data = mean_dat_sub,
    family = c("gaussian"),
    method = "REML"
  )

summary(GAM_RES1)
# Preserved R scratch code; requires the original R-session objects.
PLSR_$coefficients
x1 <- x
y0 <- predict(PLSR_, ncomp = 4, newdata = x)
y_list <- c()
for (jj in (1:10)) {
  x1[, 1] <- x[, 1] * jj
  y1 <- predict(PLSR_, ncomp = 4, newdata = x1)
  y_list[[jj]] <- mean(y1)
}
plot(1:10, y_list)

x1 <- x
x1[, 1] <- x[, 1] * 2
y1 <- predict(PLSR_, ncomp = 4, newdata = x1)
mean((y1 - y0)/y0)
sum(y1 - y0)/sum(y0)
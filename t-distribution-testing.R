?rt
nc <- -4.47213595499958
df <- 28
n <- 500000

nct_vals <- rt(n=n, df=df, nc=nc)
t_vals <- rt(n=n, df=df) + nc

plot(density(nct_vals), col="blue", ylim=c(0, 0.5))
lines(density(t_vals), col='red')


library(zoo)
library(xts)


# Evaluate dma(x) function to set global variables for DMAx
dma <- function (mat) {
  res <- 4*24
  inter <<- gsub (".", "h", substring (names (mat) [-1], 2), fixed = T)
  datas <<- as.Date (mat [, 1])
  ats <- format (datas, '%d') == '01'
  datas.g <<- paste (paste (format (as.Date (mat [, 1]), "%b"), format (as.Date (mat [, 1]), "%d")), ",", sep = "")
  dias <<- merge (inter, datas) [, 2]
  tempo <<- paste (merge (inter, datas) [, 2], merge (inter, datas) [, 1])
  tempo.g <<- paste (merge (inter, datas.g) [, 2], merge (inter, datas.g) [, 1])
  dias.da.semana <<- c ()
  for (i in 1:length (weekdays (datas))) dias.da.semana <<- c (dias.da.semana, rep (weekdays (datas) [i], res))
  horas <<- c (paste (0:23, "h", sep = ""), "0h")
  meses.ano <<- paste ( format (as.Date( mat[,1]),"%b"), format (as.Date (mat [, 1]), "%Y"))
  meses.do.ano <<- c ()
  for (i in 1:length (meses.ano)) meses.do.ano <<- c (meses.do.ano, rep (meses.ano [i], res))
  anos <<- paste ("(", first (unique (meses.ano)), " - ", last (unique (meses.ano)), ")", sep = "")
  ylab <<- expression (paste ("Water consumption (in ", m^3, "/h)"))
  ylabday <<- expression (paste ("Water consumption (in ", m^3, "/day)"))
  ylaberror <- expression(paste("Prediction error (in ", m^3, "/h)"))
  res <<- length (inter)
  y.t <<- ts (as.vector (t (as.matrix (mat [, -1])))) #Coloca os valores ordenados cronologicamente em função da hora e dia
  y.m <<- msts (as.vector (t (as.matrix (mat [, -1]))), seasonal.periods = c (res, (7*res)), ts.frequency = res)
  col1 <<- "firebrick1"
  col2 <<- "royalblue1"
  col3 <<- "seagreen"
  col4 <<- "darkgoldenrod1"
  col5 <<- "lightsalmon2"
  background.color <<- "white"
  daily.medians <<- sapply (lapply (split (y.t, f = dias), function (x) {median (x, na.rm = F)}), function (x) as.numeric (x))
  daily.means <<- sapply (lapply (split (y.t, f = dias), function (x) {mean (x, na.rm = F)}), function (x) as.numeric (x))
  daily.agg <<- sapply (split (y.t, dias), function (x) sum (x/4, na.rm = F)) #soma das médias de cada hora por cada dia
}




# Reconstruct using JQ approach (Level 1: Weekly TBATS; Level 2: median):
JQ.reconstruct <- function (y, measure) {

  daily.agg <- sapply (split (y, dias), function (x) sum (x/4, na.rm = F)) #Soma de todos os valores de cada dia do ano (dividido por 4)

  # Aggregated daily model
  daily.tbats.model <- function (agg.y) {
    for (i in 15:length (agg.y)) {
      if (is.na (agg.y [i]) && sum (is.na (agg.y [(i-14):(i-1)])) == 0) {
        mod <- tbats (ts (agg.y [(i-14):(i-1)]), seasonal.periods = 7) #Simula um modelo TBATS para cada observação missing em que não existem valores missing nos 15 dias anteriores
        pred <- forecast (mod, h = 1) $ mean
        agg.y [i] <- pred #Inclui o valor da predição na própria base de dados (podendo ser usados na predição de valores missing seguintes)
      }
    }
    agg.y
  }
  daily.flow.fc <- daily.tbats.model (daily.agg) #Modelo de agregação diária forecast
  daily.flow.bc <- rev (daily.tbats.model (rev (daily.agg))) #Modelo de agregação diária backcast
  daily.flow.TBATS <- colMeans (rbind (daily.flow.fc, daily.flow.bc), na.rm = T) #Média das predições dos modelos backcast e forecast

  agg.model <- data.frame (month = month.name [month (datas)], weekday = weekdays (datas), estimate = daily.flow.TBATS) #Lista com mês e dia da semana associado a cada valor da base de dados agregada (incluindo as predições)

  matriz <- t (matrix (y, nrow = res, ncol = 365)) #Reconstrução da série temporal original (transformando a série temporal em matriz)

  # 15-min flow model (with no clusters)
  DF <- data.frame (month = month.name [month (datas)], weekday = weekdays (datas), matriz) #Base de dados original em que é assocido o mês e o dia da semana de cada linha

  if (measure == "median") pat.func <- function (a) {if (nrow(a)!=0) {lapply (split (a [,-(1:2)], a$weekday), function (x) colMedians (as.matrix (x), na.rm = T))} else return(NULL)}
  if (measure == "mean") pat.func <- function (a) {lapply (split (a [,-(1:2)], a$weekday), function (x) colMeans (as.matrix (x), na.rm = T))}

  aux <- DF [which (DF$month == "January"),] #Valores da base de dados original correspondentes ao mês de Janeiro
  Jan <- pat.func (aux) #Para cada dia da semana do mês de Janeiro, é feita a mediana para cada variável excluindo os valores missing
  #(ou seja, faz-se a mediana entre todos os valores observados às, por exemplo, 00h dos domingos do mês de Janeiro).
  #Obtêm-se assim as medianas de cada hora observada para cada dia da semana do mês de Janeiro, ou seja, 96 valores para cada dia da semana.
  aux <- DF [which (DF$month == "February"),]
  Feb <- pat.func (aux)
  aux <- DF [which (DF$month == "March"),]
  Mar <- pat.func (aux)
  aux <- DF [which (DF$month == "April"),]
  Apr <- pat.func (aux)
  aux <- DF [which (DF$month == "May"),]
  May <- pat.func (aux)
  aux <- DF [which (DF$month == "June"),]
  Jun <- pat.func (aux)
  aux <- DF [which (DF$month == "July"),]
  Jul <- pat.func (aux)
  aux <- DF [which (DF$month == "August"),]
  Aug <- pat.func (aux)
  aux <- DF [which (DF$month == "September"),]
  Sep <- pat.func (aux)
  aux <- DF [which (DF$month == "October"),]
  Oct <- pat.func (aux)
  aux <- DF [which (DF$month == "November"),]
  Nov <- pat.func (aux)
  aux <- DF [which (DF$month == "December"),]
  Dec <- pat.func (aux)

  patterns <- list (January = Jan, February = Feb, March = Mar, April = Apr, May = May, June = Jun, July = Jul, August = Aug, September = Sep, October = Oct, November = Nov, December = Dec)
  #Para cada dia da semana de cada mês, tem-se as medianas para cada hora do dia observada, excluindo os valores missing

  y.p <- rep (NA, length (y))
  for (i in 1:length (y)) {
    if (is.na (y [i])) {
      ds <- dias.da.semana [i] #Dia da semana da observação missing
      me <- month.name [month (tempo [i])] #Mês da semana da observação missing
      ypk <- agg.model [which (rownames (agg.model) == dias [i]),] $ estimate #Valor predito pelo modelo agregado para o dia da observação missing
      ypat <- patterns [[me]] [[ds]] #Medianas de cada hora do dia da semana do mês da observação missing
      ypatki <- ypat [if (i%%res == 0) res else i%%res] #Mediana da hora do dia (do dia da semana do mês) da observação missing
      yp15 <- (ypatki / sum (ypat/4)) * ypk
      y.p [i] <- yp15
    }
  }
  y.p
}

# Reconstruct using TBATS approach (Combined Method)
forecast.reconstruct <- function (y) {
  yp <- rep (NA, length (y))

  pos.na <- which (is.na (y))
  spl.na <- split (pos.na, cumsum (c (0, diff (pos.na) != 1)))
  run.na <- list (lengths = unname (sapply (spl.na, length)), values = unname (spl.na))

  # List of sequences of missing values (positions)
  for (i in 1:length (run.na $ values)) {
    s <- run.na $ values [[i]]
    fs <- first (s)
    n <- 0
    m <- 0
    if (fs > 3*res*7) n <- 3 else if (fs > 2*res*7) n <- 2 else if (fs > res*7) n <- 1
    if (n > 0) {
      for (j in 1:n) {
        fc.set <- y [(fs-j*res*7):(fs-1)]
        if (sum (is.na (fc.set)) == 0) m <- j
      }
    }
    if (m > 0) {
      fc.set <- y [(fs-m*res*7):(fs-1)]
      mod <- tbats (ts (fc.set), seasonal.periods = c (res, res*7))
      fcast <- forecast (mod, h = run.na $ lengths [i]) $ mean
      yp [s] <- fcast
    }
  }
  yp
}
backcast.reconstruct <- function (y) {
  y <- rev (y)
  yp <- rep (NA, length (y))

  pos.na <- which (is.na (y))
  spl.na <- split (pos.na, cumsum (c (0, diff (pos.na) != 1)))
  run.na <- list (lengths = unname (sapply (spl.na, length)), values = unname (spl.na))

  # List of sequences of missing values (positions)
  for (i in 1:length (run.na $ values)) {
    s <- run.na $ values [[i]]
    fs <- first (s)
    n <- 0
    m <- 0
    if (fs > 3*res*7) n <- 3 else if (fs > 2*res*7) n <- 2 else if (fs > res*7) n <- 1
    if (n > 0) {
      for (j in 1:n) {
        fc.set <- y [(fs-j*res*7):(fs-1)]
        if (sum (is.na (fc.set)) == 0) m <- j
      }
    }
    if (m > 0) {
      fc.set <- y [(fs-m*res*7):(fs-1)]
      mod <- tbats (ts (fc.set), seasonal.periods = c (res, res*7))
      fcast <- forecast (mod, h = run.na $ lengths [i]) $ mean
      yp [s] <- fcast
    }
  }
  rev (yp)
}
combine.pred <- function (y, fc, bc) {
  combine.vec <- function (fore, back) {
    l <- length (fore)
    vec <- rep (NA, l)
    ai <- function (i) {
      if (l == 1) 0.5
      else (l-i)/(l-1)
    }
    for (j in 1:l) {
      vec [j] <- ai(j)*fore[j]+(1-ai(j))*back[j]
    }
    vec
  }

  yp <- rep (NA, length (y))

  pos.na <- which (is.na (y))
  spl.na <- split (pos.na, cumsum (c (0, diff (pos.na) != 1)))
  run.na <- list (lengths = unname (sapply (spl.na, length)), values = unname (spl.na))

  for (i in 1:length (run.na$values)) {
    s <- run.na$values[[i]]
    if (sum (is.na (fc [s])) > 0) yp [s] <- bc [s]
    if (sum (is.na (bc [s])) > 0) yp [s] <- fc [s]
    if (sum (is.na (fc [s])) == 0 && sum (is.na (bc [s])) == 0) {
      yp [s] <- combine.vec (fc [s], bc [s])
    }
  }
  yp
}
# Final method (Combined Method):
TBATS.reconstruct <- function (Y) {
  forecast.estimates <- forecast.reconstruct (Y)
  backcast.estimates <- backcast.reconstruct (Y)
  combination.estimates <- combine.pred (Y, forecast.estimates, backcast.estimates)
  combination.estimates
}

res <- 4*24
ylab <- expression (paste ("Water consumption (in ", m^3, "/h)"))
ylabday <- expression (paste ("Water consumption (in ", m^3, "/day)"))
ylaberror <- expression(paste("Prediction error (in ", m^3, "/h)"))

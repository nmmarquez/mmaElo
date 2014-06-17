 library (linHierarchy)

### first lets load in the data
fights <- read.csv ('~/Google Drive/Elo_Ranking/testing/mma/mma.csv',
                   stringsAsFactors = F, na.strings = 'N/A') [,1:11] [,-3]

one55 <- as.vector (read.csv('~/Google Drive/Elo_Ranking/testing/mma/one55.csv',
                             stringsAsFactors = F, na.strings = 'N/A') [,1])

eli <- as.vector(read.csv('~/Google Drive/Elo_Ranking/testing/mma/eligible.csv',
                          stringsAsFactors = F, na.strings = 'N/A') [,1])

### lets change that outcome variable to numeric

outcomeTranz <- function (vec){
    lower <- tolower (vec)
    new <- vector('numeric')
    for (i in 1:length (lower)){
        if (grepl ('win', lower [i])){new [i] <- 1}
        else if (grepl ('loss', lower [i])){new [i] <- -1}
        else if (grepl ('draw', lower [i])){new [i] <- 0}
        else{new [i] <- NA}
    }
    new
}

fights$outcome <- outcomeTranz (fights$outcome)

### we need the dates now
getDate <- function (vec){
    sapply (vec, function (x) paste0 (strsplit (x, '') [[1]] [2:11],
                                      collapse=''))
}

fights$date <- getDate (fights$date)


### now we need to reaarange the fight table to look for duplicates
alphaTab <- function (dat){
    alpha <- dat; names (alpha) [c(1,3)] <- c('player.1', 'player.2')
    for (i in 1:nrow(alpha)){
        if (!all (sort (c(alpha [i,1], alpha [i,3])) ==
                             c(alpha [i,1], alpha [i,3]))){
            temp <- sort (c (alpha [i,1], alpha [i,3]))
            alpha [i,1] <- temp [1]
            alpha [i,3] <- temp [2]
            alpha [i,2] <- -1 * alpha [i,2]
        }
    }
    return (alpha)
}

alpha <- alphaTab (fights) [,c(1,3,2,6)]
uniFights <- unique (alpha)

### lets subset by eligable fighters and 155
eliFights <- subset (uniFights, player.1 %in% eli & player.2 %in% eli)
fights155 <- subset (uniFights, player.1 %in% one55 & player.2 %in% one55)

### linHierarchy go!!!
fightInt <- intTableConv (fights155, format = '%Y-%m-%d')

eloF <- eloTable (fightInt)
extractScores (eloF) [1:20,]

mycol <- c('red', 'green', 'black', 'blue', 'orange', 'pink', 'purple', 
                 'brown', 'yellow', 'grey')

plot (eloF, players = extractScores (eloF, tObj = Sys.time()) [1:7,'player'],
      col = mycol, lty = 6, lwd = 3, ylab = 'Elo Rating', xlab = 'Year', 
      legend = FALSE, main ='Top 7 Elo Ratings for Lightweight MMA Fighters')

legend ('topleft', paste (extractScores (eloF) [1:7, 'player'],
                          as.character (extractScores (eloF) [1:7, 'score'])),
        col = mycol, lty = 6, lwd = 3)


ufc7 <- c('Anthony Pettis','Benson Henderson','Gilbert Melendez','Josh Thomson',
          'Khabib Nurmagomedov', 'Rafael dos Anjos', 'Donald Cerrone')

ufc7Scr <- extractScores (eloF, players=ufc7)

plot (eloF, players = ufc7,col = mycol, lty = 6,lwd = 3, ylab = 'Elo Rating',
      xlab = 'Year',legend = FALSE, main ='Top 7 UFC MMA Lightweights Elo Rating')


legend ('topleft', paste (ufc7,
                          as.character (ufc7Scr [match (ufc7, ufc7Scr$player), 
                                                 'score'])),
        col = mycol, lty = 6, lwd = 3)

### Higest Scores?

top <- function (eloTab, intTab, int = 5){
    topSc <- eloTab$eloTable[order(-eloTab$eloTable$score),]
    unique <- topSc [!duplicated (topSc$player),] [1:int,]
    ints <- intTab$interactions
    for (i in 1:nrow (unique)){
        print (list (subset (ints, (player.1 == unique [i,1] |
                                        player.2 == unique [i,1]) & 
                                 datetime == unique [i,3]), unique [i,2]))
    }
}

top (eloF, fightInt, 5)

### Biggest upsets?

upset <- function (eloTab, intTab, int = 5){
    plyrs <- eloTab$players; ET <- eloTab$eloTable; min <- 0
    df <- data.frame (player = NA, date = NA, margin = vector ('numeric', int))
    df$player <- as.character(df$player); df$date <- as.POSIXct (df$date)
    eloLis <- lapply (plyrs, function (x) subset (ET, player == x))
    ints <- intTab$interactions
    for (i in 1:length (eloLis)){
        for (j in 2:nrow (eloLis [[i]])){
            if (eloLis [[i]] [j,2] - eloLis [[i]] [j - 1,2] > min){
                df [int,3] <- eloLis [[i]] [j,2] - eloLis [[i]] [j - 1,2]
                df [int,1] <- eloLis [[i]][j,1]; df [int,2] <- eloLis [[i]][j,3]
                df <- df [order (-df$margin),]; min <- df$margin [int]
            }
        }
    }
    for (i in 1:nrow (df)){
        print (list (subset (ints, (player.1 == df [i,1] |
                                        player.2 == df [i,1]) & 
                                 datetime == df [i,2]), df [i,3]))
    }
}

upset (eloF, fightInt)
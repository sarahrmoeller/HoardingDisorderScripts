all.data <- read.csv("./out/embedding_call_response_table.csv")
all.data2 <- read.csv("./out/embedding_call_response_per_transcript_table.csv")
all.data3 <- read.csv("./out/embedding_call_response_per_transcript_long_table.csv")
# Remove unnecessary columns
data <- all.data[]
data2 <- all.data2[]
names(all.data)

# Simple regression on call-response similarity per hoarding flag
similarity.slr <- glm(Hoarder.Flag ~ Similarity, data = all.data, family = "binomial")
summary(similarity.slr)

# Filtering out short calls and responses
data.filtered2 <- all.data[nchar(all.data$Call) > 10 & nchar(all.data$Response) > 10, ]
similarity.slr2 <- glm(Hoarder.Flag ~ Similarity, data = data.filtered2, family = "binomial")
summary(similarity.slr2)

# Filtering only short calls or responses
data.filtered3 <- all.data[nchar(all.data$Call) <= 10 | nchar(all.data$Response) <= 10, ]
similarity.slr3 <- glm(Hoarder.Flag ~ Similarity, data = data.filtered3, family = "binomial")
summary(similarity.slr3)

# Filtering only short calls and responses
data.filtered4 <- all.data[nchar(all.data$Call) <= 10 & nchar(all.data$Response) <= 10, ]
similarity.slr4 <- glm(Hoarder.Flag ~ Similarity, data = data.filtered4, family = "binomial")
summary(similarity.slr4)

# Filtering only short calls
data.filtered5 <- all.data[nchar(all.data$Call) <= 10, ]
similarity.slr5 <- glm(Hoarder.Flag ~ Similarity, data = data.filtered5, family = "binomial")
summary(similarity.slr5)

# Filtering only short responses
data.filtered6 <- all.data[nchar(all.data$Response) <= 10, ]
similarity.slr6 <- glm(Hoarder.Flag ~ Similarity, data = data.filtered6, family = "binomial")
summary(similarity.slr6)

# Simple regression on call-response mean similarity per transcript vs hoarding flag
similarity.slr7 <- glm(Hoarder.Flag ~ Mean, data = all.data2, family = "binomial")
summary(similarity.slr7)

# Simple regression on call-response std similarity per transcript vs hoarding flag
similarity.slr8 <- glm(Hoarder.Flag ~ Std, data = all.data2, family = "binomial")
summary(similarity.slr8)

# Simple regression on call-response mean & std similarity per transcript vs hoarding flag
similarity.mlr9 <- glm(Hoarder.Flag ~ Mean + Std, data = all.data2, family = "binomial")
summary(similarity.mlr9)

# Simple regression on call-response mean similarity per transcript vs hoarding flag
similarity.slr10 <- glm(Hoarder.Flag ~ Mean, data = all.data3, family = "binomial")
summary(similarity.slr10)

# Simple regression on call-response std similarity per transcript vs hoarding flag
similarity.slr11 <- glm(Hoarder.Flag ~ Std, data = all.data3, family = "binomial")
summary(similarity.slr11)

# Simple regression on call-response mean & std similarity per transcript vs hoarding flag
similarity.mlr12 <- glm(Hoarder.Flag ~ Mean + Std, data = all.data3, family = "binomial")
summary(similarity.mlr12)

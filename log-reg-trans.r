all.data <- read.csv("./out/transcript_table.csv")
all.data <- all.data[, names(all.data) != "Transcript"] # Remove Transcript column
names(all.data)

# Simple regression on total labels per document
total.slr <- glm(Hoarder.Flag ~ Total, data = all.data, family = "binomial")
summary(total.slr)

# Regression model by speaker
total.rows <- names(all.data)[grepl("Total", names(all.data))]
labels.by.speaker <- all.data[, !(names(all.data) %in% total.rows)]
names(labels.by.speaker)
speaker.mlr <- glm(Hoarder.Flag ~ ., data = labels.by.speaker[, !grepl("Interviewer", names(labels.by.speaker))], 
                   family = "binomial")
summary(speaker.mlr)

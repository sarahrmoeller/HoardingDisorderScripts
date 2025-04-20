all.data <- read.csv("./out/table.csv")
all.data <- all.data[, !(names(all.data) %in% c("Project", "Document.Name"))] # Remove project and document names
names(all.data)

# Simple regression on total labels per document
total.slr <- glm(Hoarder.Flag ~ Total, data = all.data, family = "binomial")
summary(total.slr)

# Regression model by speaker
total.rows <- names(all.data)[grepl("Total", names(all.data))]
labels.by.speaker <- all.data[, !(names(all.data) %in% total.rows)]
names(labels.by.speaker)
speaker.mlr <- glm(Hoarder.Flag ~ ., data = labels.by.speaker, family = "binomial")
summary(speaker.mlr)

# Sanity check: if we regress on the total like this, we should get the same coefficients
total.rows <- total.rows[!total.rows == "Total"] # don't include the Total column
labels.by.total <- all.data[, c("Hoarder.Flag", total.rows)]
total.mlr <- glm(Hoarder.Flag ~ ., data = labels.by.total, family = "binomial")
summary(total.mlr)
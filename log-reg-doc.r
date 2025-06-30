all.data <- read.csv("./out/table.csv")
all.data <- all.data[, !(names(all.data) %in% c("Project", "Document.Name"))] # Remove project and document names
names(all.data)

# Simple regression on total labels per document
total.slr <- glm(Hoarder.Flag ~ Total, data = all.data, family = "binomial")
summary(total.slr)

library(ggplot2)
ggplot(all.data, aes(Total, Hoarder.Flag)) + 
    geom_point(position=position_jitter(h=2e-3,w=2e-3)) +
    theme_gray(base_size = 24) +
    stat_smooth(method="glm", color="red", se=FALSE,
            method.args = list(family=binomial)) +
    labs(x="Total Labels", y="Hoarder Flag")

# Regression model by speaker
total.rows <- names(all.data)[grepl("Total", names(all.data))]
labels.by.speaker <- all.data[, !(names(all.data) %in% total.rows)]
names(labels.by.speaker)
speaker.label.mlr <- glm(Hoarder.Flag ~ . - TTR - ASL, data = labels.by.speaker, family = "binomial")
speaker.label.part.mlr <- glm(Hoarder.Flag ~ . - TTR - ASL, data = labels.by.speaker[, !grepl("Interviewer", names(labels.by.speaker))],
                              family = "binomial")
speaker.mlr <- glm(Hoarder.Flag ~ ., data = labels.by.speaker, family = "binomial")
summary(speaker.mlr)
summary(speaker.label.mlr)
summary(speaker.label.part.mlr)

# Sanity check: if we regress on the total like this, we should get the same coefficients
total.rows <- total.rows[!total.rows == "Total"] # don't include the Total column
labels.by.total <- all.data[, c("Hoarder.Flag", total.rows)]
total.mlr <- glm(Hoarder.Flag ~ ., data = labels.by.total, family = "binomial")
summary(total.mlr)

write.table(all.data[, c("Total", "Hoarder.Flag")],
            row.names = FALSE, sep = "\t",
            file = "./out/total_labels.tsv")

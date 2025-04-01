data <- read.csv("./out/label_counts.csv")
# Remove names
data <- data[, !(names(data) %in% c("Project", "Document.Name"))]

mdl1 <- glm(Hoarder.Flag ~ . - Total, data = data, family = "binomial")
summary(mdl1)

mdl2 <- glm(Hoarder.Flag ~ Total, data = data, family = "binomial")
summary(mdl2)

mdl3 <- glm(Hoarder.Flag ~ . - Misspeak - Unclear - Total, data = data, family = "binomial")
summary(mdl3)

mdl4 <- glm(Hoarder.Flag ~ . - Self.Correction - Misspeak - Unclear - Total, data = data, family = "binomial")
summary(mdl4)
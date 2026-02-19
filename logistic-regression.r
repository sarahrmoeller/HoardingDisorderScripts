label.counts <- read.csv("./out/label_counts.csv")

# Make it so all documents that start with 0 start with 1 instead
for (i in which(startsWith(label.counts$Document.Name, "0"))) { 
  label.counts$Document.Name[i] <- paste("1", label.counts$Document.Name[i], 
                                         sep="")
}

ling.data <- read.csv("./out/linguistic_data.csv")

# The ling data doesn't have all of the same documents as in label.counts, so
# so we will remove their difference
missing_docs <- setdiff(label.counts$Document.Name, ling.data$Document.Name)
label.counts <- label.counts[-which(label.counts$Document.Name %in% missing_docs), ]
nrow(label.counts)

# Merge the two dataframes by Document.Name, keeping all rows from label.counts
data <- merge(label.counts, ling.data, by = "Document.Name", all.x = TRUE)

# Now for the model
mdl <- glm(Hoarder.Flag ~ Clarification.Participant + 
                          Self.Correction.Participant + 
                          Incomplete.Thought.Participant + Overlap.Participant + 
                          Generic.Disfluency.Participant +
                          + TTR + NPR + ASL,
           data = data, family = binomial(link = "logit"))
summary(mdl)

# Add embeddings to the dataframe
embeddings_table <- read.csv("out/embedding_call_response_table.csv")

# Aggregate mean and sd of Similarity by Document.Name
embeddings_summary <- aggregate(Similarity ~ Document.Name,
                                embeddings_table,
                                function(x) {
                                  c(mean = mean(x, na.rm = TRUE),
                                    sd = sd(x, na.rm = TRUE))
                                })
embeddings_summary$Similarity.mean <- embeddings_summary[["Similarity"]][, 1]
embeddings_summary$Similarity.sd <- embeddings_summary[["Similarity"]][, 2]
embeddings_summary["Similarity"] <- NULL
head(embeddings_summary)
names(embeddings_summary)

# Merge with data by Document.Name
data <- merge(data, embeddings_summary,
              by = "Document.Name", all.x = TRUE)
head(data)
names(data)

library(stargazer)

p.values <- summary(model2)$coefficients[, "Pr(>|z|)"]
display_labels <- c(
  "Clarification (Participant)",
  "Self-Correction (Participant)",
  "Incomplete Thought (Participant)",
  "Overlap (Participant)"
)

stargazer(model2,
          title = "Multiple Logistic Regression Model",
          intercept.bottom = FALSE, # want intercept on the top
          no.space = TRUE,
          report = "*vcp")

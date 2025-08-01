all.data <- read.csv("./out/document_table.csv")
# Remove project names (we will remove document names soon, but not yet)
data <- all.data[, names(all.data) != "Project"]
names(data)

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

# Now we can remove Document.Name
data <- data[, names(data) != "Document.Name"]

# "Joining" CLF and SC columns
data[["CLF.or.SC.Participant"]] <- (data[["Clarification.Participant"]] +
                                      data[["Self.Correction.Participant"]])

labels <- c("Clarification", "Incomplete.Thought", "Misspeak",
            "Self.Correction", "Generic.Disfluency", "Overlap", "Unclear")

# Get all columns that we care about:
total_cols <- names(data)[grepl("Total", names(data))]
participant_cols <- names(data)[grepl("Participant", names(data))]
# Removing Multicollinear columns
# TTR.sent.Participant gives the same as TTR.Participant
# We will investigate CLF.or.SC.Participant soon
participant_cols <- participant_cols[!grepl("sent|CLF.or.SC.Participant",
                                            participant_cols)]
# Add in similarity columns
sim_cols <- names(data)[grepl("Similarity", names(data))]
relevant_cols <- c(participant_cols, sim_cols)
# Removing unimportant columns
unimportant_columns <- c("Misspeak", "Unclear")
relevant_cols <- relevant_cols[!grepl(paste(unimportant_columns,
                                            collapse = "|"),
                                      relevant_cols)]
biased_columns <- c("Generic.Disfluency", "ASL")
relevant_cols_unbiased <- relevant_cols[!grepl(paste(biased_columns,
                                                     collapse = "|"),
                                               relevant_cols)]
cols_unbiased_combined <-
  c(relevant_cols_unbiased[!grepl("Clarification|Self.Correction",
                                  relevant_cols_unbiased)],
    "CLF.or.SC.Participant")

columns_list <- list(
  "Total" = "Total",
  "All relevant Columns" = relevant_cols,
  "Unbiased Columns" = relevant_cols_unbiased,
  "Using Combined CLF + SC" = cols_unbiased_combined,
  "No TTR" = cols_unbiased_combined[!grepl("TTR", cols_unbiased_combined)],
  "No mean" = cols_unbiased_combined[!grepl("mean", cols_unbiased_combined)],
  "No TTR nor mean" = cols_unbiased_combined[!grepl("TTR|mean",
                                                    cols_unbiased_combined)],
  "No TTR nor mean nor sd" = cols_unbiased_combined[!grepl("TTR|mean|sd",
                                                    cols_unbiased_combined)]
)

# Create a model for each set of columns
mdls <- setNames(lapply(columns_list, function(cols) {
  glm(Hoarder.Flag ~ ., data = data[, c("Hoarder.Flag", cols)],
      family = "binomial")
}), names(columns_list))
lapply(mdls, summary)

library(car)

lapply(mdls[-1], vif) # Skip the total model for VIF

write.table(data[, c("Total", "Hoarder.Flag")],
            row.names = FALSE, sep = "\t",
            file = "./out/total_labels.tsv")

library(lme4)

model <- glmer(
  Hoarder.Flag ~ CLF.or.SC.Participant + Incomplete.Thought.Participant +
    Overlap.Participant + TTR.Participant + NP.ratio.Participant +
    (1 | Generic.Disfluency.Participant) +
    (1 | Misspeak.Participant) +
    (1 | ASL.Participant) +
    (1 | Unclear.Participant),
  data = data,
  family = binomial(link = "logit")
)
summary(model)

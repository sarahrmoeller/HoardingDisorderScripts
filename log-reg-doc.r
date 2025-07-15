all.data <- read.csv("./out/document_table.csv")
# Remove project and document names
data <- all.data[, !(names(all.data) %in% c("Project", "Document.Name"))]
names(data)

# "Joining" CLF and SC columns
data[["CLF.or.SC.Participant"]] <- (data[["Clarification.Participant"]] +
                                      data[["Self.Correction.Participant"]])

# Fix columns with lists in them instead of numbers
pylist_to_vec <- function(l) {
  l <- gsub("\\[|\\]", "", l)  # Remove brackets
  l <- strsplit(l, ",")[[1]]   # Split by comma
  as.numeric(trimws(l))        # Convert to numeric and trim whitespace
}

for (col in names(data)[grepl("NP", names(data))]) {
  for (i in seq_along(data[[col]])) {
    entry <- data[[col]][i]
    entry <- pylist_to_vec(entry)
    if (grepl("counts", col)) {
      # NP count lists are lists of counts of NPs in each sentence,
      # so we need to sum them up
      entry <- sum(entry, na.rm = TRUE)
    } else if (grepl("ratio", col)) {
      # NP ratio lists are lists of NPs ratios in each sentence,
      # for simplicity we will take the mean
      entry <- mean(entry, na.rm = TRUE)
    }
    data[[col]][i] <- as.numeric(entry)
  }
  data[[col]] <- as.numeric(data[[col]])
}

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
# Removing biased or unimportant labels
biased_or_unimportant_columns <- c("Generic.Disfluency", "ASL", # Biased
                                   "Misspeak", "Unclear") # Unimportant
filtered_participant_cols <-
  participant_cols[!grepl(paste(biased_or_unimportant_columns,
                                collapse = "|"),
                          participant_cols)]
columns_list <- list(
  "Total" = "Total",
  "Participant Columns" = participant_cols,
  "Filtered Participant Columns" = filtered_participant_cols,
  "Using Combined CLF + SC" = c(filtered_participant_cols[!grepl("Clarification|Self.Correction", 
                                                          filtered_participant_cols)], 
                                "CLF.or.SC.Participant")
)

# Create a model for each set of columns
mdls <- setNames(lapply(columns_list, function(cols) {
  glm(Hoarder.Flag ~ ., data = data[, c("Hoarder.Flag", cols)],
      family = "binomial")
}), names(columns_list))
mdls[["Interaction Term"]] <- glm(Hoarder.Flag ~ . + Clarification.Participant *
                                    Self.Correction.Participant,
                                  data = data[, c("Hoarder.Flag",
                                                columns_list[[length(columns_list)]])],
                                family = "binomial")
lapply(mdls, summary)

library(car)

lapply(mdls[-1], vif) # Skip the total model for VIF

write.table(data[, c("Total", "Hoarder.Flag")],
            row.names = FALSE, sep = "\t",
            file = "./out/total_labels.tsv")

heatmap(cormat)

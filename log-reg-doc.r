all.data <- read.csv("./out/document_table.csv")
# Remove project and document names
data <- all.data[, !(names(all.data) %in% c("Project", "Document.Name"))]
names(data)

# Fix columns with lists in them instead of numbers
pylist_to_vec <- function(l) {
  l <- gsub("\\[|\\]", "", l)  # Remove brackets
  l <- strsplit(l, ",")[[1]]   # Split by comma
  as.numeric(trimws(l))         # Convert to numeric and trim whitespace
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
total_rows <- names(data)[grepl("Total", names(data))]
extra_rows <- names(data)[grepl("TTR|ASL|NP", names(data))]
label_rows <- names(data)[grepl(paste(labels, collapse = "|"),
                                names(data)) & !grepl("Total", names(data))]
columns_list <- list("Total" = "Total",
                     "Labels by Speaker" = label_rows,
                     "Non-Total Columns" =
                       names(data)[!(names(data) %in%
                                     c(total_rows, "Hoarder.Flag"))],
                     "Participant Labels w/ extra" =
                       names(data)[grepl("Participant", names(data))])

# Create a model for each set of columns
mdls <- setNames(lapply(columns_list, function(cols) {
  glm(Hoarder.Flag ~ ., data = data[, c("Hoarder.Flag", cols)],
      family = "binomial")
}), names(columns_list))
lapply(mdls, summary)

glm(Hoarder.Flag ~ ., data = data[, c("Hoarder.Flag", columns_list[[4]])],
    family = "binomial")

write.table(data[, c("Total", "Hoarder.Flag")],
            row.names = FALSE, sep = "\t",
            file = "./out/total_labels.tsv")

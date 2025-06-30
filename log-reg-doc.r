all.data <- read.csv("./out/document_table.csv")
# Remove project and document names
data <- all.data[, !(names(all.data) %in% c("Project", "Document.Name"))]
names(data)

# Get all columns that we care about:
total_rows <- names(data)[grepl("Total", names(data))]
columns_list <- list("Total",
                     total_rows,
                     names(data)[!(names(data) %in%
                                     c(total_rows, "ASL", "TTR",
                                       "Hoarder.Flag"))],
                     names(data)[grepl("Participant", names(data))])
names(columns_list) <- c("Total",
                         "Labels by Total",
                         "Labels by Speaker, with ASL and TTR",
                         "Participant-Only Labels")

# Create a model for each set of columns
mdls <- setNames(
  lapply(columns_list, function(cols) {
    glm(Hoarder.Flag ~ ., data = data[, c("Hoarder.Flag", cols)],
        family = "binomial")
  }),
  names(columns_list)
)
lapply(mdls, summary)

write.table(data[, c("Total", "Hoarder.Flag")],
            row.names = FALSE, sep = "\t",
            file = "./out/total_labels.tsv")

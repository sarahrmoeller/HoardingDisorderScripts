all.data <- read.csv("./out/transcript_table.csv")
# Remove transcripts 2005 and 2008 as their speaker detection is broken
# right now
all.data <- all.data[!(all.data$Transcript %in% c("2005", "2008")), ]
all.data <- all.data[, names(all.data) != "Transcript"] # Remove Transcript column
names(all.data)

mdl <- glm(Hoarder.Flag ~ Incomplete.Thought.Participant +
             Clarification.Participant +
             Overlap.Participant +
             Self.Correction.Participant,
           data = all.data, family = "binomial")
summary(mdl)

all.data <- read.csv("./out/transcript_table.csv")
names(all.data)

mdl <- glm(Hoarder.Flag ~ Incomplete.Thought.Participant +
             Clarification.Participant +
             Overlap.Participant +
             Self.Correction.Participant,
           data = all.data, family = "binomial")
summary(mdl)

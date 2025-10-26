library(ggplot2)

# Data frame with predictors, estimates, SEs
coef_df <- data.frame(
  Predictor = c("Generic.Disfluency","Misspeak","Incomplete.Thought",
                "Clarification","Unclear","Overlap","Self.Correction"),
  Estimate = c(-0.13398, -0.04586, 0.36519, 0.54045, -0.35011, 0.75987, 0.21729),
  SE = c(0.05252, 0.48203, 0.09668, 0.14618, 0.31509, 0.14915, 0.21805)
)

# Compute confidence intervals
coef_df$CI_low <- coef_df$Estimate - 1.96 * coef_df$SE
coef_df$CI_high <- coef_df$Estimate + 1.96 * coef_df$SE

# Add significance manually (based on p-values from your output)
coef_df$Significance <- c("Significant Negative", "Not Significant", 
                          "Significant Positive", "Significant Positive", 
                          "Not Significant", "Significant Positive", 
                          "Not Significant")

# Define colors: red = significant positive, blue = significant negative, gray = non-significant
coef_df$Color <- ifelse(coef_df$Significance == "Significant Positive", "red",
                        ifelse(coef_df$Significance == "Significant Negative", "blue", "gray"))

# Plot
ggplot(coef_df, aes(x = Estimate, y = Predictor, color = Color)) +
  geom_point(size = 3) +
  geom_errorbar(aes(xmin = CI_low, xmax = CI_high),
                height = 0.2, linewidth = 1,
                orientation = "y") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  scale_color_identity() +
  theme_minimal(base_size = 14) +
  labs(x = "Estimate (log odds)", 
       y = "Predictor",
       title = "Predictors of Hoarder Classification (Color-Coded Significance)") +
  theme(panel.grid.minor = element_blank(),
        panel.grid.major.y = element_line(color = "gray90"),
        plot.title = element_text(hjust = 0.5))

export const mapScoreToCategory = (severityScore: number): string => {
  if (severityScore > 0 && severityScore < 4.0) {
    return "low";
  } else if (severityScore >= 4.0 && severityScore < 7.0) {
    return "medium";
  } else if (severityScore >= 7.0 && severityScore < 9.0) {
    return "high";
  }

  return "critical";
};

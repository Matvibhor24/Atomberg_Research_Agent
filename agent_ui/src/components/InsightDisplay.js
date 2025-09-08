export default function InsightDisplay({ insight }) {
  if (!insight) return null;
  return (
    <div>
      <h2>Marketing Insights</h2>
      <p>{typeof insight.narrative === "object" ? JSON.stringify(insight.narrative) : insight.narrative}</p>
      <p>{typeof insight.rule_based === "object" ? JSON.stringify(insight.rule_based) : insight.rule_based}</p>
    </div>
  );
}

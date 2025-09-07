export default function InsightDisplay({ insight }) {
  if (!insight) return null;
  return (
    <div>
      <h2>Marketing Insights</h2>
      <p>{insight.narrative || insight.rule_based}</p>
    </div>
  );
}

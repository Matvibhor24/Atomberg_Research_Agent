export default function MetricsDisplay({ metrics }) {
  if (!metrics) return null;
  return (
    <div>
      <h2>Brand Metrics</h2>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
    </div>
  );
}

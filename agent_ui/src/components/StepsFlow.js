// src/components/StepsFlow.jsx
const steps = [
  "Keyword & Brand Setup",
  "Data Retrieval",
  "Noise Filtering",
  "Brand Tagging",
  "Engagement Aggregation",
  "Sentiment Analysis",
  "Metric Computation",
  "Insight Generation",
];

export default function StepsFlow({ currentStep, errorStep = null }) {
  return (
    <ol
      className="list-group list-group-numbered"
    >
      {steps.map((step, idx) => {
        const stepNum = idx + 1;
        let className =
          "list-group-item d-flex justify-content-between align-items-center";
        let status = null;

        if (stepNum < currentStep) {
          className += " list-group-item-success";
          status = <span className="badge bg-success">&#10003;</span>; // check mark
        } else if (stepNum === currentStep) {
          if (errorStep === stepNum) {
            className += " list-group-item-danger";
            status = <span className="badge bg-danger">Error</span>;
          } else {
            className += " list-group-item-info";
            status = <span className="badge bg-primary">In Progress</span>;
          }
        } else {
          status = <span className="badge bg-secondary">Pending</span>;
        }

        return (
          <li key={step} className={className}>
            {step}
            {status}
          </li>
        );
      })}
    </ol>
  );
}

// src/App.jsx
import { useState } from "react";
import InputPanel from "./components/InputPanel";
import Tabs from "./components/Tabs";
import StepsFlow from "./components/StepsFlow";
import SourcesDisplay from "./components/SourcesDisplay";
import MetricsDisplay from "./components/MetricsDisplay";
import InsightDisplay from "./components/InsightDisplay";
import { runAgent, runAgentWithProgress } from "./api/agentApi";

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

export default function App() {
  const [agentOutput, setAgentOutput] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [activeTab, setActiveTab] = useState("steps");
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState(null);

  const handleRun = async ({ keywords, n }) => {
    setIsRunning(true);
    setError(null);
    setCurrentStep(0);
    setAgentOutput(null);

    try {
      await runAgentWithProgress(
        { keywords, n },
        // onProgress
        (progressData) => {
          console.log("Progress:", progressData);
          if (progressData.status === "in_progress") {
            setCurrentStep(progressData.currentStep);
          } else if (progressData.status === "completed") {
            setCurrentStep(progressData.currentStep);
          } else if (progressData.status === "error") {
            setError(
              `Step ${progressData.stepName} failed: ${progressData.error}`
            );
            setIsRunning(false);
          }
        },
        // onComplete
        (result) => {
          console.log("Complete:", result);
          setAgentOutput({
            sources: result.sources,
            metrics: result.metrics,
            insights: result.insights,
          });
          setCurrentStep(9); // All steps completed (8 steps + 1 to show all as completed)
          setIsRunning(false);
        },
        // onError
        (errorMessage) => {
          console.error("Error:", errorMessage);
          setError(errorMessage);
          setIsRunning(false);
        }
      );
    } catch (err) {
      console.error("Failed to start agent:", err);
      setError(err.message);
      setIsRunning(false);
    }
  };

  return (
    <div className="container py-4">
      <h1 className="text-center mb-4 fw-bold">
        Atomberg Market Research Agent UI
      </h1>

      <InputPanel onRun={handleRun} isRunning={isRunning} />

      {error && (
        <div className="alert alert-danger" role="alert">
          <strong>Error:</strong> {error}
        </div>
      )}

      <Tabs activeTab={activeTab} onChange={setActiveTab} />

      {activeTab === "steps" && <StepsFlow currentStep={currentStep} />}
      {activeTab === "sources" && (
        <SourcesDisplay sources={agentOutput ? agentOutput.sources : []} />
      )}

      {agentOutput && (
        <>
          <MetricsDisplay metrics={agentOutput.metrics} />
          <InsightDisplay insight={agentOutput.insights} />
        </>
      )}
    </div>
  );
}

import { useState } from "react";

export default function InputPanel({ onRun, isRunning = false }) {
  const [keywords, setKeywords] = useState("");
  const [n, setN] = useState(20);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isRunning) {
      onRun({
        keywords: keywords.split(",").map((k) => k.trim()),
        n: Number(n),
      });
    }
  };

  return (
    <form
      className="row justify-content-center align-items-end mb-4"
      onSubmit={handleSubmit}
    >
      <div className="col-auto">
        <label className="form-label fw-semibold">
          Keywords (comma-separated):
        </label>
        <input
          type="text"
          className="form-control"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
        />
      </div>
      <div className="col-auto">
        <label className="form-label fw-semibold">Top N per platform:</label>
        <input
          type="number"
          className="form-control"
          value={n}
          min={1}
          max={100}
          onChange={(e) => setN(e.target.value)}
        />
      </div>
      <div className="col-auto">
        <button
          type="submit"
          className="btn btn-primary px-4"
          disabled={isRunning}
        >
          {isRunning ? (
            <>
              <span
                className="spinner-border spinner-border-sm me-2"
                role="status"
                aria-hidden="true"
              ></span>
              Running...
            </>
          ) : (
            "Run Agent"
          )}
        </button>
      </div>
    </form>
  );
}

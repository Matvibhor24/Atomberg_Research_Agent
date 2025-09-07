// src/components/Tabs.jsx
export default function Tabs({ activeTab, onChange }) {
    return (
      <div className="d-flex gap-3 mb-3">
        <button
          className={`btn ${activeTab === 'steps' ? 'btn-primary' : 'btn-outline-primary'}`}
          onClick={() => onChange('steps')}
        >
          Steps
        </button>
        <button
          className={`btn ${activeTab === 'sources' ? 'btn-primary' : 'btn-outline-primary'}`}
          onClick={() => onChange('sources')}
        >
          Sources
        </button>
      </div>
    );
  }
  
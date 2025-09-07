// src/components/SourcesDisplay.jsx
export default function SourcesDisplay({ sources }) {
  if (!sources || sources.length === 0) return null;

  // Group by platform
  const grouped = sources.reduce((acc, source) => {
    (acc[source.platform] = acc[source.platform] || []).push(source);
    return acc;
  }, {});

  return (
    <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
      {Object.entries(grouped).map(([platform, items]) => (
        <div key={platform} className="mb-3">
          <h5>{platform}</h5>
          <ul className="list-group">
            {items.map((item, idx) => (
              <li key={idx} className="list-group-item">
                <a href={item.meta.url || '#'} target="_blank" rel="noopener noreferrer">
                  {item.text.length > 80 ? item.text.slice(0, 80) + '...' : item.text}
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

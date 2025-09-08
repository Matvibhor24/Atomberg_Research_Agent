export async function runAgent({ keywords, n }) {
  const res = await fetch("https://atomberg-shareofvoice-ai-agent.onrender.com/run-agent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ keywords, n }),
  });

  if (!res.ok) {
    throw new Error(`Server error: ${res.status}`);
  }

  return await res.json();
}

export function runAgentWithProgress(
  { keywords, n },
  onProgress,
  onComplete,
  onError
) {
  const eventSource = new EventSource(
    `https://atomberg-shareofvoice-ai-agent.onrender.com/run-agent-stream`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ keywords, n }),
    }
  );

  // Note: EventSource doesn't support POST with body, so we need to use fetch with streaming
  return fetch("https://atomberg-shareofvoice-ai-agent.onrender.com/run-agent-stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ keywords, n }),
  }).then((response) => {
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    function readStream() {
      return reader.read().then(({ done, value }) => {
        if (done) {
          return;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));

              if (data.type === "progress") {
                onProgress(data);
              } else if (data.type === "complete") {
                onComplete(data);
                return; // End the stream
              } else if (data.type === "error") {
                onError(data.message);
                return; // End the stream
              }
            } catch (e) {
              console.error("Error parsing SSE data:", e);
            }
          }
        }

        return readStream();
      });
    }

    return readStream();
  });
}

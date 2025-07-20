import React, { useState, useEffect } from "react";

  const sampleQuestions = [
    "What's the average temperature in room 1?",
    "How does CO2 vary by day of the week?",
    "Show me humidity levels for the past 24 hours",
    "Which room has the highest CO2 levels?",
    "What's the temperature trend throughout the day?",
    "Compare humidity between all rooms"
  ];

const App: React.FC = () => {
  const [query, setQuery] = useState("");
  type QueryResult = { summary?: string; table?: Record<string, any> } | null;
  const [result, setResult] = useState<QueryResult>(null);
  const [loading, setLoading] = useState(false);
  // const [selectedRoom, setSelectedRoom] = useState<string>("");


  const sendQuery = async () => {
    if (!query) return;
    setLoading(true);
    setResult(null);

    const fullQuery = `In general, ${query}`;

    try {
      const response = await fetch("http://localhost:8000/v1/roomdata/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: fullQuery }),
      });
      const data = await response.json();
      const parsed = {
        ...data,
        result: JSON.parse(data.result)
      };
      // console.log(parsed)
      setResult(parsed.result);
    } catch (error) {
      setResult({ summary: "Error connecting to backend." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
    <div className="mt-4 align-items-center w-50 m-auto">
      <h1 className="text-2xl font-bold mb-4">Air Quality Data Analyzer</h1>

      <label className="block mb-2 font-semibold" htmlFor="room-select">
        Enter your Query
      </label>

      <textarea
        className="w-100 border p-2 mb-2"
        rows={4}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query..."
      />

      <button
        onClick={sendQuery}
        disabled={loading}
        className="btn btn-outline-primary"
        style={{display:'flex'}}
      >
        {loading ? "Processing..." : "Submit"}
      </button>

      <div className="mt-3 w-50">
        <h3 className="font-semibold">Sample Questions:</h3>
        <ul className="list-group-item list-group-item-action list-group-item-info">
          {sampleQuestions.map((q, i) => (
            <li
              key={i}
              className="list-group-item list-group-item-action list-group-item-light"
              onClick={() => setQuery(q)}
            >
              ❓{q}
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-5">
        {result?.summary && (
          <>
            <h3>Summary:</h3>
            <p>{result.summary}</p>
          </>
        )}

        {result?.table && Object.keys(result.table).length > 0 && (
          <>
            <h3>Table:</h3>
            <table className="table table-success table-striped-columns w-75 text-center">
              <thead>
                <tr>
                  <th>{result.table.key_label}</th>
                  <th>{result.table.value_label}</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(result.table.data).map(([key, value]) => (
                  <tr key={key} className="">
                    <td>{key}</td>
                    <td>{String(value)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </div>
    </div>
      <footer className="bg-dark text-white text-center py-5 mt-5">
        <div className="container">
          <p className="mb-0">©Vishva Isuranga. All rights reserved.</p>
        </div>
      </footer>
    </>
  );
};

export default App;

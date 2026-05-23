import { useState } from 'react'
import './QueryPanel.css'

function QueryPanel() {

  const [question, setQuestion] = useState("")
  const [sql, setSql] = useState("")
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [execTime, setExecTime] = useState(null)

  async function handleAsk() {
    if (!question.trim()) return

    setSql("")
    setResults([])
    setError("")
    setExecTime(null)
    setLoading(true)

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.detail || "Something went wrong")
        return
      }

      setSql(data.generated_sql)
      setResults(data.result)
      setExecTime(data.execution_time)

    } catch (err) {
      setError("Could not reach the server. Is your backend running?")
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") handleAsk()
  }

  return (
    <div className="query-panel">

      {/* Input area */}
      <div className="query-input-area">
        <div className="query-label">Ask anything about your data</div>
        <div className="query-row">
          <input
            className="query-input"
            type="text"
            placeholder="e.g. show customers who spent the most"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />
          <button
            className={`query-btn ${loading ? 'loading' : ''}`}
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? <span className="btn-spinner" /> : "Ask →"}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="query-error">
          ⚠ {error}
        </div>
      )}

      {/* Generated SQL */}
      {sql && (
        <div className="sql-block">
          <div className="sql-header">
            <span className="sql-label">Generated SQL</span>
            {execTime !== null && (
              <span className="exec-time">{execTime.toFixed(3)}s</span>
            )}
          </div>
          <pre className="sql-code">{sql}</pre>
        </div>
      )}

      {/* Results table */}
      {results.length > 0 && (
        <div className="results-block">
          <div className="results-header">
            <span className="results-label">Results</span>
            <span className="results-count">{results.length} rows</span>
          </div>
          <div className="table-scroll">
            <table className="results-table">
              <thead>
                <tr>
                  {Object.keys(results[0]).map(col => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((val, j) => (
                      <td key={j}>{String(val)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && !sql && (
        <div className="empty-state">
          <div className="empty-icon">◎</div>
          <p>Ask a question to query your database</p>
          <div className="suggestions">
            {[
              "show all customers",
              "highest spending customer in each city",
              "monthly revenue trends",
              "products never ordered"
            ].map(s => (
              <button
                key={s}
                className="suggestion-chip"
                onClick={() => { setQuestion(s); }}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

    </div>
  )
}

export default QueryPanel

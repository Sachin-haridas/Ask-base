import { useState, useEffect } from 'react'
import './SchemaPanel.css'

function SchemaPanel() {

  const [schema, setSchema] = useState({})
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState({})   // tracks which tables are open

  useEffect(() => {
    fetchSchema()
  }, [])

  async function fetchSchema() {
    try {
      const response = await fetch("http://localhost:8000/schema")
      const data = await response.json()
      setSchema(data.schema)

      // expand all tables by default
      const allExpanded = {}
      Object.keys(data.schema).forEach(t => allExpanded[t] = true)
      setExpanded(allExpanded)

    } catch (err) {
      console.error("Failed to fetch schema:", err)
    } finally {
      setLoading(false)
    }
  }

  function toggleTable(tableName) {
    setExpanded(prev => ({
      ...prev,
      [tableName]: !prev[tableName]
    }))
  }

  if (loading) {
    return (
      <div className="schema-loading">
        <div className="schema-spinner" />
        <p>Loading schema...</p>
      </div>
    )
  }

  return (
    <div className="schema-panel">

      <div className="schema-header">
        <span className="schema-title">Schema</span>
        <span className="schema-count">{Object.keys(schema).length} tables</span>
      </div>

      <div className="schema-tables">
        {Object.entries(schema).map(([tableName, columns]) => (
          <div key={tableName} className="schema-table">

            <button
              className="table-toggle"
              onClick={() => toggleTable(tableName)}
            >
              <span className="table-icon">▤</span>
              <span className="table-name">{tableName}</span>
              <span className={`table-arrow ${expanded[tableName] ? 'open' : ''}`}>›</span>
            </button>

            {expanded[tableName] && (
              <ul className="column-list">
                {columns.map(col => (
                  <li key={col} className="column-item">
                    <span className="col-dot" />
                    {col}
                  </li>
                ))}
              </ul>
            )}

          </div>
        ))}
      </div>

    </div>
  )
}

export default SchemaPanel

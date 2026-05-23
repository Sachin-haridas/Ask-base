import SchemaPanel from './SchemaPanel'
import QueryPanel from './QueryPanel'
import './App.css'

function App() {
  return (
    <div className="app">

      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">⬡</span>
            <span className="logo-text">Askbase</span>
          </div>
          <span className="header-sub">Natural language analytics</span>
        </div>
      </header>

      <main className="main">
        <aside className="left-panel">
          <SchemaPanel />
        </aside>
        <section className="right-panel">
          <QueryPanel />
        </section>
      </main>

    </div>
  )
}

export default App

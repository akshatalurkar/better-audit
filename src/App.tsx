import './App.css'

function App() {
  return (
    <div className="page-container">
      <main className="main-content">
        <div className="welcome-container">
          <h1>planning courses? BetterAudit it.</h1>
        </div>
        <div className="input-section">
          <div className="main-input-area">
            <input id="file-upload" type="file" hidden />
            <label htmlFor="file-upload" className="file-upload-label">
              <span>upload your audit</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-file-text"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            </label>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
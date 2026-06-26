import { useEffect, useState } from 'react';

const API_BASE = '/api';

function App() {
  const [sets, setSets] = useState([]);
  const [selectedKey, setSelectedKey] = useState('perfect');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [customNumbers, setCustomNumbers] = useState('1,2,3,5,8,13,21,34,55,89');

  useEffect(() => {
    fetch(`${API_BASE}/sets`)
      .then((res) => res.json())
      .then((data) => {
        setSets(data);
        if (data.length > 0) {
          setSelectedKey(data[0].key);
        }
      })
      .catch((err) => setError(err.message));
  }, []);

  const analyzeSet = async (key) => {
    setLoading(true);
    setError(null);
    setAnalysis(null);
    try {
      const response = await fetch(`${API_BASE}/analyze/${key}`);
      if (!response.ok) {
        throw new Error(await response.text());
      }
      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const analyzeCustom = async () => {
    setLoading(true);
    setError(null);
    setAnalysis(null);
    try {
      const numbers = customNumbers
        .split(',')
        .map((value) => parseInt(value.trim(), 10))
        .filter((value) => !Number.isNaN(value));

      const response = await fetch(`${API_BASE}/analyze/custom`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ numbers }),
      });
      if (!response.ok) {
        throw new Error(await response.text());
      }
      const data = await response.json();
      setAnalysis(data);
      setSelectedKey('custom');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header>
        <h1>MathDiscoveryAI</h1>
        <p>Explore number theory patterns, exact formulas, and conjectures.</p>
      </header>

      <section className="controls">
        <div className="control-group">
          <label htmlFor="set-selector">Choose a dataset</label>
          <select
            id="set-selector"
            value={selectedKey}
            onChange={(event) => setSelectedKey(event.target.value)}
          >
            {sets.map((set) => (
              <option key={set.key} value={set.key}>
                {set.name}
              </option>
            ))}
          </select>
          <button onClick={() => analyzeSet(selectedKey)} disabled={loading}>
            Analyze Selected Set
          </button>
        </div>

        <div className="control-group custom-sequence">
          <label htmlFor="custom-numbers">Custom numbers</label>
          <textarea
            id="custom-numbers"
            rows="3"
            value={customNumbers}
            onChange={(event) => setCustomNumbers(event.target.value)}
          />
          <button onClick={analyzeCustom} disabled={loading}>
            Analyze Custom Sequence
          </button>
        </div>
      </section>

      {loading && <div className="status">Analyzing... please wait.</div>}
      {error && <div className="status error">{error}</div>}
      {!loading && !analysis && !error && sets.length > 0 && (
        <div className="status">Select a dataset and click Analyze to begin.</div>
      )}

      {analysis && (
        <main>
          <section className="summary-card">
            <h2>{analysis.set_name}</h2>
            <p>{analysis.description || 'Analysis results from the discovery engine.'}</p>
            <div className="summary-grid">
              <div>
                <span>Numbers</span>
                <strong>{analysis.numbers.length}</strong>
              </div>
              <div>
                <span>Features</span>
                <strong>{analysis.feature_count}</strong>
              </div>
              <div>
                <span>Conjectures</span>
                <strong>{analysis.conjectures.length}</strong>
              </div>
            </div>
          </section>

          <section className="panel">
            <h3>Top Conjectures</h3>
            <div className="conjecture-grid">
              {analysis.conjectures.slice(0, 8).map((conj) => (
                <article key={conj.id} className="conjecture-card">
                  <h4>{conj.statement}</h4>
                  <div className="meta-row">
                    <span>{conj.type}</span>
                    <span>{conj.novelty || 'unknown'} novelty</span>
                  </div>
                  <div className="score-row">
                    <strong>{conj.confidence?.toFixed(1) ?? '0.0'}%</strong>
                    <span>Quality {conj.quality_score?.toFixed(1) ?? '0.0'}</span>
                  </div>
                  {conj.verification && (
                    <div className={`verification ${conj.verification.status}`}>
                      {conj.verification.status === 'verified' ? 'Verified' : 'Refuted'}
                    </div>
                  )}
                </article>
              ))}
            </div>
          </section>

          <section className="panel">
            <h3>Pattern Overview</h3>
            {Object.entries(analysis.patterns).map(([group, patterns]) => (
              <div key={group} className="pattern-group">
                <h4>{group.replace(/_/g, ' ')}</h4>
                <ul>
                  {patterns.slice(0, 5).map((pattern, index) => (
                    <li key={`${group}-${index}`}>
                      {pattern.description || pattern.statement || JSON.stringify(pattern)}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </section>
        </main>
      )}
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import LoadingState from './components/LoadingState';
import ErrorState from './components/ErrorState';
import Home from './pages/Home';
import Results from './pages/Results';
import { analyzeContent } from './services/api';

export default function App() {
  const [text, setText] = useState('');
  const [useMockData, setUseMockData] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [view, setView] = useState('input'); // 'input' | 'results'

  const handleAnalyze = async () => {
    if (!text || !text.trim()) {
      setError('Please paste a financial message or claim to analyze.');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const data = await analyzeContent(text.trim(), useMockData);
      setResult(data);
      setView('results');
    } catch (err) {
      console.error("Analysis Error:", err);
      setError(err.message || 'Failed to analyze the message. Please check your connection or server status.');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setView('input');
    setError(null);
  };

  return (
    <div className="app-container">
      <Header useMockData={useMockData} setUseMockData={setUseMockData} />

      <main className="main-content">
        {loading && <LoadingState />}

        {!loading && error && (
          <ErrorState error={error} onRetry={handleAnalyze} />
        )}

        {!loading && !error && view === 'input' && (
          <Home
            text={text}
            setText={setText}
            onAnalyze={handleAnalyze}
            loading={loading}
          />
        )}

        {!loading && !error && view === 'results' && result && (
          <Results
            result={result}
            onBack={handleBack}
            onReanalyze={handleAnalyze}
            inputText={text}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}

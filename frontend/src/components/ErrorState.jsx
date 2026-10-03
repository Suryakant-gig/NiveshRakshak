import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function ErrorState({ error, onRetry }) {
  return (
    <div className="error-card">
      <AlertTriangle size={36} color="var(--risk-high)" style={{ margin: '0 auto' }} />
      <h3 className="error-title">Analysis Failed</h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginBottom: '1.25rem' }}>
        {error || 'An unexpected error occurred while processing the financial message.'}
      </p>
      <button
        className="btn-secondary"
        onClick={onRetry}
        style={{ margin: '0 auto' }}
      >
        <RefreshCw size={14} />
        <span>Try Again</span>
      </button>
    </div>
  );
}

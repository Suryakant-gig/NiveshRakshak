import React from 'react';
import { Shield, Lock, Activity } from 'lucide-react';

export default function Header({ useMockData, setUseMockData }) {
  return (
    <header className="header-nav">
      <div className="header-inner">
        <div className="brand-wrapper">
          <div className="brand-icon">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <h1 className="brand-title">NIVESHRAKSHAK</h1>
            <div className="brand-subtitle">AI-Powered Financial Scam & Misinformation Shield</div>
          </div>
        </div>

        <div className="header-meta">
          <div className="disclaimer-badge">
            <Lock size={12} />
            <span>Investor Protection • Not Investment Advice</span>
          </div>

          <button
            className="mock-toggle-btn"
            onClick={() => setUseMockData(!useMockData)}
            title="Toggle between Mock Data and Live FastAPI Server"
          >
            <Activity size={12} style={{ display: 'inline', marginRight: '4px' }} />
            {useMockData ? 'Mode: Mock Data' : 'Mode: Live API'}
          </button>
        </div>
      </div>
    </header>
  );
}

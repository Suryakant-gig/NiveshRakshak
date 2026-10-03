import React from 'react';
import RiskGauge from './RiskGauge';
import { ShieldAlert, AlertTriangle, Info } from 'lucide-react';

export default function RiskCard({ overallRisk, scamScore, misinfoScore }) {
  const maxScore = Math.max(scamScore || 0, misinfoScore || 0);

  return (
    <div className="nr-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        <div className="section-title-sm">
          <ShieldAlert size={14} color="var(--primary-cyan)" />
          <span>Overall Risk Assessment</span>
        </div>
        <RiskGauge score={maxScore} riskLevel={overallRisk} />
      </div>

      <div style={{ marginTop: '1.5rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem' }}>
        {/* Scam Score Bar */}
        <div className="score-bar-wrapper">
          <div className="score-bar-label">
            <span>Scam Behavioral Score</span>
            <span style={{ color: scamScore >= 70 ? 'var(--risk-high)' : scamScore >= 40 ? 'var(--risk-medium)' : 'var(--risk-low)' }}>
              {scamScore} / 100
            </span>
          </div>
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{
                width: `${scamScore}%`,
                backgroundColor: scamScore >= 70 ? 'var(--risk-high)' : scamScore >= 40 ? 'var(--risk-medium)' : 'var(--risk-low)'
              }}
            />
          </div>
        </div>

        {/* Misinformation Score Bar */}
        <div className="score-bar-wrapper">
          <div className="score-bar-label">
            <span>Misinformation & Veracity Score</span>
            <span style={{ color: misinfoScore >= 70 ? 'var(--risk-high)' : misinfoScore >= 40 ? 'var(--risk-medium)' : 'var(--risk-low)' }}>
              {misinfoScore} / 100
            </span>
          </div>
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{
                width: `${misinfoScore}%`,
                backgroundColor: misinfoScore >= 70 ? 'var(--risk-high)' : misinfoScore >= 40 ? 'var(--risk-medium)' : 'var(--risk-low)'
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

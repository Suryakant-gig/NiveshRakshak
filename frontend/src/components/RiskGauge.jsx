import React from 'react';

export default function RiskGauge({ score = 0, riskLevel = "LOW" }) {
  const normalizedScore = Math.min(100, Math.max(0, score));
  // Arc calculation for SVG semi-circle gauge (radius = 70)
  const radius = 70;
  const strokeWidth = 12;
  const circumference = Math.PI * radius; // Half circle
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  let strokeColor = "#10B981"; // LOW Green
  if (riskLevel === "HIGH") {
    strokeColor = "#EF4444"; // HIGH Red
  } else if (riskLevel === "MEDIUM") {
    strokeColor = "#F59E0B"; // MEDIUM Amber
  }

  return (
    <div className="gauge-container">
      <svg className="gauge-svg" viewBox="0 0 180 110">
        {/* Background track arc */}
        <path
          d="M 20 95 A 70 70 0 0 1 160 95"
          fill="none"
          stroke="rgba(255, 255, 255, 0.08)"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
        />
        {/* Animated Score fill arc */}
        <path
          d="M 20 95 A 70 70 0 0 1 160 95"
          fill="none"
          stroke={strokeColor}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 1s ease-in-out, stroke 0.5s ease' }}
        />
      </svg>
      <div className="gauge-score-value">
        {normalizedScore}<span style={{ fontSize: '1.2rem', color: 'var(--text-muted)', fontWeight: 500 }}>/100</span>
      </div>
      <div className={`gauge-level-badge level-${riskLevel}`}>
        {riskLevel} RISK
      </div>
    </div>
  );
}

import React from 'react';
import RiskCard from '../components/RiskCard';
import RedFlags from '../components/RedFlags';
import ClaimsAnalysis from '../components/ClaimsAnalysis';
import EvidencePanel from '../components/EvidencePanel';
import ExplanationCard from '../components/ExplanationCard';
import SafeAction from '../components/SafeAction';
import { ArrowLeft, RefreshCw, FileText } from 'lucide-react';

export default function Results({ result, onBack, onReanalyze, inputText }) {
  if (!result) return null;

  return (
    <div className="results-container">
      {/* Header Controls */}
      <div className="results-header-actions">
        <button className="btn-secondary" onClick={onBack} type="button">
          <ArrowLeft size={16} />
          <span>Edit Message</span>
        </button>

        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-main)' }}>
          Analysis Results
        </h2>

        <button className="btn-secondary" onClick={onReanalyze} type="button">
          <RefreshCw size={14} />
          <span>Re-Analyze</span>
        </button>
      </div>

      {/* Input Message Preview */}
      <div className="nr-card" style={{ marginBottom: '1.5rem', background: 'rgba(255, 255, 255, 0.015)' }}>
        <div className="section-title-sm">
          <FileText size={14} color="var(--primary-cyan)" />
          <span>Analyzed Input Message</span>
        </div>
        <p style={{ fontStyle: 'italic', color: 'var(--text-muted)', fontSize: '0.88rem', whiteSpace: 'pre-wrap' }}>
          "{inputText}"
        </p>
      </div>

      {/* Top Section: Overall Risk Card */}
      <div className="results-grid-top">
        <RiskCard
          overallRisk={result.overall_risk}
          scamScore={result.scam_score}
          misinfoScore={result.misinformation_score}
        />

        <ExplanationCard explanation={result.explanation} />
      </div>

      {/* Red Flags Section */}
      <RedFlags redFlags={result.red_flags} />

      {/* Claims Analysis */}
      <ClaimsAnalysis claims={result.claims} />

      {/* Evidence Panel */}
      <EvidencePanel evidence={result.evidence} />

      {/* Safe Next Step */}
      <SafeAction safeAction={result.safe_action} />
    </div>
  );
}

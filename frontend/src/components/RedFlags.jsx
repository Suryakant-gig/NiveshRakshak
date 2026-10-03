import React, { useState } from 'react';
import { AlertTriangle, ChevronDown, ChevronUp, Zap, DollarSign, ShieldAlert, Clock, Award } from 'lucide-react';

export default function RedFlags({ redFlags = [] }) {
  const [expandedIndex, setExpandedIndex] = useState(null);

  const getFlagIcon = (type) => {
    switch (type) {
      case 'GUARANTEED_RETURN':
      case 'UNREALISTIC_RETURN':
        return <Zap size={18} color="#EF4444" />;
      case 'URGENCY':
      case 'LIMITED_TIME':
        return <Clock size={18} color="#F59E0B" />;
      case 'PAYMENT_REQUEST':
        return <DollarSign size={18} color="#EF4444" />;
      case 'FAKE_AUTHORITY':
        return <Award size={18} color="#EF4444" />;
      default:
        return <AlertTriangle size={18} color="#F59E0B" />;
    }
  };

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  if (!redFlags || redFlags.length === 0) {
    return (
      <div className="nr-card" style={{ marginBottom: '1.5rem' }}>
        <div className="section-title-sm">
          <AlertTriangle size={14} color="var(--risk-low)" />
          <span>Red Flags & Risk Indicators</span>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          No prominent behavioral scam signals detected in this message.
        </p>
      </div>
    );
  }

  return (
    <div className="nr-card" style={{ marginBottom: '1.5rem' }}>
      <div className="section-title-sm">
        <AlertTriangle size={14} color="var(--risk-high)" />
        <span>Red Flags & Scam Signals ({redFlags.length})</span>
      </div>

      <div className="red-flags-grid">
        {redFlags.map((flag, idx) => {
          const isExpanded = expandedIndex === idx;
          return (
            <div
              key={idx}
              className="red-flag-card"
              onClick={() => toggleExpand(idx)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') toggleExpand(idx); }}
            >
              <div className="red-flag-header">
                <div className="flag-title-wrap">
                  {getFlagIcon(flag.type)}
                  <span>{flag.label}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span className={`severity-pill severity-${flag.severity || 'HIGH'}`}>
                    {flag.severity}
                  </span>
                  {isExpanded ? <ChevronUp size={16} color="var(--text-muted)" /> : <ChevronDown size={16} color="var(--text-muted)" />}
                </div>
              </div>

              <div className="red-flag-desc">
                {flag.description}
              </div>

              {isExpanded && (
                <div style={{ marginTop: '0.75rem', paddingTop: '0.5rem', borderTop: '1px dashed var(--border-subtle)', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  <strong>Risk Detail:</strong> Flagged under category <code>{flag.type}</code>. This pattern is commonly observed in fraudulent solicitations to bypass rational user verification.
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

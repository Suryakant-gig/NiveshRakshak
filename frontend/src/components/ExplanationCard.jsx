import React from 'react';
import { HelpCircle, ShieldAlert } from 'lucide-react';

export default function ExplanationCard({ explanation }) {
  return (
    <div className="nr-card" style={{ marginBottom: '1.5rem' }}>
      <div className="section-title-sm">
        <HelpCircle size={14} color="var(--primary-cyan)" />
        <span>Why Was This Flagged?</span>
      </div>

      <div style={{ background: 'rgba(0, 242, 254, 0.03)', borderLeft: '3px solid var(--primary-cyan)', padding: '1rem', borderRadius: '0 var(--radius-md) var(--radius-md) 0' }}>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', lineHeight: 1.6 }}>
          {explanation || "The content contains multiple observable risk signals that require investor verification."}
        </p>
      </div>
    </div>
  );
}

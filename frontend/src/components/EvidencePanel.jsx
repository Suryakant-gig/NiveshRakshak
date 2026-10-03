import React from 'react';
import { Database, ExternalLink, Info } from 'lucide-react';

export default function EvidencePanel({ evidence = [] }) {
  return (
    <div className="nr-card" style={{ marginBottom: '1.5rem' }}>
      <div className="section-title-sm">
        <Database size={14} color="var(--primary-cyan)" />
        <span>Evidence & Authoritative Regulatory Context</span>
      </div>

      {!evidence || evidence.length === 0 ? (
        <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1rem', borderRadius: 'var(--radius-md)', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          <Info size={14} style={{ display: 'inline', marginRight: '6px' }} />
          No supporting evidence was returned for this claim.
        </div>
      ) : (
        <div>
          {evidence.map((item, idx) => {
            const relPercent = item.relevance_score ? Math.round(item.relevance_score * 100) : 85;
            return (
              <div key={idx} className="evidence-card">
                <div className="evidence-header">
                  <div className="evidence-source">{item.source || 'Official Source'}</div>
                  <div className="evidence-rel">Relevance: {relPercent}%</div>
                </div>

                <div className="evidence-snippet">
                  "{item.text}"
                </div>

                {item.url && (
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="evidence-link"
                  >
                    <span>View Official Source</span>
                    <ExternalLink size={12} />
                  </a>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

import React from 'react';
import { FileText, HelpCircle, CheckCircle2, AlertCircle, XCircle } from 'lucide-react';

export default function ClaimsAnalysis({ claims = [] }) {
  const getStatusBadge = (status) => {
    switch (status) {
      case 'SUPPORTED':
        return (
          <span className="status-badge status-SUPPORTED">
            <CheckCircle2 size={12} /> SUPPORTED
          </span>
        );
      case 'CONTRADICTED':
        return (
          <span className="status-badge status-CONTRADICTED">
            <XCircle size={12} /> CONTRADICTED
          </span>
        );
      case 'UNSUPPORTED':
        return (
          <span className="status-badge status-UNSUPPORTED">
            <AlertCircle size={12} /> UNSUPPORTED
          </span>
        );
      case 'UNVERIFIED':
      default:
        return (
          <span className="status-badge status-UNVERIFIED">
            <HelpCircle size={12} /> UNVERIFIED
          </span>
        );
    }
  };

  return (
    <div className="nr-card" style={{ marginBottom: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
        <div className="section-title-sm" style={{ marginBottom: 0 }}>
          <FileText size={14} color="var(--primary-cyan)" />
          <span>Extracted Financial Claims ({claims.length})</span>
        </div>
        <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontStyle: 'italic' }}>
          * UNVERIFIED means status requires registry proof, not that it is inherently fake.
        </div>
      </div>

      {claims.length === 0 ? (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          No explicit financial claims extracted from input text.
        </p>
      ) : (
        <div>
          {claims.map((claim) => (
            <div key={claim.id || claim.text} className="claim-item">
              <div className="claim-top">
                <div>
                  <div className="claim-text">"{claim.text}"</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: '0.2rem' }}>
                    Category: <code style={{ color: 'var(--primary-cyan)' }}>{claim.type || 'financial_claim'}</code>
                  </div>
                </div>
                <div>{getStatusBadge(claim.status)}</div>
              </div>

              {claim.reason && (
                <div className="claim-reason">
                  <strong>Verification Rationale:</strong> {claim.reason}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

import React from 'react';
import { ShieldCheck, ArrowRight } from 'lucide-react';

export default function SafeAction({ safeAction }) {
  return (
    <div className="safe-action-card">
      <div className="safe-action-header">
        <ShieldCheck size={22} color="var(--risk-low)" />
        <span>SAFE NEXT STEP</span>
      </div>

      <div className="safe-action-text">
        {safeAction || "Verify the claim through an authoritative source (such as official SEBI or RBI public portals) before taking any financial action."}
      </div>

      <div style={{ marginTop: '0.75rem', fontSize: '0.75rem', color: 'var(--text-muted)', fontStyle: 'italic', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
        <span>Investor Protection Reminder: NiveshRakshak never recommends financial products, stocks, or trading decisions.</span>
      </div>
    </div>
  );
}

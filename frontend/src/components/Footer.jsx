import React from 'react';

export default function Footer() {
  return (
    <footer className="app-footer">
      <div>
        <strong>NIVESHRAKSHAK</strong> — AI-Powered Investor Protection Shield &copy; {new Date().getFullYear()}
      </div>
      <div style={{ marginTop: '0.3rem', color: 'var(--text-dim)' }}>
        Strictly for investor education and scam signal detection. Not an investment advisory tool, trading bot, or stock predictor.
      </div>
    </footer>
  );
}

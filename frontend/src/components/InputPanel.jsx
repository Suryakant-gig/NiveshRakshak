import React from 'react';
import { DEMO_PRESETS } from '../data/mockResponse';
import AnalyzeButton from './AnalyzeButton';
import { FileText, Sparkles } from 'lucide-react';

export default function InputPanel({ text, setText, onAnalyze, loading }) {
  const maxLength = 2000;

  const handlePresetSelect = (presetText) => {
    setText(presetText);
  };

  return (
    <div className="nr-card">
      <div style={{ marginBottom: '1.25rem' }}>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-main)' }}>
          Check a Financial Message
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          Paste a financial message, investment claim, or promotional text to analyze its risk signals, claim veracity, and regulatory safety.
        </p>
      </div>

      <div style={{ position: 'relative' }}>
        <textarea
          className="nr-textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={`Example:\nInvest ₹10,000 today and get guaranteed 30% returns in 7 days.\nSEBI approved. Limited slots available. Send money now.`}
          maxLength={maxLength}
          rows={5}
        />
        <div className="counter-wrapper">
          {text.length} / {maxLength} characters
        </div>
      </div>

      <div style={{ marginTop: '1.25rem' }}>
        <div className="section-title-sm">
          <Sparkles size={14} color="var(--primary-cyan)" />
          <span>Load Demo Examples</span>
        </div>
        <div className="presets-grid">
          {DEMO_PRESETS.map((preset) => (
            <button
              key={preset.id}
              className="preset-btn"
              onClick={() => handlePresetSelect(preset.text)}
              type="button"
            >
              <div className="preset-btn-title">{preset.title}</div>
              <span className={`severity-pill severity-${preset.badgeColor === 'red' ? 'HIGH' : preset.badgeColor === 'amber' ? 'MEDIUM' : 'LOW'}`}>
                {preset.badge}
              </span>
            </button>
          ))}
        </div>
      </div>

      <div style={{ marginTop: '1rem' }}>
        <AnalyzeButton
          onAnalyze={onAnalyze}
          loading={loading}
          disabled={!text || !text.trim()}
        />
      </div>
    </div>
  );
}

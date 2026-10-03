import React from 'react';
import { Search, ShieldAlert } from 'lucide-react';

export default function AnalyzeButton({ onAnalyze, loading, disabled }) {
  return (
    <button
      className="btn-primary-cta"
      onClick={onAnalyze}
      disabled={disabled || loading}
      type="button"
    >
      {loading ? (
        <>
          <ShieldAlert className="w-5 h-5 animate-spin" />
          <span>Analyzing Message...</span>
        </>
      ) : (
        <>
          <Search className="w-5 h-5" />
          <span>Analyze Content</span>
        </>
      )}
    </button>
  );
}

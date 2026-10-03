import React from 'react';
import InputPanel from '../components/InputPanel';

export default function Home({ text, setText, onAnalyze, loading }) {
  return (
    <div>
      <InputPanel
        text={text}
        setText={setText}
        onAnalyze={onAnalyze}
        loading={loading}
      />
    </div>
  );
}

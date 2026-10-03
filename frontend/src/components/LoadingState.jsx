import React, { useState, useEffect } from 'react';
import { Shield, Sparkles } from 'lucide-react';

export default function LoadingState() {
  const steps = [
    "Analyzing message structure...",
    "Extracting financial claims...",
    "Scanning observable scam signals...",
    "Cross-referencing regulatory patterns...",
    "Calculating risk scores & generating safe guidance..."
  ];

  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 250);
    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div className="nr-card loading-box">
      <div className="spinner-ring" />
      <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-main)' }}>
        Analyzing Financial Security Risk
      </h3>
      <div className="loading-step" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
        <Sparkles size={14} color="var(--primary-cyan)" />
        <span>{steps[currentStep]}</span>
      </div>
    </div>
  );
}

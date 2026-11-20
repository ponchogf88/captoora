import React from 'react';

interface LogoProps {
  size?: number;
}

export const GeminiSparkleLogo: React.FC<LogoProps> = ({ size = 44 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none">
    <defs>
      <linearGradient id="geminiGrad" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stopColor="#4285F4" />
        <stop offset="50%" stopColor="#00F5D4" />
        <stop offset="100%" stopColor="#A855F7" />
      </linearGradient>
    </defs>
    <path
      d="M24 2C24 14.15 33.85 24 46 24C33.85 24 24 33.85 24 46C24 33.85 14.15 24 2 24C14.15 24 24 14.15 24 2Z"
      fill="url(#geminiGrad)"
    />
  </svg>
);

export const GoogleGLogo: React.FC<LogoProps> = ({ size = 40 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48">
    <path
      fill="#EA4335"
      d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
    />
    <path
      fill="#4285F4"
      d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
    />
    <path
      fill="#FBBC05"
      d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
    />
    <path
      fill="#34A853"
      d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
    />
  </svg>
);

export const ClaudeStarburstLogo: React.FC<LogoProps> = ({ size = 44 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none">
    <g stroke="#D97757" strokeWidth="4.2" strokeLinecap="round">
      <line x1="24" y1="5" x2="24" y2="43" />
      <line x1="5" y1="24" x2="43" y2="24" />
      <line x1="10.5" y1="10.5" x2="37.5" y2="37.5" />
      <line x1="37.5" y1="10.5" x2="10.5" y2="37.5" />
    </g>
    <circle cx="24" cy="24" r="5" fill="#D97757" />
  </svg>
);

export const OpenAILogo: React.FC<LogoProps> = ({ size = 40 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none">
    <circle cx="24" cy="24" r="19" stroke="#10A37F" strokeWidth="3.2" strokeDasharray="10 4" />
    <polygon
      points="24,8 37.8,16 37.8,32 24,40 10.2,32 10.2,16"
      stroke="#10A37F"
      strokeWidth="3"
      fill="#10A37F22"
    />
    <circle cx="24" cy="24" r="5" fill="#10A37F" />
  </svg>
);

export const TerminalHarnessLogo: React.FC<LogoProps> = ({ size = 40 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none">
    <rect x="4" y="8" width="40" height="32" rx="8" fill="#0F172A" stroke="#38BDF8" strokeWidth="3" />
    <path d="M14 19L21 25L14 31" stroke="#00F5D4" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round" />
    <line x1="24" y1="31" x2="34" y2="31" stroke="#38BDF8" strokeWidth="3.5" strokeLinecap="round" />
  </svg>
);

export const VisaWordmark: React.FC<LogoProps> = ({ size = 40 }) => (
  <svg width={size * 1.4} height={size * 0.7} viewBox="0 0 72 36" fill="none">
    <rect x="1" y="1" width="70" height="34" rx="8" fill="#0F172A" stroke="#38BDF8" strokeWidth="2" />
    <text
      x="36"
      y="24"
      textAnchor="middle"
      fill="#38BDF8"
      fontFamily="system-ui, sans-serif"
      fontWeight="900"
      fontStyle="italic"
      fontSize="18"
      letterSpacing="1.2"
    >
      VISA
    </text>
  </svg>
);

export const MastercardCircles: React.FC<LogoProps> = ({ size = 38 }) => (
  <svg width={size * 1.35} height={size * 0.85} viewBox="0 0 56 36" fill="none">
    <circle cx="21" cy="18" r="13" fill="#EF4444" fillOpacity="0.92" />
    <circle cx="35" cy="18" r="13" fill="#F59E0B" fillOpacity="0.88" />
  </svg>
);

export const BankShieldIcon: React.FC<LogoProps> = ({ size = 38 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none">
    <path
      d="M24 4L40 10V23C40 33.2 33 41.2 24 44C15 41.2 8 33.2 8 23V10L24 4Z"
      fill="#06191D"
      stroke="#00F5D4"
      strokeWidth="3"
    />
    <path d="M17 24L22 29L32 19" stroke="#00F5D4" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const GovLeakBadge: React.FC<LogoProps> = ({ size = 38 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none">
    <rect x="4" y="6" width="40" height="36" rx="8" fill="#180A0E" stroke="#FF3B3B" strokeWidth="2.8" />
    <path d="M24 14L33 30H15L24 14Z" stroke="#FF3B3B" strokeWidth="2.8" strokeLinejoin="round" />
    <line x1="24" y1="20" x2="24" y2="25" stroke="#FFFFFF" strokeWidth="2.6" strokeLinecap="round" />
    <circle cx="24" cy="27.8" r="1.4" fill="#FFFFFF" />
  </svg>
);

export const VoiceWaveIcon: React.FC<LogoProps> = ({ size = 38 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none">
    <rect x="4" y="4" width="40" height="40" rx="10" fill="#140A12" stroke="#FF3B3B" strokeWidth="2.6" />
    <line x1="12" y1="20" x2="12" y2="28" stroke="#00F5D4" strokeWidth="3.2" strokeLinecap="round" />
    <line x1="18" y1="14" x2="18" y2="34" stroke="#00F5D4" strokeWidth="3.2" strokeLinecap="round" />
    <line x1="24" y1="10" x2="24" y2="38" stroke="#FF3B3B" strokeWidth="3.2" strokeLinecap="round" />
    <line x1="30" y1="15" x2="30" y2="33" stroke="#FF3B3B" strokeWidth="3.2" strokeLinecap="round" />
    <line x1="36" y1="19" x2="36" y2="29" stroke="#FF3B3B" strokeWidth="3.2" strokeLinecap="round" />
  </svg>
);

export const TerminatorEyeIcon: React.FC<LogoProps> = ({ size = 38 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none">
    <rect x="4" y="8" width="40" height="32" rx="9" fill="#181C26" stroke="#FF1E2D" strokeWidth="3" />
    <circle cx="17" cy="24" r="5" fill="#FF1E2D" />
    <circle cx="31" cy="24" r="5" fill="#FF1E2D" />
    <circle cx="17" cy="24" r="2" fill="#FFFFFF" />
    <circle cx="31" cy="24" r="2" fill="#FFFFFF" />
    <line x1="10" y1="16" x2="22" y2="19" stroke="#94A3B8" strokeWidth="2.8" strokeLinecap="round" />
    <line x1="38" y1="16" x2="26" y2="19" stroke="#94A3B8" strokeWidth="2.8" strokeLinecap="round" />
  </svg>
);

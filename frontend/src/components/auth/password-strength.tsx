'use client';

interface PasswordStrengthProps {
  password: string;
}

export function PasswordStrength({ password }: PasswordStrengthProps) {
  const checks = [
    { label: 'At least 8 characters', test: password.length >= 8 },
    { label: 'Contains uppercase letter', test: /[A-Z]/.test(password) },
    { label: 'Contains lowercase letter', test: /[a-z]/.test(password) },
    { label: 'Contains number', test: /[0-9]/.test(password) },
    { label: 'Contains special character', test: /[^A-Za-z0-9]/.test(password) },
  ];

  const passed = checks.filter(c => c.test).length;
  const percentage = (passed / checks.length) * 100;

  const getStrengthColor = () => {
    if (percentage <= 20) return 'bg-error';
    if (percentage <= 40) return 'bg-error';
    if (percentage <= 60) return 'bg-accent';
    if (percentage <= 80) return 'bg-accent';
    return 'bg-success';
  };

  const getStrengthText = () => {
    if (percentage <= 20) return 'Very Weak';
    if (percentage <= 40) return 'Weak';
    if (percentage <= 60) return 'Fair';
    if (percentage <= 80) return 'Strong';
    return 'Very Strong';
  };

  if (!password) return null;

  return (
    <div className="mt-2">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-xs text-secondary-text">Password strength</span>
        <span className="text-xs font-medium text-secondary-text">{getStrengthText()}</span>
      </div>
      <div className="h-1.5 bg-border rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-300 ${getStrengthColor()}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="mt-3 grid grid-cols-1 gap-1.5">
        {checks.map((check, index) => (
          <div key={index} className="flex items-center gap-2">
            <div className={`w-4 h-4 rounded-full flex items-center justify-center transition-colors duration-200 ${
              check.test ? 'bg-success' : 'bg-border'
            }`}>
              {check.test && (
                <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              )}
            </div>
            <span className={`text-xs transition-colors duration-200 ${
              check.test ? 'text-primary' : 'text-secondary-text'
            }`}>
              {check.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

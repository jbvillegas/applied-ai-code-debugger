import React from 'react';

export default function LoadingIndicator({ message = 'Processing...' }) {
  return (
    <div className="flex items-center gap-2 p-4">
      <svg className="animate-spin h-5 w-5 text-blue-500" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
      </svg>
      <span className="text-sm text-neutral-500 dark:text-neutral-300">{message}</span>
    </div>
  );
}

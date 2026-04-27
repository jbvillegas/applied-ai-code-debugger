import React from 'react';

// Placeholder for execution line highlight (to be integrated with Monaco)
export default function ExecutionLineHighlight({ line }) {
  if (typeof line !== 'number') return null;
  return (
    <div
      className="absolute left-0 w-full bg-yellow-100 dark:bg-yellow-900 opacity-60 pointer-events-none"
      style={{ top: `${line * 20}px`, height: '20px' }}
    />
  );
}

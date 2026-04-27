import React from 'react';

// Placeholder for inline error highlighting (to be integrated with Monaco)
export default function InlineErrorMarkers({ errors }) {
  // errors: [{ line: number, message: string }]
  if (!errors || errors.length === 0) return null;
  return (
    <div className="absolute left-0 top-0 w-full h-full pointer-events-none">
      {errors.map((err, idx) => (
        <div
          key={idx}
          className="absolute left-0 px-2 py-1 bg-red-100 text-red-700 text-xs rounded shadow"
          style={{ top: `${err.line * 20}px` }}
        >
          {err.message}
        </div>
      ))}
    </div>
  );
}

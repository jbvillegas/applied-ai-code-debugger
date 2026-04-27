import React from 'react';

export default function WatchExpressions() {
  return (
    <div className="p-4 border-t border-neutral-200 dark:border-neutral-800">
      <div className="font-semibold text-sm mb-2">Watch Expressions</div>
      <div className="space-y-1 text-xs">
        {/* Example watch expressions */}
        <div className="flex items-center justify-between px-2 py-1 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">
          <span>len(data)</span>
          <span className="text-blue-600">5</span>
        </div>
      </div>
    </div>
  );
}

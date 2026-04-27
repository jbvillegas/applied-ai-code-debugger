import React from 'react';

export default function TopBar() {
  return (
    <header className="flex items-center justify-between px-6 py-3 bg-white dark:bg-neutral-900 shadow-sm border-b border-neutral-200 dark:border-neutral-800">
      <div className="flex items-center gap-3">
        <span className="font-bold text-lg tracking-tight">AI Code Debugger</span>
        <span className="ml-2 px-2 py-0.5 rounded bg-green-100 text-green-700 text-xs dark:bg-green-900 dark:text-green-200">● Debugging</span>
      </div>
      <div className="flex items-center gap-4">
        <button title="Toggle dark mode" className="p-2 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">
          {/* Icon placeholder */}
          <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1111.21 3a7 7 0 109.79 9.79z"></path></svg>
        </button>
        <button title="Settings" className="p-2 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">
          {/* Icon placeholder */}
          <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 01-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09a1.65 1.65 0 00-1-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09a1.65 1.65 0 001.51-1 1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06a1.65 1.65 0 001.82.33h.09A1.65 1.65 0 008.91 3.09V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51h.09a1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82v.09a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
        </button>
      </div>
    </header>
  );
}

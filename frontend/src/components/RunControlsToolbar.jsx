import React from 'react';

export default function RunControlsToolbar() {
  return (
    <div className="flex gap-2 items-center p-3 bg-white dark:bg-neutral-900 rounded-lg shadow-sm mx-4 mt-4 mb-2">
      <button title="Run (F5)" className="p-2 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">
        {/* Play Icon */}
        <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      </button>
      <button title="Step Over (F10)" className="p-2 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">
        {/* Step Over Icon */}
        <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></svg>
      </button>
      <button title="Step Into (F11)" className="p-2 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">
        {/* Step Into Icon */}
        <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><polyline points="8 6 12 2 16 6"/><line x1="12" y1="2" x2="12" y2="22"/></svg>
      </button>
      <button title="Step Out (Shift+F11)" className="p-2 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">
        {/* Step Out Icon */}
        <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><polyline points="16 18 12 22 8 18"/><line x1="12" y1="2" x2="12" y2="22"/></svg>
      </button>
      <button title="Stop (Shift+F5)" className="p-2 rounded hover:bg-red-100 dark:hover:bg-red-900 transition">
        {/* Stop Icon */}
        <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
      </button>
    </div>
  );
}

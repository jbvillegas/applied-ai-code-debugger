import React from 'react';

export default function SidebarLeft() {
  return (
    <aside className="w-56 min-w-[180px] max-w-xs bg-white dark:bg-neutral-900 border-r border-neutral-200 dark:border-neutral-800 flex flex-col">
      {/* File Explorer */}
      <div className="p-4 border-b border-neutral-200 dark:border-neutral-800">
        <div className="font-semibold text-sm mb-2">Files</div>
        <div className="space-y-1">
          {/* Example file list */}
          <button className="block w-full text-left px-2 py-1 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">src/main.py</button>
          <button className="block w-full text-left px-2 py-1 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">src/agent.py</button>
        </div>
      </div>
      {/* Breakpoints Panel */}
      <div className="p-4 flex-1 overflow-auto">
        <div className="font-semibold text-sm mb-2">Breakpoints</div>
        <div className="space-y-1">
          {/* Example breakpoints */}
          <div className="flex items-center justify-between px-2 py-1 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">
            <span>main.py:12</span>
            <button title="Remove" className="p-1 hover:text-red-500 transition">
              <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}

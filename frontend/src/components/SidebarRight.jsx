import React from 'react';
import WatchExpressions from './WatchExpressions';

export default function SidebarRight() {
  return (
    <aside className="w-72 min-w-[200px] max-w-md bg-white dark:bg-neutral-900 border-l border-neutral-200 dark:border-neutral-800 flex flex-col">
      {/* Variables Panel */}
      <div className="p-4 border-b border-neutral-200 dark:border-neutral-800">
        <div className="font-semibold text-sm mb-2">Variables</div>
        <div className="text-xs">
          {/* Example variable tree */}
          <div className="mb-1">
            <span className="font-mono">x</span>: <span className="text-blue-600">42</span>
          </div>
          <div className="mb-1">
            <span className="font-mono">user</span>: &#123; <span className="text-green-700">name</span>: "Alice" &#125;
          </div>
        </div>
      </div>
      {/* Call Stack Panel */}
      <div className="p-4 flex-1 overflow-auto">
        <div className="font-semibold text-sm mb-2">Call Stack</div>
        <div className="space-y-1 text-xs">
          {/* Example call stack */}
          <button className="block w-full text-left px-2 py-1 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">main()</button>
          <button className="block w-full text-left px-2 py-1 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition">run_agent()</button>
        </div>
      </div>
      <WatchExpressions />
    </aside>
  );
}

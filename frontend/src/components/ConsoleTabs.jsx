import React, { useState } from 'react';

const tabs = [
  { name: 'Output', color: 'text-green-600' },
  { name: 'Errors', color: 'text-red-500' },
  { name: 'Debug Console', color: 'text-blue-500' },
];

export default function ConsoleTabs({ error, output, log }) {
  const [active, setActive] = useState(0);
  return (
    <div className="flex flex-col h-full">
      <div className="flex gap-2 px-4 pt-2">
        {tabs.map((tab, idx) => (
          <button
            key={tab.name}
            className={`px-3 py-1 rounded-t text-sm font-medium ${active === idx ? 'bg-neutral-100 dark:bg-neutral-800' : 'hover:bg-neutral-100 dark:hover:bg-neutral-800 transition'}`}
            onClick={() => setActive(idx)}
          >
            {tab.name}
          </button>
        ))}
      </div>
      <div className="flex-1 overflow-auto px-4 pb-2 text-xs font-mono text-neutral-800 dark:text-neutral-100">
        {/* Output Tab */}
        {active === 0 && <div className="text-green-600">[stdout] {output || 'Program started...'}</div>}
        {/* Errors Tab */}
        {active === 1 && (
          <div className="text-red-500">
            [stderr] {error || 'No error'}
            {log && log.length > 0 && (
              <>
                <br />
                <b>Debug Log:</b>
                <pre className="whitespace-pre-wrap">{JSON.stringify(log, null, 2)}</pre>
              </>
            )}
          </div>
        )}
        {/* Debug Console Tab */}
        {active === 2 && <div className="text-blue-500">[system] Debugger attached</div>}
      </div>
    </div>
  );
}

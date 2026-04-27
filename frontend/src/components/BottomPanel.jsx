import React from 'react';
import ConsoleTabs from './ConsoleTabs';

export default function BottomPanel({ error, output, log }) {
  return (
    <div className="w-full bg-white dark:bg-neutral-900 border-t border-neutral-200 dark:border-neutral-800 shadow-sm min-h-[120px] max-h-72 flex flex-col">
      <ConsoleTabs error={error} output={output} log={log} />
    </div>
  );
}

import React from 'react';

export default function Breadcrumbs({ path = ["src", "main.py"] }) {
  return (
    <nav className="flex items-center gap-1 px-4 py-2 text-xs text-neutral-500 dark:text-neutral-400">
      {path.map((segment, idx) => (
        <span key={idx} className="flex items-center">
          {idx > 0 && <span className="mx-1">/</span>}
          <button className="hover:underline focus:underline focus:outline-none">{segment}</button>
        </span>
      ))}
    </nav>
  );
}

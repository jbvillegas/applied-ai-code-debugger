
import React from 'react';
import App from './App';
import { createRoot } from 'react-dom/client';
import './index.css';
// Patch ResizeObserver to avoid loop errors
const patchResizeObserver = () => {
  if (typeof window !== 'undefined' && window.ResizeObserver) {
    const RO = window.ResizeObserver;
    window.ResizeObserver = class ResizeObserver extends RO {
      constructor(callback) {
        callback = ((cb) => (entries, observer) => {
          requestAnimationFrame(() => cb(entries, observer));
        })(callback);
        super(callback);
      }
    };
  }
};
patchResizeObserver();

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

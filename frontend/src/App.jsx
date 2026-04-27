
import React, { useState } from 'react';
import TopBar from './components/TopBar';
import MainLayout from './components/MainLayout';
import BottomPanel from './components/BottomPanel';
import './index.css';


class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    // You can log errorInfo here if needed
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-red-50 text-red-800">
          <div className="bg-white p-8 rounded shadow max-w-lg w-full">
            <h2 className="text-xl font-bold mb-2">Something went wrong</h2>
            <pre className="text-xs whitespace-pre-wrap">{this.state.error && this.state.error.toString()}</pre>
            <button className="mt-4 px-4 py-2 bg-red-600 text-white rounded" onClick={() => window.location.reload()}>Reload</button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [error, setError] = useState("");
  const [output, setOutput] = useState("");
  const [log, setLog] = useState([]);
  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-neutral-50 dark:bg-neutral-900 font-sans flex flex-col">
        <TopBar />
        <MainLayout setError={setError} setOutput={setOutput} setLog={setLog} output={output} />
        <BottomPanel error={error} output={output} log={log} />
      </div>
    </ErrorBoundary>
  );
}

export default App;

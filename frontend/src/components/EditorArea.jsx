import React, { useRef, useState } from 'react';
import RunControlsToolbar from './RunControlsToolbar';
import Breadcrumbs from './Breadcrumbs';
import { Editor } from '@monaco-editor/react';


const initialCode = `def hello():\n    print(\"Hello, world!\")\n\nhello()\n`;



export default function EditorArea({ setError, setOutput, setLog, output }) {
  const [code, setCode] = useState(initialCode);
  const [loading, setLoading] = useState(false);
  const editorRef = useRef(null);


  // Monaco options
  const options = {
    selectOnLineNumbers: true,
    roundedSelection: false,
    readOnly: false,
    fontSize: 14,
    minimap: { enabled: false },
    lineNumbers: 'on',
    scrollBeyondLastLine: false,
    theme: 'vs',
    glyphMargin: true,
    wordWrap: 'on',
  };

  // Run code by calling backend
  async function handleRun() {
    setLoading(true);
    setOutput("");
    setError("");
    setLog([]);
    try {
      const response = await fetch("http://localhost:5000/debug", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = await response.json();
      setOutput(data.final_code || "");
      setError(data.error || "");
      setLog(data.log || []);
    } catch (err) {
      setOutput("");
      setError("Error: " + err.message);
      setLog([]);
    } finally {
      setLoading(false);
    }
  }

  // Editor did mount handler
  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
    // Optionally, set up breakpoints, errors, and execution line here if needed in the future.
  }

  // Helper: Set breakpoints
  function setBreakpoints(editor, monaco, breakpoints) {
    const decorations = breakpoints.map(line => ({
      range: new monaco.Range(line, 1, line, 1),
      options: {
        isWholeLine: true,
        glyphMarginClassName: 'bg-red-500 rounded-full w-3 h-3 block',
        glyphMarginHoverMessage: { value: 'Breakpoint' },
      },
    }));
    editor.deltaDecorations([], decorations);
  }

  // Helper: Set error squiggles
  function setErrorSquiggles(editor, monaco, errors) {
    const model = editor.getModel();
    if (!model) return;
    const markers = errors.map(err => ({
      startLineNumber: err.line,
      startColumn: 1,
      endLineNumber: err.line,
      endColumn: 100,
      message: err.message,
      severity: monaco.MarkerSeverity.Error,
    }));
    monaco.editor.setModelMarkers(model, 'owner', markers);
  }

  // Helper: Highlight execution line
  function setExecutionLine(editor, monaco, line) {
    if (!line) return;
    editor.deltaDecorations([], [
      {
        range: new monaco.Range(line, 1, line, 1),
        options: {
          isWholeLine: true,
          className: 'bg-yellow-100 dark:bg-yellow-900',
        },
      },
    ]);
  }

  return (
    <main className="flex-1 flex flex-col min-w-0">
      <Breadcrumbs />
      {/* RunControlsToolbar with Run button wired up */}
      <div className="flex gap-2 items-center p-3 bg-white dark:bg-neutral-900 rounded-lg shadow-sm mx-4 mt-4 mb-2">
        <button
          title="Run (F5)"
          className="p-2 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 transition"
          onClick={handleRun}
          disabled={loading}
        >
          ▶ Run
        </button>
        {loading && <span className="ml-2 text-xs text-gray-500">Running...</span>}
      </div>
      <div className="flex-1 bg-neutral-100 dark:bg-neutral-800 rounded-lg m-4 shadow-inner relative overflow-hidden">
        <Editor
          height="100%"
          defaultLanguage="python"
          value={code}
          onChange={setCode}
          options={options}
          onMount={handleEditorDidMount}
        />
      </div>
      {/* Output panel */}
      <div className="mx-4 mb-4 p-3 bg-white dark:bg-neutral-900 rounded shadow text-xs font-mono min-h-[40px]">
        <b>Output:</b>
        <pre className="whitespace-pre-wrap">{output}</pre>
      </div>
    </main>
  );
}

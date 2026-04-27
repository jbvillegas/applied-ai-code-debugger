import React from 'react';
import SidebarLeft from './SidebarLeft';
import EditorArea from './EditorArea';
import SidebarRight from './SidebarRight';

export default function MainLayout({ setError, setOutput, setLog, output }) {
  return (
    <div className="flex flex-1 min-h-0">
      <SidebarLeft />
      <EditorArea setError={setError} setOutput={setOutput} setLog={setLog} output={output} />
      <SidebarRight />
    </div>
  );
}

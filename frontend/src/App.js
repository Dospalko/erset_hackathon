import React, { useEffect, useState } from 'react';

function App() {
  const [backendResponse, setBackendResponse] = useState('');

  useEffect(() => {
    fetch('/test')
      .then(response => response.json())
      .then(data => setBackendResponse(data.message))
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>Response from backend: {backendResponse}</p>
      </header>
    </div>
  );
}

export default App;

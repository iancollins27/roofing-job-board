import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Optional: Your CSS file
import App from './app'; // Ensure this matches the correct path to your App component
import ReactGA from 'react-ga';

// Initialize Google Analytics
ReactGA.initialize(process.env.GOOGLE_ANALYTICS_ID);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
import React from 'react';
import './index.css';
import App from './App';
import { AuthProvider } from './AuthContext';
import { BrowserRouter as Router } from 'react-router-dom';
import ReactDOM from 'react-dom';

ReactDOM.render(
  <Router>
    <AuthProvider>
      <App />
    </AuthProvider>
  </Router>,
  document.getElementById('root')
);


import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Login.css';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const ec2_ip = process.env.REACT_APP_BACKEND_IP;
  const apiUrl = `http://${ec2_ip}:7000`;
  
  console.log("apiUrl: ",apiUrl);
  const handleLogin = (event) => {
    event.preventDefault();
    (async () => {
    const loginData = {
      "Email" : email,
      "Password" : password
    };

    try {
      const response = await fetch(`${apiUrl}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });
  
      if (response.ok) {
          navigate('/create_capsule');
          alert('Login successful! Please check your email and confirm the subscription.');
      } else {
        console.error('Login failed. Invalid credentials');
        alert('Login failed. Invalid credentials!');
      }
    } catch (error) {
      console.error('Error occurred during login:', error);
    }
  
    // Clear the form fields after login
    setEmail('');
    setPassword('');
  })();
};

  return (
    <div className="login-container">
    <div className="login-form-container">
      <h2 className="login-form-title">Login</h2>
      <form onSubmit={handleLogin} className="login-form">

        <input
          type="email"
          name="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit"><b>Sign In</b></button>
        <div style={{ textAlign: 'center',  marginTop: '20px'  }}>
        <Link to="/register">Haven't registered yet? Register</Link>
        </div>
      </form>
    </div>
  </div>
  );
};

export default LoginForm;
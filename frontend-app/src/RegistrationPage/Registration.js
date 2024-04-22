import React, { useState } from 'react';
import { useNavigate, Link  } from 'react-router-dom';
import './Registration.css';

const RegistrationForm = () => {
  const [Name, setName] = useState('');
  const [Password, setPassword] = useState('');
  const [Email, setEmail] = useState('');
  const navigate = useNavigate();

  const backendIp = process.env.REACT_APP_BACKEND_IP;
  const apiUrl = `http://${backendIp}:7000`;
  

  const handleRegistration = async (event) => {
    event.preventDefault();

    const registrationData = {
      "Name": Name,
      "Password" : Password,
      "Email" : Email
    };

    try {
      const response = await fetch(`${apiUrl}/register`, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData),
      });
      console.log(registrationData)
      if (response.ok) {
        // Registration successful, handle the response accordingly
        console.log('Registration successful!');
        setName('');
        setPassword('');
        setEmail('');

        alert('Registration successful!');
        navigate('/login'); 
      }
      else if (response.status === 409) {
        // Email already exists, handle the response
        console.error('Email already exists.');
        alert('Email already exists. Please choose a different email.');
      }  
      else {
        // Registration failed, handle the error response
        console.error('Registration failed.');
        // setRegistrationStatus('error');
        alert('Registration failed. Please try again.');
      }
    } catch (error) {
      console.error('Error occurred during registration:', error);
    //   setRegistrationStatus('error');
    alert('Error occurred during registration. Please try again.');
    }
    
  };

  return (
    <div className="registration-container">
    <div className="registration-form-container">
      <h2 className="registration-form-title">Registration Form</h2>
      <form onSubmit={handleRegistration} className="registration-form">

      <input
          type="text"
          name="name"
          placeholder="Enter your name"
          value={Name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Enter your email"
          value={Email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Enter your password"
          value={Password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit"><b>Register</b></button>
        <div style={{ textAlign: 'center',  marginTop: '20px'  }}>
         <Link to="/login">Already registered ? Login</Link>
        </div>
    
      </form>
    </div>
  </div>
  );
};

export default RegistrationForm;
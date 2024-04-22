import React, { useState } from 'react';
import './Capsule.css';

const CreateCapsulePage = () => {
  const [email, setEmail] = useState('');
  const [deliveryDateTime, setDeliveryDateTime] = useState('');
  const [textContent, setTextContent] = useState('');
  const [imageFile, setImageFile] = useState(null);

  const ec2_ip = process.env.REACT_APP_BACKEND_IP;
  const apiUrl = `http://${ec2_ip}:7000`;

  const handleCreateCapsule = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('email', email);
    formData.append('deliveryDate', deliveryDateTime);
    formData.append('textContent', textContent);
    formData.append('image', imageFile);

    const response = await fetch(`${apiUrl}/create_capsule`, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();

    if (response.ok) {
      window.alert('Capsule created successfully. Anticipate for its delivery.');
      setEmail('');
      setDeliveryDateTime('');
      setTextContent('');
      setImageFile(null);
    } else {
      console.error('Error occurred during capsule creation:', data.message);
    }
  };

  return (
    <div className="capsule-container">
      <div className="capsule-form-container">
        <h2 className="capsule-form-title">Create Your Soul Capsule</h2>
        <hr className="line"/>
        <form onSubmit={handleCreateCapsule} className="capsule-form">
        <div className="input-group">
            <div className="label-container">
              <label><b>Email:</b></label>
            </div>
            <div className="input-container">
              <input
               type="email"
               name="email"
               placeholder="Re-confirm your email"
               value={email}
               onChange={(e) => setEmail(e.target.value)}
               required
              />
            </div>
          </div>
          <div className="input-group">
            <div className="label-container">
              <label><b>Delivery Date & Time:</b></label>
            </div>
            <div className="input-container">
              <input
                type="datetime-local"
                value={deliveryDateTime}
                onChange={(e) => setDeliveryDateTime(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="input-group">
            <div className="label-container">
              <label><b>Personalized Message:</b></label>
            </div>
            <div className="input-container">
              <textarea
                rows="5"
                placeholder="Enter your personalized message here..."
                value={textContent}
                onChange={(e) => setTextContent(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="input-group">
            <div className="label-container">
              <label><b>Motivational Quote:</b></label>
            </div>
            <div className="input-container">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setImageFile(e.target.files[0])}
                required
              />
            </div>
          </div>
          <button type="submit"><b>Create Capsule</b></button>
        </form>
      </div>
    </div>
  );
};

export default CreateCapsulePage;

import React from 'react';

const LoginComponent = () => {
  const backgroundImage = "url('yip.jpg')"; // Replace with your image path

  // Function to handle login button click
  const handleLogin = () => {
    // Redirect to your Flask backend's /login route to initiate OAuth
    window.location.href = 'http://127.0.0.1:5000//login';  // Replace with the actual Flask backend URL
  };

  return (
    <div style={{
      position: 'relative',
      width: '100vw',
      height: '100vh',
      backgroundImage: backgroundImage,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }}>
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '450px',
        height: '350px',
        background: 'rgba(255, 255, 255, 0.5)',
        borderRadius: '15px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}>
        <button
          onClick={handleLogin}  // Trigger the login on button click
          style={{
            backgroundColor: 'white',
            border: '1px solid lightgray',
            padding: '20px 30px',
            fontSize: '20px',
            borderRadius: '10px',
            cursor: 'pointer',
          }}
        >
          Login with Google
        </button>
      </div>
    </div>
  );
};

export default LoginComponent;



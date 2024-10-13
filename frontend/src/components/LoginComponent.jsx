import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginComponent = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const backgroundImage = "url('yip.jpg')"

  const handleLogin = async () => {
    try {
      // Call /login endpoint to initiate Google OAuth login
      const response = await fetch('/login');
      if (response.ok) {
        // Redirect to Google OAuth page
        window.location.href = '/login';
      } else {
        setError('Failed to initiate login');
      }
    } catch (error) {
      setError(error.message);
    }
  };

  useEffect(() => {
    // After login, Google redirects back to /callback
    // Then, we redirect to /list_files and finally to HomepageComponent
    if (window.location.pathname === '/callback') {
      fetch('/list_files')
        .then((response) => response.json())
        .then((data) => {
          // Redirect to HomepageComponent
          navigate('/HeritagePage', { replace: true, state: { files: data } });
        })
        .catch((error) => setError(error.message));
    }
  }, []);

  return (
    <div
      style={{
        position: "relative",
        width: "100vw",
        height: "100vh",
        backgroundImage: backgroundImage,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: "450px",
          height: "350px",
          background: "rgba(255, 255, 255, 0.5)",
          borderRadius: "15px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <button
          onClick={handleLogin} // Trigger the login on button click
          style={{
            backgroundColor: "white",
            border: "1px solid lightgray",
            padding: "20px 30px",
            fontSize: "20px",
            borderRadius: "10px",
            cursor: "pointer",
          }}
        >
          Login with Google
        </button>
      </div>
    </div>
  );
};

export default LoginComponent;

import React from 'react';

import { useNavigate } from 'react-router-dom';  // Import useNavigate


  

const HeritageSquareComponent = () => {
    const navigate = useNavigate();  // Initialize navigate hook

  function handleSearchClick() {
    navigate('/heritage-page');  // Navigate to the heritage-square page
  };
  return (
    <div style={{
      backgroundImage: "url('yip.jpg')", // Add the path to the house image here
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      width: '100vw',
      height: '100vh',
      position: 'relative',
    }}>
      {/* Transparent card section */}
      <div style={{
        backgroundColor: 'rgba(255, 255, 255, 0.7)',  // Transparent white background
        width: '350px',
        height: '430px',
        borderRadius: '20px',
        padding: 'absolute',
        position: 'absolute',
        top: '15%',
        right: '5%',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
      }}>
        {/* Content inside the card */}
      </div>

      {/* Search Section */}
      <div style={{
        position: 'absolute',
        right: '4%',
        top: '90%',
        display: 'flex',
        alignItems: 'center',
        backgroundColor: '#fff',
        borderRadius: '30px',
        padding: '10px 20px',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
        width: '25%',
      }}>
        <input 
          type="text" 
          placeholder="Search files..." 
          style={{
            flex: 1,
            border: 'none',
            outline: 'none',
            fontSize: '16px',
            padding: '10px 20px',
            borderRadius: '30px 0 0 30px',
          }} 
        />
       
        <button onClick={handleSearchClick}>🔍</button>
     
      </div>
    </div>
    
  );
 
};

export default HeritageSquareComponent;

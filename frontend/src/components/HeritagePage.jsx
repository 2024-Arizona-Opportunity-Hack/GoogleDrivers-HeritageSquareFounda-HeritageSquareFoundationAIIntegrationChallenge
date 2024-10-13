import React from 'react';

const HeritagePage = () => {
  return (
    <div style={{
      backgroundImage: "url('yip.jpg')", // Add your background image path here
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      width: '100vw',
      height: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      position: 'relative',
    }}>
      {/* Card Section */}
      <div style={{
        backgroundColor: 'rgba(255, 255, 255, 0.7)',  // Light pink background for the card
        width: '350px',
        height: '430px',
        borderRadius: '20px',
        padding: 'absolute',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
        position: 'absolute',
        top: '15%',  // Adjust to position the card as needed
        right: '5%',
      }}>
        <div style={{ fontSize: '16px', marginBottom: '20px', color: '#333' }}>
          Suggest the locations for the files
        </div>
        <div style={{ width: '80%', display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div style={{ backgroundColor: '#baddfa', height: '40px', borderRadius: '10px' }}>
            <text>1.</text>
          </div>
          <div style={{ backgroundColor: '#baddfa', height: '40px', borderRadius: '10px' }}></div>
          <div style={{ backgroundColor: '#baddfa', height: '40px', borderRadius: '10px' }}></div>
        </div>
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
          placeholder="The files you are searching for?" 
          style={{
            flex: 1,
            border: 'none',
            outline: 'none',
            fontSize: '16px',
            padding: '10px 20px',
            borderRadius: '30px 0 0 30px'
          }} 
        />
        <button style={{
          backgroundColor: '#333', 
          color: '#fff',
          padding: '10px 20px',
          borderRadius: '0 30px 30px 0',
          border: 'none',
          cursor: 'pointer',
        }}>
          🔍
        </button>
      </div>
    </div>
  );
};

export default HeritagePage;

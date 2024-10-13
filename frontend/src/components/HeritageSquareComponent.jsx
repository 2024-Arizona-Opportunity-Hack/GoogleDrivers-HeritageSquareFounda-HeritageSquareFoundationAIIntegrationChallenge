import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const HeritageSquareComponent = () => {
  const navigate = useNavigate(); // Initialize navigate hook
  const [searchTerm, setSearchTerm] = useState(''); // State for search input
  const [filteredItems, setFilteredItems] = useState([]); // State for filtered items
  const [error, setError] = useState(''); // State for error messages

  async function handleSearchClick() { // Mark as async function to use await
    console.log(`Searching for: ${searchTerm}`); // Logs the search term

    try {
      // Make the API call to the Flask endpoint
      const response = await fetch(`http://localhost:5000/queries?category=${encodeURIComponent(searchTerm)}`);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const results = await response.json();
      setFilteredItems(results); // Update state with the results from the API

      // Optionally navigate to a different page if needed
      // navigate('/heritage-square'); // Uncomment to navigate after search

    } catch (err) {
      console.error(err);
      setError('Failed to fetch results. Please try again later.');
    }
  }

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
        {/* Content inside the card can be added here */}
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
          value={searchTerm} // Control the input value
          onChange={(e) => setSearchTerm(e.target.value)} // Update searchTerm on input change
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

      {error && <div style={{ color: 'red', position: 'absolute', top: '80%', right: '5%' }}>{error}</div>} {/* Show error message if any */}

      <ul style={{ position: 'absolute', top: '25%', right: '5%', listStyleType: 'none' }}>
        {filteredItems.map(item => (
          <li key={item.id}>{item.name}</li> // Display filtered items
        ))}
      </ul>
    </div>
  );
};

export default HeritageSquareComponent;

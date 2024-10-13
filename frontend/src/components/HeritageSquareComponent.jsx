import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const HeritageSquareComponent = () => {
  // const [files, setFiles] = useState([]); // State to hold file data
  // const [searchQuery, setSearchQuery] = useState(''); // State for search input
  // const navigate = useNavigate(); // Initialize navigate hook

  // Fetch the files from the Flask server when the component mounts
  // useEffect(() => {
  //   const fetchFiles = async () => {
  //     try {
  //       const response = await fetch('http://localhost:5000/api/queries(searchQuery)'); // Adjust the URL as needed
  //       if (!response.ok) {
  //         throw new Error('Network response was not ok');
  //       }
  //       const data = await response.json();
  //       setFiles(data); // Store the fetched files in the state
  //     } catch (error) {
  //       console.error('There was a problem with the fetch operation:', error);
  //     }
  //   };

  //   fetchFiles(); // Call the fetch function
  // }, []); // Empty dependency array means this effect runs once on mount
  const [files, setFiles] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState(null);

  const queries = async (searchQuery) => {
    try {
      const response = await fetch(`http://localhost:5000/queries?category=${searchQuery}`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const fetchFiles = async () => {
      const data = await queries(searchQuery);
      setFiles(data);
    };

    fetchFiles();
  }, [searchQuery]);
  // Function to handle search input change
  const handleSearchInputChange = (event) => {
    setSearchQuery(event.target.value); // Update search query state
  };


  // Filter files based on the search query
  // const filteredFiles = files.filter(file =>
  //   file.filename.toLowerCase().includes(searchQuery.toLowerCase())
  // );

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
        backgroundColor: 'rgba(255, 255, 255, 0.7)', // Transparent white background
        width: '350px',
        height: '430px',
        borderRadius: '20px',
        position: 'absolute',
        top: '15%',
        right: '5%',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
      }}>
        {/* Content inside the card */}
        <h2>Files</h2>
        <div>
          {/* Search Section */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            backgroundColor: '#fff',
            borderRadius: '30px',
            padding: '10px 20px',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
            width: '100%',
            marginBottom: '20px'
          }}>
            <input
              type="text"
              placeholder="Search files..."
              value={searchQuery}
              onChange={handleSearchInputChange}
              style={{
                flex: 1,
                border: 'none',
                outline: 'none',
                fontSize: '16px',
                padding: '10px 20px',
                borderRadius: '30px 0 0 30px',
              }}
            />
          </div>
        </div>

        {/* Display the filtered files as hyperlinks */}
        {/* <ul style={{ listStyleType: 'none', padding: 0 }}>
          {filteredFiles.map((file, index) => (
            <li key={index}>
              <a href={file.file_url} target="_blank" rel="noopener noreferrer">
                {file.filename}
              </a>
            </li>
          ))}
        </ul> */}
      </div>
    </div>
  );
};

export default HeritageSquareComponent;

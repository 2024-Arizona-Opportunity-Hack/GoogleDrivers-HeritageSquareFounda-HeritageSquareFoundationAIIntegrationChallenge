import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import HeritagePage from './components/HeritagePage'; // Import your component
import HeritageSquareComponent from './components/HeritageSquareComponent'; // Import the other component
import LoginComponent from './components/LoginComponent';
const App = () => {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Navigate to="/Login" />} /> 
        <Route path="/Login" element={<LoginComponent/>}/>
        <Route path="/heritage-page" element={<HeritagePage />} />
        <Route path="/heritage-square" element={<HeritageSquareComponent />} />
      </Routes>
    </Router>
  );
};

export default App;

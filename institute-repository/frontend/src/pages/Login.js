import React from 'react';
import { Link } from 'react-router-dom';
import './Login.css';
import facultyImage from './Images/Faculty.jpeg';
import Student from './Images/Student.jpeg';
import Staff from './Images/Staff.jpeg';

function Home() {
  function initiateOAuthFlow() {
  // Replace with your OAuth 2.0 provider's authorization URL
    const authorizationUrl = 'https://oauth.iitd.ac.in/authorize.php?response_type=code&client_id=YmA3yo921mEHImVWI67rSRwXTOkvMaG4&state=xyz';
  // Open the authorization URL in a new window or pop-up
    window.open(authorizationUrl, '_blank');
  }
  return (
    <div className="login-container">
      <h1 className="project-repo-heading">The Project Repo</h1>
      <div className="login-boxes">
        <div className="login-box faculty-box">
          <h2>Faculty Login</h2>
          <div class="pic_box">
          <img src={facultyImage} alt="Faculty" /></div>
          <Link to="/faculty-login" className="login-button">LOGIN</Link>
        </div>
        <div className="login-box student-box">
          <h2>Student Login</h2>
          <div class="pic_box">
          <img src={Student} alt="Student" /></div>
          <Link to="/student-login" className="login-button" onClick={initiateOAuthFlow}>LOGIN</Link>
        </div>
        <div className="login-box staff-box">
          <h2>Staff Login</h2>
          <div class="pic_box">
          <img src={Staff} alt="Staff" /></div>
          <Link to="/staff-login" className="login-button">LOGIN</Link>
        </div>
      </div>
    </div>
  );
}

export default Home;

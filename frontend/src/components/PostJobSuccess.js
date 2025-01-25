import React from 'react';
import { Link } from 'react-router-dom';
import './PostJobSuccess.css';

const PostJobSuccess = () => {
  return (
    <div className="success-page">
      <div className="success-content">
        <div className="success-icon">
          <i className="fas fa-check-circle"></i>
        </div>
        
        <h1>Job Posted Successfully!</h1>
        <p className="message">
          Your job listing has been published and is now live on our job board.
        </p>
        
        <div className="next-steps">
          <h2>What's Next?</h2>
          <ul>
            <li>
              <i className="fas fa-eye"></i>
              Your job will be visible to thousands of qualified candidates
            </li>
            <li>
              <i className="fas fa-bell"></i>
              You'll receive email notifications when candidates apply
            </li>
            <li>
              <i className="fas fa-chart-line"></i>
              Track applications and engagement in real-time
            </li>
          </ul>
        </div>
        
        <div className="action-buttons">
          <Link to="/" className="primary-button">
            View Job Board
          </Link>
          <Link to="/post-job" className="secondary-button">
            Post Another Job
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PostJobSuccess; 
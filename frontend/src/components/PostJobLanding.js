import React from 'react';
import { useNavigate } from 'react-router-dom';
import './PostJobLanding.css';

const PostJobLanding = () => {
  const navigate = useNavigate();

  return (
    <div className="post-job-landing">
      <div className="landing-content">
        <h1>Post Your Roofing Job</h1>
        <p className="subtitle">Reach qualified roofing professionals across the country</p>

        <div className="pricing-card">
          <div className="price">
            <span className="amount">$35</span>
            <span className="period">per job posting</span>
          </div>

          <div className="features">
            <h3>What's Included:</h3>
            <ul>
              <li>
                <i className="fas fa-check"></i>
                30-day active job listing
              </li>
              <li>
                <i className="fas fa-check"></i>
                Reach thousands of qualified candidates
              </li>
              <li>
                <i className="fas fa-check"></i>
                Multiple application methods
              </li>
              <li>
                <i className="fas fa-check"></i>
                Real-time application tracking
              </li>
              <li>
                <i className="fas fa-check"></i>
                Premium job board placement
              </li>
            </ul>
          </div>

          <button 
            className="continue-button"
            onClick={() => navigate('/post-job/form')}
          >
            Continue to Job Form
            <i className="fas fa-arrow-right"></i>
          </button>
        </div>

        <div className="trust-signals">
          <div className="trust-item">
            <i className="fas fa-bolt"></i>
            <h4>Quick Setup</h4>
            <p>Post your job in minutes</p>
          </div>
          <div className="trust-item">
            <i className="fas fa-shield-alt"></i>
            <h4>Secure Payment</h4>
            <p>Protected by Stripe</p>
          </div>
          <div className="trust-item">
            <i className="fas fa-chart-line"></i>
            <h4>Wide Reach</h4>
            <p>Target qualified candidates</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostJobLanding; 
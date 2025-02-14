import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Header.css';
import logo from '../assets/findroofingjobs-logo.png';
import ReactGA from 'react-ga';

const Header = () => {
  const navigate = useNavigate();
  const [isHidden, setIsHidden] = useState(false);
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      
      if (currentScrollY > lastScrollY && currentScrollY > 70) {
        // Scrolling down & past header height
        setIsHidden(true);
      } else {
        // Scrolling up
        setIsHidden(false);
      }
      
      setLastScrollY(currentScrollY);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [lastScrollY]);

  const handlePostJobClick = () => {
    ReactGA.event({
      category: 'Navigation',
      action: 'Click',
      label: 'Post Job Button'
    });
    navigate('/post-job');
  };

  return (
    <nav className={`navbar ${isHidden ? 'hidden' : ''}`}>
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <img src={logo} alt="FindRoofingJobs.com" />
        </Link>
        
        <div className="nav-buttons">
          <a href={process.env.REACT_APP_BLOG_URL || 'http://localhost:2368'} className="nav-link" target="_blank" rel="noopener noreferrer">Blog</a>
          <Link 
            to="/post-job" 
            className="nav-post-job"
            onClick={handlePostJobClick}
          >
            Post Job
          </Link>
          <button className="nav-menu">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Header;
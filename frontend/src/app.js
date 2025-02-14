// src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import ReactGA from 'react-ga';
import JobList from './components/JobList';
import Filters from './components/Filters';
import LocationSelector from './components/LocationSelector';
import Header from './components/Header';
import JobModal from './components/JobModal';
import PostJobForm from './components/PostJobForm';
import PostJobLanding from './components/PostJobLanding';
import PostJobSuccess from './components/PostJobSuccess';
import './app.css';

const TrackPageViews = () => {
  const location = useLocation();

  useEffect(() => {
    ReactGA.pageview(location.pathname + location.search);
  }, [location]);

  return null;
};

const HomePage = ({ jobs, filteredJobs, handleFilterChange, handleLocationChange, handleJobClick, error, isLoading }) => (
    <main className="main-content">
        <div className="search-section">
            <LocationSelector onLocationChange={handleLocationChange} />
            <Filters onFilterChange={handleFilterChange} />
        </div>
        <div className="jobs-container">
            {error ? (
                <div className="error-message">
                    <h3>Unable to connect to job server</h3>
                    <p>Please try again later. The server might be temporarily down.</p>
                </div>
            ) : isLoading ? (
                <div className="loading">
                    <h3>Searching for jobs...</h3>
                </div>
            ) : filteredJobs.length > 0 ? (
                <JobList jobs={filteredJobs} onJobClick={handleJobClick} />
            ) : (
                <div className="no-jobs">
                    <h3>No jobs available at the moment</h3>
                    <p>Please check back later or try adjusting your search criteria.</p>
                </div>
            )}
        </div>
    </main>
);

const App = () => {
    const [jobs, setJobs] = useState([]);
    const [filteredJobs, setFilteredJobs] = useState([]);
    const [selectedJob, setSelectedJob] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchJobs = async () => {
            setIsLoading(true);
            try {
                console.log("Fetching jobs from API...");
                const response = await fetch('http://localhost:8000/api/v1/jobs');
                console.log("Response status:", response.status);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                console.log("Fetched jobs:", data);
                
                setJobs(data);
                setFilteredJobs(data);
                setError(null);
            } catch (error) {
                console.error('Error fetching jobs:', error);
                setError(error.message);
                setJobs([]);
                setFilteredJobs([]);
            } finally {
                setIsLoading(false);
            }
        };

        fetchJobs();
    }, []);

    const handleFilterChange = (jobFunction) => {
        if (!jobFunction) {
            setFilteredJobs(jobs);
        } else {
            const newFilteredJobs = jobs.filter(job => job.job_function === jobFunction);
            setFilteredJobs(newFilteredJobs);
        }
    };

    const handleLocationChange = async (locationFilter) => {
        setIsLoading(true);
        try {
            if (!locationFilter) {
                setFilteredJobs(jobs);
                setError(null);
            } else {
                const { zipCode, radius } = locationFilter;
                const response = await fetch(
                    `http://localhost:8000/api/v1/jobs/search/location?zip_code=${zipCode}&radius=${radius}`
                );
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setFilteredJobs(data);
                setError(null);
            }
        } catch (error) {
            console.error('Error searching jobs:', error);
            setError(error.message);
            setFilteredJobs([]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleJobClick = (job) => {
        setSelectedJob(job);
    };

    const handleCloseModal = () => {
        setSelectedJob(null);
    };

    return (
        <Router>
            <TrackPageViews />
            <div className="app-container">
                <Header />
                <Routes>
                    <Route path="/" element={
                        <HomePage 
                            jobs={jobs}
                            filteredJobs={filteredJobs}
                            handleFilterChange={handleFilterChange}
                            handleLocationChange={handleLocationChange}
                            handleJobClick={handleJobClick}
                            error={error}
                            isLoading={isLoading}
                        />
                    } />
                    {/* Redirect /post-job to the landing page */}
                    <Route path="/post-job" element={<Navigate to="/post-job/landing" replace />} />
                    <Route path="/post-job/landing" element={<PostJobLanding />} />
                    <Route path="/post-job/form" element={<PostJobForm />} />
                    <Route path="/post-job/success" element={<PostJobSuccess />} />
                </Routes>
                {selectedJob && <JobModal job={selectedJob} onClose={handleCloseModal} />}
            </div>
        </Router>
    );
};

export default App;
// src/App.js
import React, { useState, useEffect, useCallback } from 'react';
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

const HomePage = ({ jobs, filteredJobs, handleFilterChange, handleLocationChange, handleJobClick, error, isLoading, hasMore, onLoadMore }) => (
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
            ) : (
                <JobList 
                    jobs={filteredJobs} 
                    onJobClick={handleJobClick}
                    isLoading={isLoading}
                    hasMore={hasMore}
                    onLoadMore={onLoadMore}
                />
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
    const [page, setPage] = useState(0);
    const [hasMore, setHasMore] = useState(true);
    const JOBS_PER_PAGE = 25;

    const fetchJobs = useCallback(async (pageToFetch = 0) => {
        setIsLoading(true);
        try {
            console.log("Fetching jobs from API...");
            const skip = pageToFetch * JOBS_PER_PAGE;
            const response = await fetch(`https://your-render-backend-url.onrender.com/api/v1/jobs?skip=${skip}&limit=${JOBS_PER_PAGE}`);
            console.log("Response status:", response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Fetched jobs:", data);
            
            if (pageToFetch === 0) {
                setJobs(data.items);
                setFilteredJobs(data.items);
            } else {
                setJobs(prevJobs => [...prevJobs, ...data.items]);
                setFilteredJobs(prevJobs => [...prevJobs, ...data.items]);
            }
            
            setHasMore(data.items.length === JOBS_PER_PAGE);
            setError(null);
        } catch (error) {
            console.error('Error fetching jobs:', error);
            setError(error.message);
            setJobs([]);
            setFilteredJobs([]);
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchJobs(0);
    }, [fetchJobs]);

    const handleLoadMore = useCallback(() => {
        if (!isLoading && hasMore) {
            const nextPage = page + 1;
            setPage(nextPage);
            fetchJobs(nextPage);
        }
    }, [fetchJobs, isLoading, hasMore, page]);

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
                    <Route 
                        path="/" 
                        element={
                            <HomePage 
                                jobs={jobs}
                                filteredJobs={filteredJobs}
                                handleFilterChange={handleFilterChange}
                                handleLocationChange={handleLocationChange}
                                handleJobClick={handleJobClick}
                                error={error}
                                isLoading={isLoading}
                                hasMore={hasMore}
                                onLoadMore={handleLoadMore}
                            />
                        } 
                    />
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
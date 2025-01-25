import React from 'react';
import JobCard from './JobCard';

const JobList = ({ jobs, onJobClick }) => {
    return (
        <div className="job-list">
            {jobs.length > 0 ? (
                jobs.map(job => (
                    <JobCard 
                        key={job.id} 
                        job={job} 
                        onClick={onJobClick}
                    />
                ))
            ) : (
                <p>No jobs available.</p>
            )}
        </div>
    );
};

export default JobList;
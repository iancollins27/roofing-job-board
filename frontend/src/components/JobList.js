import React, { useEffect, useRef, useCallback } from 'react';
import JobCard from './JobCard';

const JobList = ({ jobs, onJobClick, isLoading, hasMore, onLoadMore }) => {
    const observer = useRef();
    const lastJobElementRef = useCallback(node => {
        if (isLoading) return;
        
        if (observer.current) {
            observer.current.disconnect();
        }
        
        observer.current = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting && hasMore) {
                onLoadMore();
            }
        });
        
        if (node) {
            observer.current.observe(node);
        }
    }, [isLoading, hasMore, onLoadMore]);

    return (
        <div className="job-list">
            {jobs.length > 0 ? (
                <>
                    {jobs.map((job, index) => (
                        <div
                            key={job.id}
                            ref={index === jobs.length - 1 ? lastJobElementRef : null}
                        >
                            <JobCard 
                                job={job} 
                                onClick={onJobClick}
                            />
                        </div>
                    ))}
                    {isLoading && (
                        <div className="loading-more">
                            <div className="loading-spinner"></div>
                            <p>Loading more jobs...</p>
                        </div>
                    )}
                </>
            ) : (
                <div className="no-jobs">
                    <h3>No jobs available at the moment</h3>
                    <p>Please check back later or try adjusting your search criteria.</p>
                </div>
            )}
        </div>
    );
};

export default JobList;
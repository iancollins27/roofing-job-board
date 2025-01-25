import React from 'react';
import './JobCard.css';

const JobCard = ({ job, onClick }) => {
  // Function to strip HTML tags and get plain text
  const stripHtml = (html) => {
    const tmp = document.createElement('div');
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || '';
  };

  // Get a preview of the description (first 150 chars, without HTML tags)
  const getDescriptionPreview = () => {
    const plainText = stripHtml(job.description || '');
    return plainText.substring(0, 150) + (plainText.length > 150 ? '...' : '');
  };

  // Add this function to format the job function text
  const formatJobFunction = (jobFunction) => {
    if (!jobFunction) return '';
    return jobFunction.charAt(0).toUpperCase() + jobFunction.slice(1).toLowerCase();
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Posted yesterday';
    if (diffDays < 7) return `Posted ${diffDays} days ago`;
    if (diffDays < 30) return `Posted ${Math.floor(diffDays / 7)} weeks ago`;
    return `Posted ${Math.floor(diffDays / 30)} months ago`;
  };

  const formatEmploymentType = (type) => {
    if (!type) return '';
    return type.split('-').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  return (
    <div className="job-card" onClick={() => onClick(job)}>
      <div className="job-card-header">
        <h3 className="job-title">{job.job_title}</h3>
        {job.posted_date && (
          <span className="posted-date">{formatDate(job.posted_date)}</span>
        )}
      </div>

      <div className="job-info">
        <div className="job-location-salary">
          <p className="location">
            <i className="fas fa-map-marker-alt"></i> {job.location}
          </p>
          {job.salary_range && (
            <p className="salary">
              <i className="fas fa-dollar-sign"></i> {job.salary_range}
            </p>
          )}
        </div>
      </div>

      <div className="job-tags">
        {job.employment_type && (
          <span className="tag employment-type">
            {formatEmploymentType(job.employment_type)}
          </span>
        )}
        {job.remote_type && (
          <span className="tag remote-type">
            {formatEmploymentType(job.remote_type)}
          </span>
        )}
        {job.job_function && (
          <span className="tag job-function">
            {formatJobFunction(job.job_function)}
          </span>
        )}
      </div>
      
      <div className="card-arrow">
        <i className="fas fa-chevron-right"></i>
      </div>
    </div>
  );
};

export default JobCard;
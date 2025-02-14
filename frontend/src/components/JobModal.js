import React, { useEffect } from 'react';
import './JobModal.css';
import { trackJobView } from '../utils/analytics';
import ReactGA from 'react-ga';

const JobModal = ({ job, onClose }) => {
  useEffect(() => {
    if (job) {
      trackJobView(job);
    }
  }, [job]);

  if (!job) return null;

  const formatJobFunction = (jobFunction) => {
    if (!jobFunction) return '';
    return jobFunction.charAt(0).toUpperCase() + jobFunction.slice(1).toLowerCase();
  };

  const handleApplyClick = (method) => {
    ReactGA.event({
      category: 'Job Application',
      action: 'Click Apply',
      label: `${method} - ${job.title}`
    });
    
    switch(method) {
      case 'email':
        window.location.href = `mailto:${job.application_email}?subject=Application for ${job.job_title}`;
        break;
      case 'link':
        window.open(job.application_link, '_blank');
        break;
      case 'company':
        window.open(job.company_url, '_blank');
        break;
      default:
        break;
    }
  };

  const ApplicationSection = () => (
    <div className="application-section">
      <h3>How to Apply</h3>
      <div className="application-methods">
        {job.application_email && (
          <button 
            className="apply-button email"
            onClick={() => handleApplyClick('email')}
          >
            <i className="fas fa-envelope"></i>
            Apply via Email
          </button>
        )}
        {job.application_link && (
          <button 
            className="apply-button external"
            onClick={() => handleApplyClick('link')}
          >
            <i className="fas fa-external-link-alt"></i>
            Apply on Job Site
          </button>
        )}
        {job.company_url && (
          <button 
            className="apply-button company"
            onClick={() => handleApplyClick('company')}
          >
            <i className="fas fa-building"></i>
            Apply on Company Site
          </button>
        )}
      </div>
    </div>
  );

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>
        
        <div className="modal-header">
          <h2>{job.job_title}</h2>
          <ApplicationSection />
        </div>

        <div className="modal-body">
          <div className="job-meta">
            <p className="location"><i className="fas fa-map-marker-alt"></i> {job.location}</p>
            {job.employment_type && (
              <p className="employment-type">
                <i className="fas fa-briefcase"></i> {job.employment_type}
              </p>
            )}
            {job.remote_type && (
              <p className="remote-type">
                <i className="fas fa-home"></i> {job.remote_type}
              </p>
            )}
            {job.salary_range && (
              <p className="salary">
                <i className="fas fa-dollar-sign"></i> {job.salary_range}
              </p>
            )}
          </div>

          <div className="job-description">
            <h3>Description</h3>
            <div 
              className="formatted-description"
              dangerouslySetInnerHTML={{ __html: job.description }}
            />
          </div>

          <ApplicationSection />
        </div>
      </div>
    </div>
  );
};

export default JobModal; 
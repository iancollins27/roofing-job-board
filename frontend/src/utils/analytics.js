// Simple analytics tracking for job interactions
const trackJobInteraction = (action, jobData) => {
  // Get existing interactions from session storage
  const existingInteractions = JSON.parse(sessionStorage.getItem('jobInteractions') || '[]');
  
  // Add new interaction
  const interaction = {
    timestamp: new Date().toISOString(),
    action,
    jobId: jobData.id,
    jobTitle: jobData.job_title,
    ...jobData
  };
  
  existingInteractions.push(interaction);
  
  // Store in session storage
  sessionStorage.setItem('jobInteractions', JSON.stringify(existingInteractions));
  
  // You can also send this to your backend or analytics service
  console.log('Job Interaction:', interaction);
};

export const trackJobView = (jobData) => {
  trackJobInteraction('view_details', jobData);
};

export const trackJobApplication = (jobData, method) => {
  trackJobInteraction('apply_click', { ...jobData, application_method: method });
}; 
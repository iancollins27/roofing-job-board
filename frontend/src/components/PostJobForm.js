import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactQuill from 'react-quill';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import 'react-quill/dist/quill.snow.css';  // Import Quill styles
import './PostJobForm.css';

// Initialize Stripe
const stripePromise = loadStripe('pk_test_51QkFrfITYxt3jMS523hBCavUIcSW4Ru06sDJE0sLDi4to8wvXUdtzaZZjMJGBQ3mFkMleuFtc9xwRDgw1ci1dUPD00XRslTjWP');

const PaymentForm = ({ onPaymentSuccess, isSubmitting }) => {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!stripe || !elements) return;

    const { error, paymentMethod } = await stripe.createPaymentMethod({
      type: 'card',
      card: elements.getElement(CardElement),
    });

    if (error) {
      setError(error.message);
    } else {
      onPaymentSuccess(paymentMethod.id);
    }
  };

  return (
    <div className="payment-section">
      <h3>Payment Details</h3>
      <p className="payment-info">Job posting fee: $35</p>
      <div className="card-element-container">
        <CardElement 
          options={{
            style: {
              base: {
                fontSize: '16px',
                color: '#424770',
                '::placeholder': {
                  color: '#aab7c4',
                },
              },
              invalid: {
                color: '#9e2146',
              },
            },
          }}
        />
      </div>
      {error && <div className="payment-error">{error}</div>}
      <button 
        type="submit"
        className="submit-button"
        disabled={!stripe || isSubmitting}
        onClick={handleSubmit}
      >
        {isSubmitting ? 'Processing...' : 'Pay & Post Job'}
      </button>
    </div>
  );
};

const PostJobForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    job_title: '',
    company_name: '',
    location: '',
    postal_code: '',  // Add zip code field
    employment_type: 'full-time',
    remote_type: 'on-site',
    description: '',  // This will now store HTML
    salary_range: '',
    application_email: '',
    application_link: '',
    company_url: '',
    job_function: 'LABOR' // Changed default value to match enum
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Quill editor modules/formats configuration
  const modules = {
    toolbar: [
      [{ 'header': [1, 2, 3, false] }],
      ['bold', 'italic', 'underline'],
      [{'list': 'ordered'}, {'list': 'bullet'}],
      ['link'],
      ['clean']
    ],
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleDescriptionChange = (content) => {
    setFormData(prev => ({ ...prev, description: content }));
  };

  const handlePaymentSuccess = async (paymentMethodId) => {
    setIsSubmitting(true);
    try {
      // First, create payment intent
      const paymentResponse = await fetch('http://localhost:8000/api/v1/payments/create-intent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount: 3500, // $35.00 in cents
          payment_method_id: paymentMethodId,
        }),
      });
      
      if (!paymentResponse.ok) {
        const errorData = await paymentResponse.json();
        throw new Error(errorData.detail || 'Payment failed');
      }
      
      const { client_secret } = await paymentResponse.json();

      // Then create the job
      const jobResponse = await fetch('http://localhost:8000/api/v1/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!jobResponse.ok) {
        const errorData = await jobResponse.json();
        throw new Error(errorData.detail || 'Failed to create job');
      }
      
      // Redirect to success page
      navigate('/post-job/success');
    } catch (error) {
      console.error('Error:', error);
      alert(error.message || 'There was an error processing your request. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="post-job-container">
      <h2>Post a Job</h2>
      <form className="post-job-form">
        <div className="form-group">
          <label htmlFor="job_title">Job Title *</label>
          <input
            type="text"
            id="job_title"
            name="job_title"
            value={formData.job_title}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="company_name">Company Name *</label>
          <input
            type="text"
            id="company_name"
            name="company_name"
            value={formData.company_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="location">City, State *</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
              placeholder="e.g. Austin, TX"
            />
          </div>

          <div className="form-group">
            <label htmlFor="postal_code">ZIP Code *</label>
            <input
              type="text"
              id="postal_code"
              name="postal_code"
              value={formData.postal_code}
              onChange={handleChange}
              required
              pattern="[0-9]{5}"
              placeholder="e.g. 78701"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="job_function">Job Function *</label>
            <select
              id="job_function"
              name="job_function"
              value={formData.job_function}
              onChange={handleChange}
              required
            >
              <option value="SALES">Sales</option>
              <option value="LABOR">Labor</option>
              <option value="PRODUCTION">Production</option>
              <option value="MANAGEMENT">Management</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="employment_type">Employment Type</label>
            <select
              id="employment_type"
              name="employment_type"
              value={formData.employment_type}
              onChange={handleChange}
            >
              <option value="full-time">Full Time</option>
              <option value="part-time">Part Time</option>
              <option value="contract">Contract</option>
              <option value="temporary">Temporary</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="remote_type">Work Type</label>
          <select
            id="remote_type"
            name="remote_type"
            value={formData.remote_type}
            onChange={handleChange}
          >
            <option value="on-site">On Site</option>
            <option value="remote">Remote</option>
            <option value="hybrid">Hybrid</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="description">Job Description *</label>
          <ReactQuill
            theme="snow"
            value={formData.description}
            onChange={handleDescriptionChange}
            modules={modules}
            className="quill-editor"
          />
        </div>

        <div className="form-group">
          <label htmlFor="salary_range">Salary Range</label>
          <input
            type="text"
            id="salary_range"
            name="salary_range"
            value={formData.salary_range}
            onChange={handleChange}
            placeholder="e.g. $50,000 - $70,000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="application_email">Application Email</label>
          <input
            type="email"
            id="application_email"
            name="application_email"
            value={formData.application_email}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="application_link">Application URL</label>
          <input
            type="url"
            id="application_link"
            name="application_link"
            value={formData.application_link}
            onChange={handleChange}
            placeholder="https://"
          />
        </div>

        <div className="form-group">
          <label htmlFor="company_url">Company Website</label>
          <input
            type="url"
            id="company_url"
            name="company_url"
            value={formData.company_url}
            onChange={handleChange}
            placeholder="https://"
          />
        </div>

        <Elements stripe={stripePromise}>
          <PaymentForm 
            onPaymentSuccess={handlePaymentSuccess}
            isSubmitting={isSubmitting}
          />
        </Elements>
      </form>
    </div>
  );
};

export default PostJobForm; 
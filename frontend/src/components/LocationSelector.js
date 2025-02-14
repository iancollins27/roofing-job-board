// src/components/LocationSelector.js
import React, { useState, useEffect } from 'react';

const LocationSelector = ({ onLocationChange }) => {
    const [zipCode, setZipCode] = useState('');
    const [radius, setRadius] = useState('25');

    const handleSubmit = (e) => {
        e.preventDefault();
        onLocationChange(zipCode.trim() ? { zipCode, radius: parseFloat(radius) } : null);
    };

    return (
        <div className="location-selector">
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter ZIP code (optional)"
                    value={zipCode}
                    onChange={e => setZipCode(e.target.value)}
                    pattern="[0-9]{5}|^$"
                    title="Please enter a valid 5-digit ZIP code or leave empty to show all jobs"
                />
                <select
                    value={radius}
                    onChange={e => setRadius(e.target.value)}
                    className="radius-select"
                >
                    <option value="25">25 mi</option>
                    <option value="50">50 mi</option>
                    <option value="100">100 mi</option>
                    <option value="150">150 mi</option>
                    <option value="200">200 mi</option>
                </select>
                <button type="submit">
                    {zipCode.trim() ? 'Search Jobs' : 'Show All Jobs'}
                </button>
            </form>
        </div>
    );
};

export default LocationSelector;
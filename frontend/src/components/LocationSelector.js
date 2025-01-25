// src/components/LocationSelector.js
import React, { useState, useEffect } from 'react';

const LocationSelector = ({ onLocationChange }) => {
    const [zipCode, setZipCode] = useState('');
    const [radius, setRadius] = useState('150');
    const [isLoadingLocation, setIsLoadingLocation] = useState(true);

    useEffect(() => {
        const getUserLocation = async () => {
            try {
                // Get user's coordinates
                const position = await new Promise((resolve, reject) => {
                    navigator.geolocation.getCurrentPosition(resolve, reject);
                });

                const { latitude, longitude } = position.coords;

                // Use Nominatim for reverse geocoding (free service)
                const response = await fetch(
                    `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&addressdetails=1`,
                    {
                        headers: {
                            'User-Agent': 'RoofingJobBoard/1.0'
                        }
                    }
                );
                
                if (!response.ok) {
                    throw new Error('Failed to get location details');
                }

                const data = await response.json();
                const userZip = data.address.postcode;
                
                if (userZip) {
                    setZipCode(userZip);
                    // Trigger initial search with user's location
                    onLocationChange({ zipCode: userZip, radius: parseFloat(radius) });
                }
            } catch (error) {
                console.error('Error getting user location:', error);
                // Silently fail - user can still enter ZIP manually
            } finally {
                setIsLoadingLocation(false);
            }
        };

        getUserLocation();
    }, [radius, onLocationChange]);

    const handleSubmit = (e) => {
        e.preventDefault();
        onLocationChange(zipCode.trim() ? { zipCode, radius: parseFloat(radius) } : null);
    };

    return (
        <div className="location-selector">
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder={isLoadingLocation ? "Getting your location..." : "Enter ZIP code (optional)"}
                    value={zipCode}
                    onChange={e => setZipCode(e.target.value)}
                    pattern="[0-9]{5}|^$"
                    title="Please enter a valid 5-digit ZIP code or leave empty to show all jobs"
                    disabled={isLoadingLocation}
                />
                <select
                    value={radius}
                    onChange={e => setRadius(e.target.value)}
                    disabled={isLoadingLocation}
                >
                    <option value="25">Within 25 miles</option>
                    <option value="50">Within 50 miles</option>
                    <option value="100">Within 100 miles</option>
                    <option value="150">Within 150 miles</option>
                    <option value="200">Within 200 miles</option>
                </select>
                <button type="submit" disabled={isLoadingLocation}>
                    {isLoadingLocation ? 'Getting Location...' : (zipCode.trim() ? 'Search Jobs' : 'Show All Jobs')}
                </button>
            </form>
        </div>
    );
};

export default LocationSelector;
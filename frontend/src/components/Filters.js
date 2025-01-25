import React from 'react';

const Filters = ({ onFilterChange }) => {
    return (
        <div className="filters">
            <select 
                onChange={e => onFilterChange(e.target.value)}
                className="function-filter"
            >
                <option value="">All Job Functions</option>
                <option value="sales">Sales</option>
                <option value="labor">Labor</option>
                <option value="production">Production</option>
                <option value="management">Management</option>
            </select>
        </div>
    );
};

export default Filters;

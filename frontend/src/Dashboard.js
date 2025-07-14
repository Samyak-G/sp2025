import React, { useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Dashboard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [dockResults, setDockResults] = useState(null);
  const [fulfillmentResults, setFulfillmentResults] = useState(null);
  const [carbonResults, setCarbonResults] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState({
    dock: false,
    fulfillment: false,
    carbon: false,
    recommendations: false
  });

  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Dock Efficiency',
        data: [65, 72, 78, 85, 82, 90],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
      },
      {
        label: 'Carbon Reduction',
        data: [20, 25, 30, 35, 40, 45],
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'SmartFlow Analytics',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const testDockScheduler = async () => {
    setLoading(prev => ({ ...prev, dock: true }));
    const testData = {
      truck_id: 'TRK001',
      size: 'large',
      cargo_type: 'general',
      arrival_time: '14:30',
    };

    try {
      const response = await fetch('http://localhost:5000/api/dock-scheduler', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testData),
      });
      const data = await response.json();
      setDockResults({
        dock_assignment: data.dock_assignment,
        time_slot: data.time_slot,
        status: 'success'
      });
    } catch (error) {
      setDockResults({
        error: 'Failed to connect to dock scheduler',
        status: 'error'
      });
    } finally {
      setLoading(prev => ({ ...prev, dock: false }));
    }
  };

  const testFulfillment = async () => {
    setLoading(prev => ({ ...prev, fulfillment: true }));
    const testData = {
      customer_location: 'Mumbai',
      order_items: ['electronics', 'books'],
      priority: 'standard',
    };

    try {
      const response = await fetch('http://localhost:5000/api/fulfillment-engine', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testData),
      });
      const data = await response.json();
      setFulfillmentResults({
        warehouse: data.warehouse,
        estimated_delivery: data.estimated_delivery,
        status: 'success'
      });
    } catch (error) {
      setFulfillmentResults({
        error: 'Failed to connect to fulfillment engine',
        status: 'error'
      });
    } finally {
      setLoading(prev => ({ ...prev, fulfillment: false }));
    }
  };

  const testCarbonCalculator = async () => {
    setLoading(prev => ({ ...prev, carbon: true }));
    const testData = {
      distance: 25,
      vehicle_type: 'truck',
      delivery_type: 'standard',
    };

    try {
      const response = await fetch('http://localhost:5000/api/carbon-calculator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testData),
      });
      const data = await response.json();
      setCarbonResults({
        carbon_footprint: data.carbon_footprint,
        eco_friendly_options: data.eco_friendly_options,
        status: 'success'
      });
    } catch (error) {
      setCarbonResults({
        error: 'Failed to connect to carbon calculator',
        status: 'error'
      });
    } finally {
      setLoading(prev => ({ ...prev, carbon: false }));
    }
  };

  const getRecommendations = async () => {
    if (!userInput.trim()) return;
    
    setLoading(prev => ({ ...prev, recommendations: true }));
    const testData = {
      user_input: userInput,
      user_data: {
        age: 28,
        location: 'Mumbai',
        income_level: 'middle',
      },
    };

    try {
      const response = await fetch('http://localhost:5000/api/product-recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testData),
      });
      const data = await response.json();
      setRecommendations({
        recommendations: data.recommendations,
        status: 'success'
      });
    } catch (error) {
      setRecommendations({
        error: 'Failed to connect to recommendation engine',
        status: 'error'
      });
    } finally {
      setLoading(prev => ({ ...prev, recommendations: false }));
    }
  };

  const showHeatmap = () => {
    
    alert('Heatmap functionality would be implemented here');
  };

  const renderResult = (result, type) => {
    if (!result) return null;
    
    if (result.status === 'error') {
      return (
        <div className="alert alert-danger">
          <strong>Error:</strong> {result.error}
        </div>
      );
    }

    switch (type) {
      case 'dock':
        return (
          <div className="alert alert-success">
            <strong>Scheduled!</strong><br />
            Dock: {result.dock_assignment}<br />
            Time: {result.time_slot}
          </div>
        );
      case 'fulfillment':
        return (
          <div className="alert alert-info">
            <strong>Optimal Warehouse:</strong> {result.warehouse}<br />
            <strong>Delivery Time:</strong> {result.estimated_delivery}
          </div>
        );
      case 'carbon':
        return (
          <div className="alert alert-warning">
            <strong>Carbon Footprint:</strong> {result.carbon_footprint}<br />
            <strong>Eco-friendly options:</strong> {result.eco_friendly_options ? 'Available' : 'Not Available'}
          </div>
        );
      case 'recommendations':
        return (
          <div className="alert alert-success">
            <strong>Recommendations:</strong><br />
            {result.recommendations.map((item, index) => (
              <div key={index}>• {item}</div>
            ))}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container">
          <span className="navbar-brand">
            SmartFlow
          </span>
          <span className="navbar-text">AI-Powered Walmart Management System</span>
        </div>
      </nav>

      <div className="container mt-4">
        <div className="row">
          
          <div className="col-md-6">
            <div className="feature-card">
              <h5>
                <span className="status-indicator status-active"></span>
                AI Dock & Inventory Scheduler
              </h5>
              <p>Optimize dock scheduling and inventory placement</p>
              <button 
                className="btn btn-primary me-2" 
                onClick={testDockScheduler}
                disabled={loading.dock}
              >
                {loading.dock ? 'Scheduling...' : 'Schedule Truck'}
              </button>
              <button className="btn btn-secondary" onClick={showHeatmap}>
                View Heatmap
              </button>
              <div className="mt-3">
                {renderResult(dockResults, 'dock')}
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="feature-card">
              <h5>
                <span className="status-indicator status-active"></span>
                Geo-Intelligent Fulfillment
              </h5>
              <p>Select optimal warehouse and delivery routes</p>
              <button 
                className="btn btn-primary" 
                onClick={testFulfillment}
                disabled={loading.fulfillment}
              >
                {loading.fulfillment ? 'Processing...' : 'Find Best Warehouse'}
              </button>
              <div className="mt-3">
                {renderResult(fulfillmentResults, 'fulfillment')}
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="feature-card">
              <h5>
                <span className="status-indicator status-active"></span>
                Carbon Footprint Estimator
              </h5>
              <p>Calculate and optimize delivery emissions</p>
              <button 
                className="btn btn-primary" 
                onClick={testCarbonCalculator}
                disabled={loading.carbon}
              >
                {loading.carbon ? 'Calculating...' : 'Calculate Emissions'}
              </button>
              <div className="mt-3">
                {renderResult(carbonResults, 'carbon')}
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="feature-card">
              <h5>
                <span className="status-indicator status-active"></span>
                Emotion-Aware Recommendations
              </h5>
              <p>AI-powered product recommendations</p>
              <input
                type="text"
                className="form-control mb-2"
                placeholder="Enter your message..."
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && getRecommendations()}
              />
              <button 
                className="btn btn-primary" 
                onClick={getRecommendations}
                disabled={loading.recommendations || !userInput.trim()}
              >
                {loading.recommendations ? 'Processing...' : 'Get Recommendations'}
              </button>
              <div className="mt-3">
                {renderResult(recommendations, 'recommendations')}
              </div>
            </div>
          </div>
        </div>

        <div className="row mt-4">
          <div className="col-12">
            <div className="feature-card">
              <h5>System Analytics</h5>
              <div style={{ height: '400px' }}>
                <Line data={chartData} options={chartOptions} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

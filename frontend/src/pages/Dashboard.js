import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService, predictionService } from '../services/api';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    if (!currentUser) {
      navigate('/login');
      return;
    }
    setUser(currentUser);
    loadHistory();
  }, [navigate]);

  const loadHistory = async () => {
    try {
      const data = await predictionService.getHistory();
      setHistory(data.slice(0, 5)); // Show only last 5
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const handleFileSelect = (file) => {
    if (file) {
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
      if (!validTypes.includes(file.type)) {
        setError('Please select a valid image file (JPG, JPEG, or PNG)');
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }

      setSelectedFile(file);
      setError('');
      setPrediction(null);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFileChange = (e) => {
    handleFileSelect(e.target.files[0]);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await predictionService.predict(selectedFile);
      setPrediction(result);
      loadHistory(); // Refresh history
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
    navigate('/');
  };

  const getClassBadgeClass = (classNum) => {
    const classes = {
      0: 'badge-success',
      1: 'badge-info',
      2: 'badge-warning',
      3: 'badge-warning',
      4: 'badge-danger',
    };
    return classes[classNum] || 'badge-info';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (!user) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="container-fluid">
          <div className="header-content">
            <h1 className="logo">DR Detection System</h1>
            <div className="header-actions">
              <span className="user-name">Welcome, {user.name}</span>
              <button onClick={handleLogout} className="btn btn-outline">
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="dashboard-content">
        <div className="container-fluid">
          {/* Summary Cards */}
          <div className="summary-cards">
            <div className="summary-card">
              <div className="summary-icon">📊</div>
              <div className="summary-info">
                <div className="summary-value">{history.length}</div>
                <div className="summary-label">Total Scans</div>
              </div>
            </div>

            <div className="summary-card">
              <div className="summary-icon">⏱️</div>
              <div className="summary-info">
                <div className="summary-value">
                  {prediction ? `${(prediction.confidence * 100).toFixed(1)}%` : '--'}
                </div>
                <div className="summary-label">Last Confidence</div>
              </div>
            </div>

            <div className="summary-card">
              <div className="summary-icon">🎯</div>
              <div className="summary-info">
                <div className="summary-value">
                  {prediction ? prediction.class_name : 'No prediction yet'}
                </div>
                <div className="summary-label">Last Prediction</div>
              </div>
            </div>
          </div>

          <div className="dashboard-grid">
            {/* Upload Section */}
            <div className="card upload-card">
              <div className="card-header">
                <h2>Upload Retinal Image</h2>
              </div>
              <div className="card-body">
                <div
                  className={`upload-zone ${dragActive ? 'drag-active' : ''}`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  {preview ? (
                    <div className="image-preview">
                      <img src={preview} alt="Preview" />
                      <button
                        className="remove-image"
                        onClick={() => {
                          setSelectedFile(null);
                          setPreview(null);
                          setPrediction(null);
                        }}
                      >
                        ×
                      </button>
                    </div>
                  ) : (
                    <div className="upload-placeholder">
                      <div className="upload-icon">📁</div>
                      <p className="upload-text">
                        Drag & drop your retinal image here
                      </p>
                      <p className="upload-subtext">or</p>
                      <label htmlFor="file-upload" className="btn btn-primary">
                        Browse Files
                      </label>
                      <input
                        id="file-upload"
                        type="file"
                        accept="image/jpeg,image/jpg,image/png"
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                      />
                      <p className="upload-hint">
                        Supported formats: JPG, JPEG, PNG (Max 10MB)
                      </p>
                    </div>
                  )}
                </div>

                {error && (
                  <div className="alert alert-error mt-2">
                    {error}
                  </div>
                )}

                {selectedFile && !prediction && (
                  <button
                    onClick={handleAnalyze}
                    className="btn btn-primary w-100 mt-3"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner"></span>
                        Analyzing...
                      </>
                    ) : (
                      'Analyze Image'
                    )}
                  </button>
                )}
              </div>
            </div>

            {/* Results Section */}
            {prediction && (
              <div className="card result-card">
                <div className="card-header">
                  <h2>Analysis Results</h2>
                </div>
                <div className="card-body">
                  <div className="result-main">
                    <div className="result-class">
                      <span className={`badge ${getClassBadgeClass(prediction.predicted_class)}`}>
                        {prediction.class_name}
                      </span>
                    </div>
                    
                    <div className="result-confidence">
                      <div className="confidence-label">
                        Confidence Score
                      </div>
                      <div className="confidence-value">
                        {(prediction.confidence * 100).toFixed(2)}%
                      </div>
                      <div className="progress">
                        <div
                          className="progress-bar"
                          style={{ width: `${prediction.confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="result-explanation">
                      <h4>Interpretation</h4>
                      <p>{prediction.explanation}</p>
                    </div>

                    <div className="result-disclaimer">
                      <strong>Important:</strong> This is an AI-assisted screening tool 
                      and should not replace professional medical diagnosis. Please consult 
                      with a qualified ophthalmologist for proper evaluation and treatment.
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* History Section */}
            <div className="card history-card">
              <div className="card-header">
                <h2>Recent Scans</h2>
              </div>
              <div className="card-body">
                {history.length > 0 ? (
                  <div className="history-list">
                    {history.map((item) => (
                      <div key={item.id} className="history-item">
                        <div className="history-info">
                          <div className="history-date">
                            {formatDate(item.created_at)}
                          </div>
                          <div className="history-result">
                            <span className={`badge ${getClassBadgeClass(item.predicted_class)}`}>
                              Class {item.predicted_class}
                            </span>
                            <span className="confidence-text">
                              {(item.confidence * 100).toFixed(1)}% confidence
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="no-history">No scans yet. Upload an image to get started!</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

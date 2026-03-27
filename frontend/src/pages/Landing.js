import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Landing.css';

const Landing = () => {
  return (
    <div className="landing">
      {/* Navigation */}
      <nav className="navbar">
        <div className="container">
          <div className="navbar-content">
            <h1 className="logo">DR Detection System</h1>
            <div className="nav-links">
              <Link to="/about" className="nav-link">About</Link>
              <Link to="/login" className="btn btn-outline">Login</Link>
              <Link to="/register" className="btn btn-primary">Get Started</Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <div className="hero-text">
              <h1 className="hero-title">
               GAN-Based Diabetic Retinopathy Detection
              </h1>
              <p className="hero-subtitle">
                Early detection saves vision. Our advanced GAN-based deep learning system 
                analyzes retinal images to detect and classify diabetic retinopathy with 
                exceptional accuracy.
              </p>
              <div className="hero-buttons">
                <Link to="/register" className="btn btn-primary btn-large">
                  Start Free Analysis
                </Link>
                <Link to="/about" className="btn btn-outline btn-large">
                  Learn More
                </Link>
              </div>
              <div className="hero-stats">
                <div className="stat">
                  <div className="stat-number">95%+</div>
                  <div className="stat-label">Accuracy</div>
                </div>
                <div className="stat">
                  <div className="stat-number">&lt;30s</div>
                  <div className="stat-label">Analysis Time</div>
                </div>
                <div className="stat">
                  <div className="stat-number">5</div>
                  <div className="stat-label">DR Stages</div>
                </div>
              </div>
            </div>
            <div className="hero-image">
              <div className="retina-visual">
                <img 
                  src="https://images.unsplash.com/photo-1559757175-5700dde675bc?w=600&h=600&fit=crop" 
                  alt="Retinal scan illustration"
                  className="retina-img"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pipeline Section */}
      <section className="pipeline-section">
        <div className="container">
          <h2 className="section-title">Advanced AI Pipeline</h2>
          <p className="section-subtitle">
            Our hybrid deep learning approach combines multiple state-of-the-art technologies
          </p>
          
          <div className="pipeline-cards">
            <div className="pipeline-card">
              <div className="pipeline-icon">📸</div>
              <h3>Preprocessing</h3>
              <p>
                Images are enhanced using CLAHE for contrast, Gaussian blur for noise 
                reduction, and normalized for optimal analysis.
              </p>
            </div>
            
            <div className="pipeline-card">
              <div className="pipeline-icon">🎨</div>
              <h3>GAN Augmentation</h3>
              <p>
                Generative Adversarial Networks create synthetic retinal images to 
                expand the dataset and handle class imbalance.
              </p>
            </div>
            
            <div className="pipeline-card">
              <div className="pipeline-icon">🧠</div>
              <h3>Hybrid CNN Features</h3>
              <p>
                VGG16, MobileNet, and DenseNet121 extract comprehensive features 
                from multiple perspectives.
              </p>
            </div>
            
            <div className="pipeline-card">
              <div className="pipeline-icon">⚡</div>
              <h3>Vision Transformer</h3>
              <p>
                State-of-the-art transformer architecture classifies DR into 5 
                severity stages with high precision.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Advantages Section */}
      <section className="advantages-section">
        <div className="container">
          <h2 className="section-title">Why Choose Our System?</h2>
          
          <div className="advantages-grid">
            <div className="advantage-item">
              <div className="advantage-icon">⚡</div>
              <h3>Lightning Fast</h3>
              <p>Get results in under 30 seconds with our optimized inference pipeline</p>
            </div>
            
            <div className="advantage-item">
              <div className="advantage-icon">🎯</div>
              <h3>Highly Accurate</h3>
              <p>95%+ accuracy validated on extensive datasets with robust evaluation</p>
            </div>
            
            <div className="advantage-item">
              <div className="advantage-icon">🤖</div>
              <h3>Fully Automated</h3>
              <p>No manual intervention required - upload and receive instant analysis</p>
            </div>
            
            <div className="advantage-item">
              <div className="advantage-icon">📈</div>
              <h3>Scalable</h3>
              <p>Handle thousands of scans per day with cloud-ready architecture</p>
            </div>
            
            <div className="advantage-item">
              <div className="advantage-icon">🔒</div>
              <h3>Secure & Private</h3>
              <p>HIPAA-compliant data handling with encrypted storage and transmission</p>
            </div>
            
            <div className="advantage-item">
              <div className="advantage-icon">💪</div>
              <h3>Robust</h3>
              <p>Handles various image qualities and conditions with advanced preprocessing</p>
            </div>
          </div>
        </div>
      </section>

      {/* DR Stages Section */}
      <section className="stages-section">
        <div className="container">
          <h2 className="section-title">Diabetic Retinopathy Stages</h2>
          
          <div className="stages-list">
            <div className="stage-item stage-0">
              <div className="stage-badge">Stage 0</div>
              <h3>No DR</h3>
              <p>No abnormalities detected. Continue regular monitoring.</p>
            </div>
            
            <div className="stage-item stage-1">
              <div className="stage-badge">Stage 1</div>
              <h3>Mild DR</h3>
              <p>Microaneurysms present. Early stage requiring monitoring.</p>
            </div>
            
            <div className="stage-item stage-2">
              <div className="stage-badge">Stage 2</div>
              <h3>Moderate DR</h3>
              <p>More extensive microaneurysms and hemorrhages visible.</p>
            </div>
            
            <div className="stage-item stage-3">
              <div className="stage-badge">Stage 3</div>
              <h3>Severe DR</h3>
              <p>Extensive hemorrhages and cotton-wool spots. Urgent care needed.</p>
            </div>
            
            <div className="stage-item stage-4">
              <div className="stage-badge">Stage 4</div>
              <h3>Proliferative DR</h3>
              <p>Neovascularization present. Immediate treatment required.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h3>DR Detection System</h3>
              <p>AI-powered early detection for better vision health</p>
            </div>
            
            <div className="footer-section">
              <h4>Quick Links</h4>
              <Link to="/about">About</Link>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </div>
            
            <div className="footer-section">
              <h4>Resources</h4>
              <Link to="/about">Documentation</Link>
              <a href="#contact">Contact Us</a>
              <a href="#privacy">Privacy Policy</a>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>&copy; 2025 GAN-Based DR Detection System. This is a research tool, not a medical device.</p>
            <p>&copy; Developed By VIIT_Vizag_IT</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;

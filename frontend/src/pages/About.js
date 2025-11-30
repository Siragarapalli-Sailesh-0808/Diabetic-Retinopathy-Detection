import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/About.css';

const About = () => {
  return (
    <div className="about-page">
      <nav className="navbar">
        <div className="container">
          <div className="navbar-content">
            <Link to="/" className="logo">DR Detection System</Link>
            <div className="nav-links">
              <Link to="/" className="nav-link">Home</Link>
              <Link to="/login" className="btn btn-outline">Login</Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="about-content">
        <div className="container">
          <section className="about-hero">
            <h1>About Diabetic Retinopathy Detection</h1>
            <p className="lead">
              Understanding our AI-powered system and the importance of early detection
            </p>
          </section>

          <section className="content-section">
            <h2>What is Diabetic Retinopathy?</h2>
            <p>
              Diabetic retinopathy (DR) is a diabetes complication that affects the eyes. It's 
              caused by damage to the blood vessels of the light-sensitive tissue at the back 
              of the eye (retina). At first, diabetic retinopathy may cause no symptoms or only 
              mild vision problems. Eventually, it can cause blindness.
            </p>
            <p>
              The condition can develop in anyone who has type 1 or type 2 diabetes. The longer 
              you have diabetes and the less controlled your blood sugar is, the more likely you 
              are to develop this eye complication.
            </p>
          </section>

          <section className="content-section">
            <h2>The Five Severity Levels</h2>
            
            <div className="severity-grid">
              <div className="severity-card">
                <div className="severity-header level-0">
                  <h3>Stage 0: No DR</h3>
                </div>
                <div className="severity-body">
                  <p>
                    No abnormalities detected in the retinal images. This represents a healthy 
                    retina with no visible signs of diabetic retinopathy. Continue regular 
                    monitoring and maintain good blood sugar control.
                  </p>
                </div>
              </div>

              <div className="severity-card">
                <div className="severity-header level-1">
                  <h3>Stage 1: Mild DR</h3>
                </div>
                <div className="severity-body">
                  <p>
                    Microaneurysms are present. These are small areas of balloon-like swelling 
                    in the retina's tiny blood vessels. This is the earliest stage of diabetic 
                    retinopathy. Regular follow-up examinations are recommended, typically every 
                    12 months.
                  </p>
                </div>
              </div>

              <div className="severity-card">
                <div className="severity-header level-2">
                  <h3>Stage 2: Moderate DR</h3>
                </div>
                <div className="severity-body">
                  <p>
                    More extensive microaneurysms and hemorrhages are visible. Some blood vessels 
                    that nourish the retina are blocked. Close monitoring is required, with 
                    follow-up examinations every 6-9 months. Strict blood glucose control is 
                    essential.
                  </p>
                </div>
              </div>

              <div className="severity-card">
                <div className="severity-header level-3">
                  <h3>Stage 3: Severe DR</h3>
                </div>
                <div className="severity-body">
                  <p>
                    Extensive hemorrhages and cotton-wool spots are present. Many more blood 
                    vessels are blocked, depriving several areas of the retina of their blood 
                    supply. These areas signal the retina to grow new blood vessels. Urgent 
                    ophthalmologist consultation is recommended.
                  </p>
                </div>
              </div>

              <div className="severity-card">
                <div className="severity-header level-4">
                  <h3>Stage 4: Proliferative DR</h3>
                </div>
                <div className="severity-body">
                  <p>
                    Neovascularization (growth of new abnormal blood vessels) is present. These 
                    new blood vessels are fragile and can leak fluid, causing severe vision 
                    problems and potentially leading to retinal detachment or glaucoma. Immediate 
                    treatment is required to prevent vision loss.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section className="content-section">
            <h2>Our AI Pipeline</h2>
            
            <div className="pipeline-detail">
              <div className="pipeline-step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h3>Image Preprocessing</h3>
                  <p>
                    <strong>Resize:</strong> All images are standardized to 224x224 pixels for 
                    consistent processing.
                  </p>
                  <p>
                    <strong>CLAHE:</strong> Contrast Limited Adaptive Histogram Equalization 
                    enhances the contrast and makes subtle features more visible.
                  </p>
                  <p>
                    <strong>Gaussian Blur:</strong> Noise reduction technique that smooths the 
                    image while preserving important features.
                  </p>
                  <p>
                    <strong>Normalization:</strong> Pixel values are scaled to the range [0, 1] 
                    for optimal neural network processing.
                  </p>
                </div>
              </div>

              <div className="pipeline-step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h3>GAN-based Data Augmentation</h3>
                  <p>
                    We use a Generative Adversarial Network (GAN) with a DCGAN architecture to 
                    generate synthetic retinal images. This helps:
                  </p>
                  <ul>
                    <li>Expand the training dataset significantly</li>
                    <li>Handle class imbalance between different DR severity levels</li>
                    <li>Improve model robustness and generalization</li>
                    <li>Reduce overfitting on limited real-world data</li>
                  </ul>
                </div>
              </div>

              <div className="pipeline-step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h3>Hybrid CNN Feature Extraction</h3>
                  <p>
                    We employ three state-of-the-art pre-trained CNN architectures in parallel:
                  </p>
                  <ul>
                    <li><strong>VGG16:</strong> Deep architecture excellent at capturing detailed patterns</li>
                    <li><strong>MobileNet:</strong> Efficient lightweight model for diverse feature extraction</li>
                    <li><strong>DenseNet121:</strong> Dense connections preserve fine-grained information</li>
                  </ul>
                  <p>
                    Features from all three models are concatenated to create a comprehensive 
                    2560-dimensional feature vector, capturing multiple perspectives of the retinal image.
                  </p>
                </div>
              </div>

              <div className="pipeline-step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h3>Vision Transformer Classification</h3>
                  <p>
                    The concatenated features are fed into a Vision Transformer (ViT) classifier with:
                  </p>
                  <ul>
                    <li>Multi-head self-attention mechanisms for global context understanding</li>
                    <li>4 transformer blocks with 8 attention heads each</li>
                    <li>Dense layers for final classification into 5 DR severity classes</li>
                    <li>Softmax activation to output class probabilities</li>
                  </ul>
                </div>
              </div>

              <div className="pipeline-step">
                <div className="step-number">5</div>
                <div className="step-content">
                  <h3>Evaluation & Metrics</h3>
                  <p>
                    Model performance is rigorously evaluated using:
                  </p>
                  <ul>
                    <li><strong>Accuracy:</strong> Overall classification correctness</li>
                    <li><strong>Precision:</strong> Ratio of true positives to predicted positives</li>
                    <li><strong>Recall:</strong> Ratio of true positives to actual positives</li>
                    <li><strong>F1-Score:</strong> Harmonic mean of precision and recall</li>
                    <li><strong>Confusion Matrix:</strong> Detailed per-class performance analysis</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>

          <section className="content-section disclaimer-section">
            <h2>Important Disclaimer</h2>
            <div className="disclaimer-box">
              <p>
                <strong>This is a research and educational tool, NOT a certified medical device.</strong>
              </p>
              <p>
                While our system achieves high accuracy in detecting diabetic retinopathy, it should 
                NEVER be used as a substitute for professional medical diagnosis and treatment. The 
                results provided by this system are for informational and screening purposes only.
              </p>
              <p>
                <strong>Always consult with a qualified ophthalmologist or healthcare provider for:</strong>
              </p>
              <ul>
                <li>Proper diagnosis and confirmation of any eye condition</li>
                <li>Treatment recommendations and medical advice</li>
                <li>Regular eye examinations and monitoring</li>
                <li>Any concerns about your vision or eye health</li>
              </ul>
              <p>
                Do not make any medical decisions based solely on the output of this AI system. 
                Early detection and professional medical care are crucial for preventing vision loss 
                from diabetic retinopathy.
              </p>
            </div>
          </section>

          <section className="content-section cta-section">
            <h2>Ready to Get Started?</h2>
            <p>
              Create a free account and start analyzing retinal images with our AI-powered system.
            </p>
            <div className="cta-buttons">
              <Link to="/register" className="btn btn-primary btn-large">
                Create Free Account
              </Link>
              <Link to="/" className="btn btn-outline btn-large">
                Back to Home
              </Link>
            </div>
          </section>
        </div>
      </div>

      <footer className="footer">
        <div className="container">
          <div className="footer-bottom">
            <p>&copy; 2024 DR Detection System. Research tool for educational purposes.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default About;

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../services/api';
import '../styles/Auth.css';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'user',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const validatePassword = (password) => {
    const minLength = password.length >= 6;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    
    return {
      minLength,
      hasUpper,
      hasLower,
      hasNumber,
      isValid: minLength && hasUpper && hasLower && hasNumber,
    };
  };

  const passwordStrength = validatePassword(formData.password);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    // Clear error for this field
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: '',
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    // Validation
    const newErrors = {};
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    }
    if (!passwordStrength.isValid) {
      newErrors.password = 'Password does not meet requirements';
    }
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);

    try {
      await authService.register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        role: formData.role,
      });
      
      // Auto login after registration
      await authService.login({
        email: formData.email,
        password: formData.password,
      });
      
      navigate('/dashboard');
    } catch (err) {
      setErrors({
        general: err.response?.data?.detail || 'Registration failed. Please try again.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <Link to="/" className="auth-logo">DR Detection System</Link>
          <h1 className="auth-title">Create Account</h1>
          <p className="auth-subtitle">Start detecting diabetic retinopathy with AI</p>
        </div>

        {errors.general && (
          <div className="alert alert-error">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="name" className="form-label">
              Full Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              className="form-control"
              placeholder="John Doe"
              value={formData.name}
              onChange={handleChange}
              required
            />
            {errors.name && <div className="form-error">{errors.name}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-control"
              placeholder="your.email@example.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
            {errors.email && <div className="form-error">{errors.email}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="role" className="form-label">
              Role
            </label>
            <select
              id="role"
              name="role"
              className="form-control form-select"
              value={formData.role}
              onChange={handleChange}
            >
              <option value="user">Patient</option>
              <option value="doctor">Doctor</option>
              <option value="admin">Administrator</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className="form-control"
              placeholder="Create a strong password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            {formData.password && (
              <div className="password-strength">
                <div className="strength-item">
                  <span className={passwordStrength.minLength ? 'valid' : 'invalid'}>
                    {passwordStrength.minLength ? '✓' : '○'}
                  </span>
                  At least 6 characters
                </div>
                <div className="strength-item">
                  <span className={passwordStrength.hasUpper ? 'valid' : 'invalid'}>
                    {passwordStrength.hasUpper ? '✓' : '○'}
                  </span>
                  One uppercase letter
                </div>
                <div className="strength-item">
                  <span className={passwordStrength.hasLower ? 'valid' : 'invalid'}>
                    {passwordStrength.hasLower ? '✓' : '○'}
                  </span>
                  One lowercase letter
                </div>
                <div className="strength-item">
                  <span className={passwordStrength.hasNumber ? 'valid' : 'invalid'}>
                    {passwordStrength.hasNumber ? '✓' : '○'}
                  </span>
                  One number
                </div>
              </div>
            )}
            {errors.password && <div className="form-error">{errors.password}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword" className="form-label">
              Confirm Password
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              className="form-control"
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
            {errors.confirmPassword && (
              <div className="form-error">{errors.confirmPassword}</div>
            )}
          </div>

          <button
            type="submit"
            className="btn btn-primary w-100"
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account?{' '}
            <Link to="/login" className="auth-link">
              Sign in
            </Link>
          </p>
        </div>
      </div>

      <div className="auth-visual">
        <div className="visual-content">
          <h2>Advanced AI Technology</h2>
          <p>
            Our system uses state-of-the-art GAN and Vision Transformer 
            architecture for accurate DR detection.
          </p>
          <div className="visual-features">
            <div className="visual-feature">
              <span className="feature-icon">🎨</span>
              <span>GAN-based Augmentation</span>
            </div>
            <div className="visual-feature">
              <span className="feature-icon">🧠</span>
              <span>Hybrid CNN Features</span>
            </div>
            <div className="visual-feature">
              <span className="feature-icon">⚡</span>
              <span>Vision Transformer</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;

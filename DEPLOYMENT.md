# 🚀 Deployment Guide - Diabetic Retinopathy Detection System

This guide will help you deploy your application to production using free services.

## 📋 Prerequisites

- GitHub account (you already have this! ✓)
- Render account (free - we'll create this)
- Your code is already on GitHub ✓

---

## 🎯 DEPLOYMENT ARCHITECTURE

```
┌─────────────────┐         ┌──────────────────┐
│  GitHub Pages   │         │      Render      │
│   (Frontend)    │ ──────> │    (Backend)     │
│  React App      │   API   │   FastAPI + ML   │
└─────────────────┘         └──────────────────┘
```

---

## 📦 PART 1: Deploy Backend to Render (FREE)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account

### Step 2: Deploy Backend
1. Once logged in, click "New +" → "Web Service"
2. Click "Connect GitHub" and authorize Render
3. Find and select: `Diabetic-Retinopathy-Detection`
4. Configure the service:
   ```
   Name: diabetic-retinopathy-backend
   Region: Choose closest to you
   Branch: main
   Root Directory: backend
   Runtime: Docker
   Instance Type: Free
   ```

5. Add Environment Variables:
   ```
   DATABASE_URL = sqlite:///./dr_detection.db
   SECRET_KEY = your-secret-key-here-change-this
   UPLOAD_DIR = ./uploads
   ```

6. Click "Create Web Service"

### Step 3: Wait for Build
- First build takes 5-10 minutes
- Render will:
  - Build your Docker container
  - Install all dependencies
  - Start the FastAPI server
  - Give you a URL like: `https://diabetic-retinopathy-backend.onrender.com`

### Step 4: Test Backend
Once deployed, test these endpoints:
```
https://your-backend-url.onrender.com/health
https://your-backend-url.onrender.com/docs
```

---

## 🌐 PART 2: Deploy Frontend to Vercel (FREE)

### Step 1: Update Frontend API URL
Before deploying, you need to update the backend URL in your frontend:

1. Open `frontend/src/services/api.js`
2. Change this line:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000';
   ```
   To:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.onrender.com';
   ```
   (Use your actual Render URL from Part 1)

3. Commit and push:
   ```bash
   git add .
   git commit -m "Update API URL for production"
   git push origin main
   ```

### Step 2: Create Vercel Account
1. Go to https://vercel.com
2. Click "Sign Up" → Choose "GitHub"
3. Authorize Vercel to access your repositories

### Step 3: Deploy Frontend
1. Click "Add New..." → "Project"
2. Import `Diabetic-Retinopathy-Detection`
3. Configure:
   ```
   Framework Preset: Create React App
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```
4. Click "Deploy"

### Step 4: Get Your Frontend URL
- Vercel will give you a URL like: `https://diabetic-retinopathy-detection.vercel.app`
- This is your production app!

---

## 🔧 PART 3: Configure CORS (Important!)

Your backend needs to allow requests from your frontend domain.

1. Go to your Render dashboard
2. Click on your backend service
3. Go to "Environment"
4. Add or update CORS settings in your code (already configured in `app/main.py`)

The CORS is already set up in your code to accept requests from any origin. In production, you should update it:

```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-url.vercel.app",
        "http://localhost:3000"  # for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ⚠️ IMPORTANT: Model Files

Your ML model files (.h5) are NOT in the repository (they're too large). You have two options:

### Option A: Train on First Run (Automatic)
The backend is configured to train models on first startup if they don't exist. This will happen automatically on Render.

### Option B: Upload Pre-trained Models
1. Train models locally: `python train.py`
2. Upload to cloud storage (Google Drive, Dropbox, AWS S3)
3. Download them on server startup with a script

---

## 📝 DEPLOYMENT CHECKLIST

- [ ] Backend deployed to Render
- [ ] Backend URL is live and responding
- [ ] Updated frontend API_BASE_URL with Render URL
- [ ] Frontend deployed to Vercel
- [ ] Frontend can communicate with backend
- [ ] Demo user created on backend
- [ ] Models trained or uploaded
- [ ] Tested login functionality
- [ ] Tested image upload and prediction

---

## 🔍 TESTING YOUR DEPLOYMENT

1. **Visit your Vercel URL**
2. **Try to log in:**
   - Email: demo@demo.com
   - Password: Demo@123
3. **Upload a retinal image**
4. **Check prediction results**

---

## 🐛 TROUBLESHOOTING

### Backend won't start on Render
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure Dockerfile is in `backend/` directory

### Frontend can't connect to backend
- Check CORS settings
- Verify API_BASE_URL in `api.js`
- Check browser console for errors
- Ensure backend is running (visit `/health` endpoint)

### Models not loading
- Check Render logs for training progress
- May take 10-15 minutes on first deployment
- Verify model files are being created in `models_saved/`

### Database errors
- Render's free tier has ephemeral storage
- Database resets on each deploy
- Consider upgrading to persistent storage or use PostgreSQL

---

## 💰 COST BREAKDOWN

- **Render Free Tier:**
  - 750 hours/month (enough for one service)
  - Sleeps after 15 min of inactivity
  - Wakes up in <30 seconds

- **Vercel Free Tier:**
  - Unlimited deployments
  - 100GB bandwidth/month
  - Perfect for personal projects

**Total Cost: $0/month** 🎉

---

## 🚀 GOING TO PRODUCTION

For production use, consider:

1. **Upgrade to Paid Plans:**
   - Render: $7/month (always on, faster)
   - Vercel: Free tier is usually enough

2. **Add Database:**
   - PostgreSQL on Render: Free tier available
   - Or use Supabase (free PostgreSQL)

3. **Model Storage:**
   - AWS S3, Google Cloud Storage, or Azure Blob
   - Or use Git LFS for model files

4. **Custom Domain:**
   - Buy domain on Namecheap, GoDaddy, etc.
   - Connect to Vercel (easy setup)

---

## 📞 NEED HELP?

If you encounter issues:
1. Check Render/Vercel logs
2. Review the error messages
3. Ask me for help!

---

## ✅ QUICK DEPLOY COMMANDS

After you've set up Render and Vercel accounts:

```bash
# Update API URL for production
cd frontend/src/services
# Edit api.js and update API_BASE_URL

# Commit and push
git add .
git commit -m "Configure for production deployment"
git push origin main
```

Both services will auto-deploy when you push to GitHub! 🎉

---

**Your app will be live at:**
- Frontend: `https://[your-project].vercel.app`
- Backend API: `https://[your-project].onrender.com`
- API Docs: `https://[your-project].onrender.com/docs`

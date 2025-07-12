# Strategic Intelligence Reports - Web App Setup Guide

## 🚀 Complete Setup for Public Web App

This guide will help you deploy the **Strategic Intelligence Reports** web app with email signup and Stripe donations.

## 📋 Prerequisites

### Required Accounts & Credentials
1. **MongoDB Atlas Account** (free tier available)
2. **Stripe Account** (for $5 donations)
3. **Deployment Accounts**:
   - Vercel (for frontend)
   - Railway/Render (for backend)

## 🔧 Environment Setup

### 1. MongoDB Configuration

**Create MongoDB Atlas Database:**
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create new project: "Strategic Intelligence"
3. Create cluster (free M0 tier)
4. Create database user with read/write permissions
5. Add your IP to network access list
6. Get connection string

**Connection String Format:**
```
mongodb+srv://username:password@cluster.mongodb.net/strategic-intelligence
```

### 2. Stripe Configuration

**Setup Stripe Account:**
1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Get your API keys:
   - Publishable key: `pk_test_...`
   - Secret key: `sk_test_...`
3. Configure webhook endpoint (for production)

## 📁 Backend Deployment

### 1. Install Dependencies
```bash
cd backend
npm install
```

### 2. Environment Variables
Create `/backend/.env`:
```env
# MongoDB
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/strategic-intelligence

# Stripe
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here

# Server
PORT=3001
NODE_ENV=production
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

### 3. Deploy Backend (Railway)

**Option A: Railway (Recommended)**
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Deploy: `railway up`
4. Set environment variables in Railway dashboard

**Option B: Render**
1. Connect GitHub repo to Render
2. Set build command: `npm install`
3. Set start command: `npm start`
4. Add environment variables

### 4. Backend API Endpoints

Once deployed, your backend will have:
- Health: `GET /api/health`
- Subscribe: `POST /api/subscribe`
- Unsubscribe: `POST /api/unsubscribe`
- Get subscribers: `GET /api/active`
- Create donation: `POST /api/donations/create-checkout-session`
- Statistics: `GET /api/stats`

## 🌐 Frontend Deployment

### 1. Install Dependencies
```bash
cd frontend/strategic-intelligence
npm install
```

### 2. Update API URLs
Create `/frontend/strategic-intelligence/.env.production`:
```env
REACT_APP_API_URL=https://your-backend-domain.railway.app/api
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
```

### 3. Build & Deploy (Vercel)

**Automatic Deployment:**
1. Connect GitHub repo to Vercel
2. Import project from `/frontend/strategic-intelligence`
3. Set build settings:
   - Build command: `npm run build`
   - Output directory: `build`
4. Add environment variables
5. Deploy

**Manual Deployment:**
```bash
npm run build
npx vercel --prod
```

## 🔗 Python Integration

### 1. Update Python Environment
Add to your Python `.env`:
```env
# Web Subscriber Integration
WEB_API_URL=https://your-backend-domain.railway.app/api
```

### 2. Test Integration
```bash
python3 -c "
from src.inoreader_intelligence.web_subscribers import WebSubscriberManager
from src.inoreader_intelligence.config import Config
manager = WebSubscriberManager(Config.from_env())
manager.test_connection()
print(f'Web subscribers: {len(manager.get_web_subscribers())}')
"
```

### 3. Run with Combined Recipients
```bash
python3 -c "
from src.inoreader_intelligence import InoreaderIntelligence
app = InoreaderIntelligence()
app.setup()
report = app.generate_report(send_email=True)
print(f'Report sent: {report}')
"
```

## 📧 Email Flow Integration

### How It Works:
1. **Web users** subscribe via the web app → Stored in MongoDB
2. **Python app** fetches web subscribers via API
3. **Combined recipients** = Config emails + Web subscribers
4. **Daily reports** sent to everyone at 06:00 SGT

### Email Recipients:
- **Config recipients**: Your personal emails from `.env`
- **Web subscribers**: Public signups from the website
- **Deduplication**: No duplicate emails sent

## 💳 Donation Flow

### User Experience:
1. User visits website and reads about the service
2. Optional donation prompt with $5 suggestion
3. Stripe checkout for secure payment
4. Success/failure handling
5. Users can proceed with free service regardless

### Revenue Tracking:
- All donations stored in MongoDB
- Statistics available via `/api/donations/stats`
- Stripe handles payment processing

## 🚀 Final Steps

### 1. Test Complete Flow
```bash
# Test frontend
curl https://your-frontend.vercel.app

# Test backend
curl https://your-backend.railway.app/api/health

# Test email subscription
curl -X POST https://your-backend.railway.app/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'

# Test Python integration
python3 run_example.py
```

### 2. Production Checklist
- ✅ MongoDB Atlas connected
- ✅ Stripe keys configured
- ✅ Frontend deployed on Vercel
- ✅ Backend deployed on Railway
- ✅ Python app updated with web API URL
- ✅ Daily scheduler running with combined recipients
- ✅ Domain configured (optional)

### 3. Monitoring
- **Frontend**: Vercel analytics
- **Backend**: Railway logs
- **Database**: MongoDB Atlas monitoring
- **Payments**: Stripe dashboard
- **Python logs**: Server monitoring

## 🔒 Security Notes

- All API keys stored as environment variables
- CORS configured for frontend domain only
- Rate limiting on API endpoints
- Input validation and sanitization
- HTTPS enforced in production

## 🆘 Troubleshooting

### Common Issues:

1. **CORS errors**: Check `FRONTEND_URL` in backend `.env`
2. **MongoDB connection**: Verify connection string and network access
3. **Stripe errors**: Check API keys and webhook configuration
4. **Email integration**: Verify `WEB_API_URL` in Python `.env`

### Debug Commands:
```bash
# Check backend logs
railway logs

# Check database connection
node -e "require('mongoose').connect(process.env.MONGODB_URI).then(() => console.log('MongoDB OK'))"

# Test Python API connection
python3 -c "from src.inoreader_intelligence.web_subscribers import WebSubscriberManager; from src.inoreader_intelligence.config import Config; WebSubscriberManager(Config.from_env()).test_connection()"
```

## 📊 Success Metrics

Once deployed, you'll have:
- 📈 **Public web presence** for Strategic Intelligence Reports
- 📧 **Automated email collection** from interested users
- 💰 **Optional donation system** to support costs
- 🔗 **Seamless integration** with existing Python system
- 📱 **Professional landing page** explaining your service

**Your users will receive the same high-quality intelligence reports whether they signed up via web or were added manually!**
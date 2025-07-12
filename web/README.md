# 📬 Strategic Intelligence Email Collector

A minimalist web application for collecting email subscriptions with MongoDB storage and secure deployment.

## 🚀 Features

- ✅ Clean, responsive email collection form
- ✅ MongoDB Atlas integration with Mongoose ODM
- ✅ Rate limiting and security middleware
- ✅ Buy Me a Coffee donation integration
- ✅ Real-time form validation
- ✅ Success/error messaging with animations
- ✅ Duplicate email detection
- ✅ Production-ready deployment configuration

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Node.js, Express.js
- **Database**: MongoDB Atlas
- **Security**: Helmet, CORS, Rate Limiting
- **Deployment**: Vercel-ready configuration

## 📦 Installation

1. **Clone and navigate to the web directory**:
   ```bash
   cd web
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your MongoDB connection string:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/strategic-intelligence
   PORT=3000
   NODE_ENV=development
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser**:
   Navigate to `http://localhost:3000`

## 🌐 Deployment

### Vercel Deployment

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel
   ```

3. **Set environment variables in Vercel dashboard**:
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `NODE_ENV`: production

### Other Platforms

The app is also compatible with:
- **Render**: Use `npm start` as start command
- **Railway**: Auto-detects Node.js apps
- **DigitalOcean App Platform**: Use the provided `package.json` scripts

## 📊 API Endpoints

### POST `/api/submit-email`
Submit a new email subscription.

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response (Success)**:
```json
{
  "success": true,
  "message": "Successfully subscribed to Strategic Intelligence updates!",
  "data": {
    "email": "user@example.com",
    "submitted_at": "2025-07-12T10:30:00Z",
    "status": "active"
  }
}
```

### GET `/api/stats`
Get subscription statistics (optional admin endpoint).

### GET `/api/health`
Health check endpoint.

## 🔒 Security Features

- **Rate Limiting**: 5 requests per 15 minutes per IP
- **Input Validation**: Email format validation and sanitization
- **CORS Protection**: Configurable origin restrictions
- **Security Headers**: Helmet.js integration
- **Error Handling**: No sensitive data leakage

## 📱 MongoDB Schema

```javascript
{
  email: String (required, unique, lowercase),
  submitted_at: Date,
  ip_address: String,
  user_agent: String,
  source: String (default: 'web_form'),
  status: String (active|unsubscribed|bounced)
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | Required |
| `PORT` | Server port | 3000 |
| `NODE_ENV` | Environment | development |
| `RATE_LIMIT_WINDOW_MS` | Rate limit window | 900000 (15 min) |
| `RATE_LIMIT_MAX_REQUESTS` | Max requests per window | 5 |

### Rate Limiting

Adjust rate limiting in `.env`:
```
RATE_LIMIT_WINDOW_MS=900000  # 15 minutes
RATE_LIMIT_MAX_REQUESTS=5    # 5 requests per window
```

## 🎨 Customization

### Styling
Edit `public/styles.css` to customize the appearance.

### Form Behavior
Modify `public/script.js` for different form interactions.

### Email Schema
Update `models/Email.js` to add additional fields.

## 📈 Integration with Intelligence Reports

The PRD mentions updating the intelligence web_subscribers.py to pull emails directly from MongoDB:

```python
# Example integration
from pymongo import MongoClient

client = MongoClient(MONGODB_URI)
db = client['strategic-intelligence']
emails_collection = db['emails']

# Get active subscribers
active_subscribers = emails_collection.find({'status': 'active'})
email_list = [doc['email'] for doc in active_subscribers]
```

## 🐛 Troubleshooting

### MongoDB Connection Issues
- Verify your MongoDB URI format
- Check network access in MongoDB Atlas
- Ensure IP whitelist includes your deployment platform

### Rate Limiting
- Adjust `RATE_LIMIT_WINDOW_MS` and `RATE_LIMIT_MAX_REQUESTS`
- Clear browser cache if testing repeatedly

### CORS Errors
- Update `corsOptions` in `server.js` with your domain
- Check browser network tab for specific CORS issues

## 📄 License

MIT License - feel free to use for your own projects!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ☕ Support

If you find this useful, consider supporting the project:
[Buy Me a Coffee](https://coff.ee/p0oh)
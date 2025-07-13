import mongoose from 'mongoose';

// Email schema - inline since we can't import modules in serverless functions easily
const emailSchema = new mongoose.Schema({
    email: {
        type: String,
        required: [true, 'Email is required'],
        unique: true,
        lowercase: true,
        trim: true,
        validate: {
            validator: function(email) {
                return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
            },
            message: 'Please provide a valid email address'
        }
    },
    submitted_at: {
        type: Date,
        default: Date.now
    },
    ip_address: {
        type: String,
        default: null
    },
    user_agent: {
        type: String,
        default: null
    },
    source: {
        type: String,
        default: 'web_form'
    },
    status: {
        type: String,
        enum: ['active', 'unsubscribed', 'bounced'],
        default: 'active'
    }
}, {
    timestamps: true
});

// Create model
const Email = mongoose.models.Email || mongoose.model('Email', emailSchema);

// Rate limiting store (in-memory for serverless)
const rateLimitStore = new Map();

// Rate limiting function
function checkRateLimit(ip) {
    const now = Date.now();``
    const windowMs = parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000; // 15 minutes
    const maxRequests = parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 5;
    
    if (!rateLimitStore.has(ip)) {
        rateLimitStore.set(ip, []);
    }
    
    const requests = rateLimitStore.get(ip);
    
    // Remove old requests outside the window
    const validRequests = requests.filter(time => now - time < windowMs);
    
    if (validRequests.length >= maxRequests) {
        return false; // Rate limit exceeded
    }
    
    // Add current request
    validRequests.push(now);
    rateLimitStore.set(ip, validRequests);
    
    return true; // Within rate limit
}

// MongoDB connection
let isConnected = false;

async function connectToDatabase() {
    if (isConnected) {
        return;
    }

    if (!process.env.MONGODB_URI) {
        throw new Error('MONGODB_URI environment variable is required');
    }

    try {
        const options = {
            maxPoolSize: 5,
            serverSelectionTimeoutMS: 10000,
            socketTimeoutMS: 30000,
            bufferCommands: false,
            maxIdleTimeMS: 30000,
            retryWrites: true,
            w: 'majority'
        };

        await mongoose.connect(process.env.MONGODB_URI, options);
        isConnected = true;
        console.log('✅ Connected to MongoDB');
    } catch (error) {
        console.error('❌ MongoDB connection error:', error);
        throw error;
    }
}

export default async function handler(req, res) {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');

    // Handle preflight requests
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    // Only allow POST requests
    if (req.method !== 'POST') {
        return res.status(405).json({
            error: 'Method not allowed',
            code: 'METHOD_NOT_ALLOWED'
        });
    }

    try {
        console.log('📨 Email submission request received');
        console.log('Headers:', req.headers);
        console.log('Body:', req.body);

        // Get client IP for rate limiting
        const clientIP = req.headers['x-forwarded-for'] || 
                        req.headers['x-real-ip'] || 
                        req.connection?.remoteAddress || 
                        'unknown';

        // Check rate limit
        if (!checkRateLimit(clientIP)) {
            console.log(`❌ Rate limit exceeded for IP: ${clientIP}`);
            return res.status(429).json({
                error: 'Too many email submissions from this IP, please try again later.',
                code: 'RATE_LIMIT_EXCEEDED'
            });
        }

        const { email } = req.body;

        // Validate input
        if (!email) {
            console.log('❌ Email validation failed: missing email');
            return res.status(400).json({
                error: 'Email address is required',
                code: 'EMAIL_REQUIRED'
            });
        }

        // Additional email format validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            console.log('❌ Email validation failed: invalid format');
            return res.status(400).json({
                error: 'Please provide a valid email address',
                code: 'INVALID_EMAIL_FORMAT'
            });
        }

        // Connect to database
        await connectToDatabase();

        // Get client info for logging
        const clientInfo = {
            ip_address: clientIP,
            user_agent: req.headers['user-agent'] || null
        };

        // Create new email subscription
        const newEmail = new Email({
            email: email.toLowerCase().trim(),
            ...clientInfo
        });

        // Save to database
        await newEmail.save();

        // Log successful subscription
        console.log(`✅ New subscription: ${email} from IP: ${clientInfo.ip_address}`);

        // Return success response
        return res.status(201).json({
            success: true,
            message: 'Successfully subscribed to Strategic Intelligence updates!',
            data: {
                email: newEmail.email,
                submitted_at: newEmail.submitted_at,
                status: newEmail.status
            }
        });

    } catch (error) {
        console.error('Email submission error:', error);

        // Handle duplicate email error
        if (error.code === 11000) {
            return res.status(409).json({
                error: 'This email is already subscribed to our updates',
                code: 'EMAIL_ALREADY_EXISTS'
            });
        }

        // Handle validation errors
        if (error.name === 'ValidationError') {
            const validationErrors = Object.values(error.errors).map(err => err.message);
            return res.status(400).json({
                error: validationErrors[0] || 'Invalid email format',
                code: 'VALIDATION_ERROR'
            });
        }

        // Handle other errors
        return res.status(500).json({
            error: 'Internal server error. Please try again later.',
            code: 'INTERNAL_ERROR'
        });
    }
}
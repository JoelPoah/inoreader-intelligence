import mongoose from 'mongoose';

// Email schema
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
        console.log('✅ Connected to MongoDB for stats');
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

    // Only allow GET requests
    if (req.method !== 'GET') {
        return res.status(405).json({
            error: 'Method not allowed',
            code: 'METHOD_NOT_ALLOWED'
        });
    }

    try {
        // Connect to database
        await connectToDatabase();

        const stats = {
            total_subscribers: await Email.countDocuments({ status: 'active' }),
            total_all_time: await Email.countDocuments(),
            recent_subscriptions: await Email.find({ status: 'active' })
                .sort({ submitted_at: -1 })
                .limit(5)
                .select('email submitted_at -_id')
        };

        return res.status(200).json({
            success: true,
            data: stats
        });
    } catch (error) {
        console.error('Stats error:', error);
        return res.status(500).json({
            error: 'Failed to fetch statistics',
            code: 'STATS_ERROR'
        });
    }
}
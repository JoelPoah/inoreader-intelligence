const mongoose = require('mongoose');

const donationSchema = new mongoose.Schema({
  stripePaymentIntentId: {
    type: String,
    required: true,
    unique: true
  },
  stripeCustomerId: {
    type: String,
    required: false
  },
  amount: {
    type: Number,
    required: true,
    min: [100, 'Minimum donation is $1.00'] // Amount in cents
  },
  currency: {
    type: String,
    default: 'usd',
    uppercase: true
  },
  status: {
    type: String,
    enum: ['pending', 'succeeded', 'failed', 'canceled'],
    default: 'pending'
  },
  donorEmail: {
    type: String,
    required: false,
    lowercase: true
  },
  donorName: {
    type: String,
    required: false
  },
  message: {
    type: String,
    maxLength: 500
  },
  metadata: {
    ipAddress: String,
    userAgent: String,
    source: {
      type: String,
      default: 'website'
    }
  }
}, {
  timestamps: true
});

// Index for faster queries
donationSchema.index({ stripePaymentIntentId: 1 });
donationSchema.index({ status: 1 });
donationSchema.index({ createdAt: -1 });

// Static method to get total donations
donationSchema.statics.getTotalDonations = function() {
  return this.aggregate([
    { $match: { status: 'succeeded' } },
    { $group: { _id: null, total: { $sum: '$amount' }, count: { $sum: 1 } } }
  ]);
};

// Static method to get recent donations
donationSchema.statics.getRecentDonations = function(limit = 10) {
  return this.find({ status: 'succeeded' })
    .sort({ createdAt: -1 })
    .limit(limit)
    .select('amount donorName createdAt message');
};

module.exports = mongoose.model('Donation', donationSchema);
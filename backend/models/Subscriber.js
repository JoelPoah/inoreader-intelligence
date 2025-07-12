const mongoose = require('mongoose');
const validator = require('validator');

const subscriberSchema = new mongoose.Schema({
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    validate: [validator.isEmail, 'Please provide a valid email address']
  },
  subscriptionDate: {
    type: Date,
    default: Date.now
  },
  isActive: {
    type: Boolean,
    default: true
  },
  source: {
    type: String,
    enum: ['website', 'manual', 'api'],
    default: 'website'
  },
  metadata: {
    ipAddress: String,
    userAgent: String,
    referrer: String
  }
}, {
  timestamps: true
});

// Index for faster queries
subscriberSchema.index({ email: 1 });
subscriberSchema.index({ isActive: 1 });
subscriberSchema.index({ subscriptionDate: -1 });

// Static method to get active subscribers
subscriberSchema.statics.getActiveSubscribers = function() {
  return this.find({ isActive: true }).select('email subscriptionDate');
};

// Static method to get subscriber count
subscriberSchema.statics.getSubscriberCount = function() {
  return this.countDocuments({ isActive: true });
};

// Instance method to unsubscribe
subscriberSchema.methods.unsubscribe = function() {
  this.isActive = false;
  return this.save();
};

module.exports = mongoose.model('Subscriber', subscriberSchema);
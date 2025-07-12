const express = require('express');
const router = express.Router();
const Subscriber = require('../models/Subscriber');

// Subscribe endpoint
router.post('/subscribe', async (req, res) => {
  try {
    const { email } = req.body;

    if (!email) {
      return res.status(400).json({ 
        success: false, 
        message: 'Email address is required' 
      });
    }

    // Check if already subscribed
    const existingSubscriber = await Subscriber.findOne({ email: email.toLowerCase() });
    
    if (existingSubscriber) {
      if (existingSubscriber.isActive) {
        return res.status(400).json({ 
          success: false, 
          message: 'Email address is already subscribed' 
        });
      } else {
        // Reactivate if previously unsubscribed
        existingSubscriber.isActive = true;
        existingSubscriber.subscriptionDate = new Date();
        await existingSubscriber.save();
        
        return res.status(200).json({ 
          success: true, 
          message: 'Successfully resubscribed! You\'ll receive your next report at 06:00 SGT.' 
        });
      }
    }

    // Create new subscriber
    const subscriber = new Subscriber({
      email: email.toLowerCase(),
      metadata: {
        ipAddress: req.ip,
        userAgent: req.get('User-Agent'),
        referrer: req.get('Referer')
      }
    });

    await subscriber.save();

    res.status(201).json({ 
      success: true, 
      message: 'Successfully subscribed! You\'ll receive your first report tomorrow at 06:00 SGT.' 
    });

  } catch (error) {
    console.error('Subscription error:', error);
    
    if (error.code === 11000) {
      return res.status(400).json({ 
        success: false, 
        message: 'Email address is already subscribed' 
      });
    }

    if (error.name === 'ValidationError') {
      return res.status(400).json({ 
        success: false, 
        message: error.message 
      });
    }

    res.status(500).json({ 
      success: false, 
      message: 'Internal server error. Please try again later.' 
    });
  }
});

// Unsubscribe endpoint
router.post('/unsubscribe', async (req, res) => {
  try {
    const { email } = req.body;

    if (!email) {
      return res.status(400).json({ 
        success: false, 
        message: 'Email address is required' 
      });
    }

    const subscriber = await Subscriber.findOne({ email: email.toLowerCase() });
    
    if (!subscriber) {
      return res.status(404).json({ 
        success: false, 
        message: 'Email address not found' 
      });
    }

    await subscriber.unsubscribe();

    res.status(200).json({ 
      success: true, 
      message: 'Successfully unsubscribed from Strategic Intelligence Reports' 
    });

  } catch (error) {
    console.error('Unsubscribe error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Internal server error. Please try again later.' 
    });
  }
});

// Get active subscribers (for Python integration)
router.get('/active', async (req, res) => {
  try {
    const subscribers = await Subscriber.getActiveSubscribers();
    const emails = subscribers.map(sub => sub.email);
    
    res.status(200).json({ 
      success: true, 
      count: emails.length,
      emails 
    });
  } catch (error) {
    console.error('Get subscribers error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to retrieve subscribers' 
    });
  }
});

// Get subscriber statistics
router.get('/stats', async (req, res) => {
  try {
    const totalCount = await Subscriber.getSubscriberCount();
    const recentSubs = await Subscriber.find({ isActive: true })
      .sort({ subscriptionDate: -1 })
      .limit(5)
      .select('email subscriptionDate');

    res.status(200).json({ 
      success: true, 
      totalSubscribers: totalCount,
      recentSubscriptions: recentSubs 
    });
  } catch (error) {
    console.error('Stats error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to retrieve statistics' 
    });
  }
});

module.exports = router;
const express = require('express');
const router = express.Router();
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const Donation = require('../models/Donation');

// Create checkout session for donation
router.post('/create-checkout-session', async (req, res) => {
  try {
    const { amount = 5 } = req.body; // Default $5 donation
    
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency: 'usd',
            product_data: {
              name: 'Strategic Intelligence Reports Support',
              description: 'Help maintain free AI-powered military intelligence briefings',
              images: ['https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=400&fit=crop'],
            },
            unit_amount: amount * 100, // Convert to cents
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `${process.env.FRONTEND_URL}/donation-success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.FRONTEND_URL}/donation-cancelled`,
      metadata: {
        source: 'website',
        amount: amount.toString()
      }
    });

    res.json({ url: session.url });
  } catch (error) {
    console.error('Stripe session error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to create donation session' 
    });
  }
});

// Handle successful donation
router.post('/donation-success', async (req, res) => {
  try {
    const { session_id } = req.body;
    
    if (!session_id) {
      return res.status(400).json({ 
        success: false, 
        message: 'Session ID is required' 
      });
    }

    const session = await stripe.checkout.sessions.retrieve(session_id);
    
    if (session.payment_status === 'paid') {
      // Record donation in database
      const donation = new Donation({
        stripePaymentIntentId: session.payment_intent,
        stripeCustomerId: session.customer,
        amount: session.amount_total,
        currency: session.currency,
        status: 'succeeded',
        donorEmail: session.customer_details?.email,
        donorName: session.customer_details?.name,
        metadata: {
          source: 'website',
          ipAddress: req.ip,
          userAgent: req.get('User-Agent')
        }
      });

      await donation.save();

      res.status(200).json({ 
        success: true, 
        message: 'Thank you for your support!',
        donation: {
          amount: session.amount_total / 100,
          currency: session.currency
        }
      });
    } else {
      res.status(400).json({ 
        success: false, 
        message: 'Payment was not successful' 
      });
    }
  } catch (error) {
    console.error('Donation success error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to process donation confirmation' 
    });
  }
});

// Stripe webhook for payment events
router.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

  let event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object;
      
      try {
        await Donation.findOneAndUpdate(
          { stripePaymentIntentId: paymentIntent.id },
          { status: 'succeeded' },
          { new: true }
        );
        console.log('Payment succeeded:', paymentIntent.id);
      } catch (error) {
        console.error('Failed to update donation status:', error);
      }
      break;

    case 'payment_intent.payment_failed':
      const failedPayment = event.data.object;
      
      try {
        await Donation.findOneAndUpdate(
          { stripePaymentIntentId: failedPayment.id },
          { status: 'failed' },
          { new: true }
        );
        console.log('Payment failed:', failedPayment.id);
      } catch (error) {
        console.error('Failed to update donation status:', error);
      }
      break;

    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  res.json({ received: true });
});

// Get donation statistics
router.get('/stats', async (req, res) => {
  try {
    const stats = await Donation.getTotalDonations();
    const recentDonations = await Donation.getRecentDonations(5);
    
    const totalAmount = stats.length > 0 ? stats[0].total / 100 : 0;
    const totalCount = stats.length > 0 ? stats[0].count : 0;

    res.status(200).json({
      success: true,
      totalAmount,
      totalCount,
      recentDonations: recentDonations.map(donation => ({
        amount: donation.amount / 100,
        donorName: donation.donorName || 'Anonymous',
        date: donation.createdAt,
        message: donation.message
      }))
    });
  } catch (error) {
    console.error('Donation stats error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to retrieve donation statistics' 
    });
  }
});

module.exports = router;
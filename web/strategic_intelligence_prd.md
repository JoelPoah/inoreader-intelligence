# 📬 Strategic Intelligence Email Collector – Project Requirement Document (PRD)

## 🧠 Logical Thinking – What We Want to Build

### Purpose
To build a minimalist and easily deployable web app that collects a user's email address and stores it securely in a MongoDB database. It serves as a simple lead-capture system for future updates, reports, or newsletters.

### Key Goals
- Collect user emails with a simple input form.
- Store emails in a MongoDB Atlas database.
- Include a “Buy Me a Coffee” donation button to support the project: [https://coff.ee/p0oh](https://coff.ee/p0oh).
- Host the app with minimal infrastructure (e.g., Vercel, Render, or DigitalOcean).

---

## 📊 Analytical Thinking – Skills & Tools Required

### Core Skills

#### Web Development
- Basic HTML/CSS and frontend form handling
- Minimal JavaScript or frontend framework (e.g., React/Vue optional)
- Backend integration with Node.js, Express, or Flask

#### Database Integration
- MongoDB Atlas configuration and connection
- MongoDB URI security practices
- Email document schema creation

#### Deployment & Hosting
- Deployment to a cloud platform (e.g., Vercel, Render, Heroku)
- Environment variable management (for MongoDB URI)
- HTTPS and CORS configuration

#### Optional Enhancements
- Form validation
- Email deduplication
- Admin dashboard (future upgrade)

---

## 🧮 Computational Thinking – Key Features & System Design

### Key Features

- ✅ **Email Input Form**
  - A single input field for users to submit their email
  - Simple submit button

- ✅ **Database Save**
  - On submission, email is POSTed to a backend API
  - Stored in MongoDB with a timestamp

- ✅ **Buy Me a Coffee Button**
  - Embedded prominently below the form
  - Uses: [https://coff.ee/p0oh](https://coff.ee/p0oh)

- ✅ **Success Feedback**
  - “Thank you” message or animation after submission

### Architecture Overview

```plaintext
User Browser
   |
   v
Frontend (HTML/CSS/JS)
   |
   v
Backend API (Node.js or Flask)
   |
   v
MongoDB Atlas (strategic-intelligence)
```

---

## 🔁 Procedural Thinking – Detailed Steps & Processes

### 1. **Frontend Form**
- Simple HTML or framework-based page with:
  - Email input field (`<input type="email">`)
  - Submit button
  - "Buy Me a Coffee" button (link to https://coff.ee/p0oh)

### 2. **Backend Setup**
- Node.js + Express or Flask backend
- POST route `/submit-email`
  - Receives email from form
  - Validates and checks format
  - Connects to MongoDB and inserts email with timestamp

### 3. **MongoDB Integration**
- MongoDB URI:
  ```
  mongodb+srv://Wolfteam111:Wolfteam111@atlascluster.sfflokd.mongodb.net/strategic-intelligence
  ```
- Use Mongoose (Node.js) or PyMongo (Flask) to connect
- Create a simple schema:
  ```json
  {
    "email": "user@example.com",
    "submitted_at": "2025-07-11T08:00:00Z"
  }
  ```

  The Inoreader intelligence web_subscribers.py should then be changed to directly pull the emails from the MongoDB database instead of an api call change that.

### 4. **Security Measures**
- Store MongoDB URI in `.env` file, never hardcoded
- Sanitize input and use rate limiting if exposed publicly
- Use HTTPS (especially when deployed)

### 5. **Deployment**
- Push code to GitHub
- Deploy to:
  - Vercel (static + serverless functions)
  - Render or Railway (Node backend)
- Set environment variables in dashboard

### 6. **User Experience**
- Minimal UI with:
  - Friendly message after submission
  - Optional animation or checkmark
- Error message if email invalid or submission fails

---

## ✅ Example HTML Snippet

```html
<form id="email-form" action="/submit-email" method="POST">
  <label for="email">Subscribe for updates:</label><br>
  <input type="email" id="email" name="email" required>
  <button type="submit">Submit</button>
</form>

<br>

<a href="https://coff.ee/p0oh" target="_blank">
  <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me a Coffee" style="height:40px;">
</a>
```

---

## 🛠️ Next Steps

1. Set up Git repository
2. Create frontend and backend boilerplate
3. Test MongoDB connection with secure `.env`
4. Deploy to Vercel or Render
5. Launch and monitor submissions
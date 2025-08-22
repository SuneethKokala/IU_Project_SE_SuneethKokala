# SafeRoute Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Heroku (Recommended)

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Or download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Initialize Git Repository**
   ```bash
   cd "women-safety-map 3"
   git init
   git add .
   git commit -m "Initial commit - SafeRoute Women Safety Map"
   ```

4. **Create Heroku App**
   ```bash
   heroku create saferoute-women-safety
   # Or use your preferred app name
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set TWILIO_ACCOUNT_SID=your_twilio_sid
   heroku config:set TWILIO_AUTH_TOKEN=your_twilio_token
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Open Your App**
   ```bash
   heroku open
   ```

### Option 2: Railway

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

### Option 3: Render

1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new Web Service
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`

## 🔧 Environment Variables

Set these in your deployment platform:

```
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

## 📱 Post-Deployment Setup

1. **Test the deployment** - Visit your app URL
2. **Configure Twilio WhatsApp** - Set up WhatsApp sandbox
3. **Update Google Maps API** - Ensure API key works in production
4. **Test emergency features** - Verify WhatsApp alerts work

## 🌐 Your App Will Be Live At:
- Heroku: `https://your-app-name.herokuapp.com`
- Railway: `https://your-app-name.up.railway.app`
- Render: `https://your-app-name.onrender.com`

## 🔒 Security Notes

- Never commit API keys to Git
- Use environment variables for all secrets
- Enable HTTPS in production
- Consider adding rate limiting for API endpoints

## 📊 Monitoring

- Check app logs: `heroku logs --tail`
- Monitor performance in platform dashboard
- Set up alerts for downtime

## 🚨 Emergency Contact Setup

After deployment, update the admin phone number in `app.py`:
```python
admin_number = '+your_admin_number'
```

Your SafeRoute Women Safety Map is now ready for production! 🛡️
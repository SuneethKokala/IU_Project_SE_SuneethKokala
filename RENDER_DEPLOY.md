# 🚀 Deploy SafeRoute to Render

## Step 1: Push to GitHub

```bash
cd "women-safety-map 3"
git add .
git commit -m "SafeRoute Women Safety Map - Ready for Render"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/saferoute-women-safety.git
git push -u origin main
```

## Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)**
2. **Sign up/Login** with GitHub
3. **Click "New +"** → **"Web Service"**
4. **Connect Repository**: Select your GitHub repo
5. **Configure Service**:
   - **Name**: `saferoute-women-safety`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

## Step 3: Set Environment Variables

In Render dashboard, add these environment variables:

```
TWILIO_ACCOUNT_SID = your_twilio_account_sid
TWILIO_AUTH_TOKEN = your_twilio_auth_token
```

## Step 4: Deploy

Click **"Create Web Service"** - Render will automatically deploy!

## 🌐 Your Live URL

Your app will be available at:
`https://saferoute-women-safety.onrender.com`

## ✅ Post-Deployment Checklist

- [ ] Test the live URL
- [ ] Verify emergency WhatsApp alerts work
- [ ] Test route calculations
- [ ] Check live tracking features
- [ ] Confirm all modals and forms work

## 🔧 Troubleshooting

- **Build fails**: Check requirements.txt
- **App crashes**: Check logs in Render dashboard
- **WhatsApp not working**: Verify Twilio credentials

Your SafeRoute Women Safety Map is now LIVE! 🛡️
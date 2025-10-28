# Womap
A local safety navigation application with AI powered route analysis and emergency features.

1. # Install Dependencies
   '''bash
   pip install -r requirements.txt
   '''

2. # Start MongoDB
   '''bash
   brew services start mongodb-community
   '''

3. # Run Application
   '''bash
   python3 start.py
   '''

# Features

- Interactive safety map
- AI powered route analysis
- Emergency alert system
- Admin dashboard with PostgreSQL data
- Live journey tracking
- Safety reviews and reports


# Project Structure

'''
women-safety-map/
├── app.py              # Main Flask application
├── database.py         # MongoDB connection
├── model.py           # AI safety predictions
├── live_tracking.py    # Journey tracking system
├── start.py           # Localhost startup script
├── templates/         # HTML templates
├── static/           # CSS and assets
└── requirements.txt  # Python dependencies
'''

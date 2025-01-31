from flask import Flask
import main as application  # Import your Flask app

# Vercel requires a WSGI application
app = application

# For local development
if __name__ == "__main__":
    app.run()
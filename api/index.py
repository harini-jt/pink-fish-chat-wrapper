"""
Vercel serverless function entry point
"""
from backend_code.main import app

# Export the app for Vercel
handler = app

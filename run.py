import os
from app import create_app

# Create the app instance using the create_app function
app = create_app()

if __name__ == "__main__":
    # Run the app in debug mode for development purposes
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port)
    

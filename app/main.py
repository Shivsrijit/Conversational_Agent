import sys
import os
sys.path.append(os.path.dirname(__file__))

from routes import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
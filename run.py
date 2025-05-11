# run.py - Updated for app within app folder
from app.app import app

if __name__ == '__main__':
    # The initialize function should be handled inside app.py
    app.run(debug=True)
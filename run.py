import os
import sys

from app import create_app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_API_ENV', 'development'))

    if len(sys.argv) < 2:
        port = 5000
    else:
        port = sys.argv[1]
    app.run(port=port)

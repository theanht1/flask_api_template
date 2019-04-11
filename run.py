import os
from app import create_app

if __name__ == '__main__':
    app = create_app(os.environ.get('SEO_PLATFORM_CONFIG', 'development'))

    app.run()

activate_this = '/var/www/bins.artifactual.co.uk/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/var/www/bins.artifactual.co.uk/source')
from app import app as application

if __name__ == '__main__':
    application.run()

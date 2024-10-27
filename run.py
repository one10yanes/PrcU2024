from app import app

import sys
import os

# Agregar la ruta de app al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))


if __name__ == '__main__':
    app.run(debug=True)

from app.config import app
from app.config.database_config import create_table

create_table()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
from flask_script import Server, Manager
from app import create_app

app = create_app()
app.config['DEBUG'] = True
manager = Manager(app)
manager.add_command("runserver", Server(host='127.0.0.1', port=5000, use_debugger=True))

if __name__ == "__main__":
   manager.run()
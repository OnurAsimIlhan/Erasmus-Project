from website import create_app
import os

app = create_app()

# Run Server
if __name__ == "__main__":
    app.run()

os.rmdir("instance")
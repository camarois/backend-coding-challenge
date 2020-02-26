import src.api.server as server

flask_app = server.create_app()

def main():
    flask_app.run()


if __name__ == '__main__':
    main()

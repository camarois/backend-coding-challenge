import src.web.server as server

app = server.create_app()


def main():
    app.run()


if __name__ == '__main__':
    main()

import connexion


def main():
    app = connexion.App(__name__, specification_dir="/app/swagger")
    app.add_api('api.yml', strict_validation=True)
    app.run(port=8080)


if __name__ == "__main__":
    main()

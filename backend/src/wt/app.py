import os
import connexion
from wt.loader import load_components


def main():
    app = connexion.App(__name__, specification_dir="/app/swagger")
    app.add_api('api.yml', strict_validation=True, validate_responses=True)
    db_url = os.environ.get("DB_URL")
    load_components(db_url)

    app.run(port=8080)


if __name__ == "__main__":
    main()

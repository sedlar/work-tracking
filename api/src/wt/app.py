import argparse
import os
import sys

import connexion
from flask_injector import FlaskInjector

from wt.commands.add_user import command_add_user
from wt.loader import configure_with_engine, prepare_db


def setup_debugger_from_env():
    if os.environ.get("REMOTE_DEBUGGER"):
        import pydevd
        pydevd.settrace(
            '172.17.0.1',
            port=9999,
            stdoutToServer=True,
            stderrToServer=True,
            suspend=False
        )


def main(argv):
    setup_debugger_from_env()
    parser = get_arg_parser()
    args = parser.parse_args(argv)

    db_url = os.environ.get("DB_URL")
    engine = prepare_db(db_url)

    if args.command == "run-server":
        app = create_app(engine)
        app.run(port=args.listen_port)
    elif args.command == "add-user":
        command_add_user(engine, args.username, args.password)
    else:
        raise ValueError("Unknown command")


def create_app(engine):
    app = connexion.App(__name__, specification_dir="/app/swagger")
    app.add_api('api.yml', strict_validation=True, validate_responses=True)
    FlaskInjector(app=app.app, modules=[configure_with_engine(engine)])
    return app


def get_arg_parser():
    parser = argparse.ArgumentParser(description="Work Tracking")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    run_server = subparsers.add_parser("run-server")
    run_server.add_argument("--listen-port", default=8080, type=int)
    added_parser = subparsers.add_parser("add-user")
    added_parser.add_argument("--username", type=str)
    added_parser.add_argument("--password", type=str)
    return parser


if __name__ == "__main__":
    main(sys.argv[1:])

from flask.app import Flask
from flask.cli import FlaskGroup
from src import app, db

cli = FlaskGroup(app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session_commit()


if __name__ == "__main__":
    cli()

import click
from energuide import database
from energuide import transform
from energuide import extractor


@click.group()
def main() -> None:
    pass


@main.command()
@click.option('--username', envvar=database.EnvVariables.username.value, default=database.EnvDefaults.username.value)
@click.option('--password', envvar=database.EnvVariables.password.value, default=database.EnvDefaults.password.value)
@click.option('--host', envvar=database.EnvVariables.host.value, default=database.EnvDefaults.host.value)
@click.option('--port', envvar=database.EnvVariables.port.value, default=database.EnvDefaults.port.value, type=int)
@click.option('--db_name', envvar=database.EnvVariables.database.value, default=database.EnvDefaults.database.value)
@click.option('--collection',
              envvar=database.EnvVariables.collection.value,
              default=database.EnvDefaults.collection.value)
@click.option('--filename', type=click.Path(exists=True), required=True)
def load(username: str, password: str, host: str, port: int, db_name: str, collection: str, filename: str) -> None:
    coords = database.DatabaseCoordinates(
        username=username,
        password=password,
        host=host,
        port=port
    )

    transform.run(coords, db_name, collection, filename)


@main.command()
@click.option('--infile', required=True)
@click.option('--outfile', required=True)
def extract(infile: str, outfile: str) -> None:
    extracted = extractor.extract_data(infile)
    extractor.write_data(extracted, outfile)

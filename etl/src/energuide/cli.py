import typing
import os
import click
from energuide import database
from energuide import transform
from energuide import extractor
from energuide import logger


LOGGER = logger.get_logger(__name__)


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
@click.option('--azure', is_flag=True, help='Download data from Azure')
@click.option('--filename', type=click.Path(exists=True), required=False)
@click.option('--update/--no-update', default=True, help='Update data instead of rebuilding from empty')
@click.option('--progress/--no-progress', default=True)
@click.option('--production/--local',
              envvar=database.EnvVariables.production.value,
              default=False,
              help='Generate a connection string to an Atlas managed MongoDB instance')
def load(username: str,
         password: str,
         host: str,
         port: int,
         db_name: str,
         collection: str,
         azure: bool,
         filename: typing.Optional[str],
         update: bool,
         progress: bool,
         production: bool,
        ) -> None:

    coords = database.DatabaseCoordinates(
        username=username,
        password=password,
        host=host,
        port=port,
        production=production
    )

    reader: transform.ExtractProtocol
    if azure:
        LOGGER.info(f'Loading data from Azure into {db_name}.{collection}')
        azure_coords = transform.AzureCoordinates.from_env()
        reader = transform.AzureExtractReader(azure_coords)
    elif filename:
        LOGGER.info(f'Loading data from {filename} into {db_name}.{collection}')
        reader = transform.LocalExtractReader(filename)
    else:
        LOGGER.error('Must supply a filename or use azure')
        raise ValueError('Must supply a filename or use azure')
    data = transform.transform(reader, progress)
    database.load(coords, db_name, collection, data, update)
    LOGGER.info(f'Finished loading data')


@main.command()
@click.option('--infile', required=True)
@click.option('--outfile', required=True)
@click.option('--progress/--no-progress', default=True)
def extract(infile: str, outfile: str, progress: bool) -> None:
    LOGGER.info(f'Extracting data from {infile} into {outfile}')
    if os.path.exists(outfile):
        LOGGER.warning(f'Warning: file {outfile} exists. Overwriting.')
    extracted = extractor.extract_data(infile, show_progress=progress)
    records_written, records_failed = extractor.write_data(extracted, outfile)
    LOGGER.info(f'Finished extracting data into {outfile}. '
                f'Successfully written: {records_written}. Failed: {records_failed}')

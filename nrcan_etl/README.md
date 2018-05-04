[La version française suit.](#---------------------------------------------------------------------)

## Energuide API - ETL component

### Installation

#### Python 3.6

Energuide API - ETL is tested to run on Python 3.6. To begin, you will need to have Python 3.6 installed.

We recommend `pyenv` as an easy way to easily install and switch between any versions of Python that you need.

See https://github.com/pyenv/pyenv#installation for pyenv installation instructions.

#### MongoDB

To run the ETL, you need to be able to access a MongoDB instance. For instructions on installing one locally, see https://docs.mongodb.com/manual/administration/install-community/

#### Virtualenv

Installing Python applications in a `virtualenv` is considered best practice. To do so, run:
```
python3 -m venv env
source env/bin/activate
```
This will create a new virtualenv in a  folder called `env`, and activate the virutalenv. To deactivate the virtualenv, run `deactivate`

**WINDOWS NOTE** To activate a virtual environment on Windows instead run `env\Scripts\activate.bat`

#### Installing the app

Inside an activated virtualenv, and from the python folder of the project, run:
```
pip install -r requirements.txt
pip install -e .
```

#### Running the app

The ETL application is accessed from the `energuide` CLI. Run `energuide --help` for help.

There are currently two commands for energuide:
```
energuide extract --infile /path/to/file --outfile /path/to/other/file
```

```
energuide load --filename /path/to/file
```

These two commands are meant to be chained together,`energuide load` accepts a file that is output by `energuide extract`.

A sample file is included for demonstration purposes at `./tests/randomized_energuide_data.csv`

By default, the `energuide load` command connects using the following defaults:
- username: `''` (blank)
- password: `''` (blank)
- host: `localhost`
- port: `27017`
- database: `energuide`
- collection: `dwellings`

Any of these defaults may be overridden at the command line using command-line flags:
```
energuide load --username my_username --filename path/to/file
```
They may also be overriden using environment variables prefixed with `ENERGUIDE_`:
```
ENERGUIDE_USERNAME=my_username energuide load --filename path/to/file
```

Run `energuide load --help` for a full list of available options.

#### Running tests locally

Many of the tests require a running local MongoDB server. It will attempt to connect using the environment variable values, if they are set, or the defaults if they are not.

To run the tests, run:
```
pytest tests
```

To run the linter, run:
```
pylint src tests
```

To run the mypy type checker, run:
```
mypy src tests
```

#### Automated Testing

This repo is connected to CircleCI, and all tests, linters, and static type checking must pass before merging to master.


### Running Locally

The system can be run locally using the CLI commands that are described above, but to run all the components behaving as they do when deployed to Azure, follow instructions in the **Running Locally** section of the `extract_endpoint` module.

## ---------------------------------------------------------------------

## API de l'Énerguide - Composantes ETL

### Installation

#### Python 3.6

L'API de l'Énerguide - ETL est testé pour fonctionner avec Python 3.6. Pour commencer, vous devrez avoir Python 3.6 d'installé.

Nous recommendons `pyenv` comme moyen de l'installer facilement et de changer entre les différentes versions de Python que vous avez besoin.

Visitez https://github.com/pyenv/pyenv#installation pour les instructions d'installation pour pyenv.

#### MongoDB

Pour faire fonctionner l'ETL, vous devez avoir accès à une instance de MongoDB. Pour obtenir les instructions d'installation locale, visitez https://docs.mongodb.com/manual/administration/install-community/

#### Virtualenv (Environnement virtuel)

Installer des application Python dans un `virtualenv` est considéré comme une pratique exemplaire. Pour le faire, exécutez :
```
python3 -m venv env
source env/bin/activate
```
Ceci va créer un nouvel 'virtualenv' dans un dossier appelé `env`, et activera le 'virutalenv'. Pour le désactivé, exécutez `deactivate`

**NOTE WINDOWS** Pour activer un environnement virtuel sur Windows, exécutez la commande `env\Scripts\activate.bat`

#### Installer l'application

À l'intérieur du virtualenv activé, et à partir du dossier python du projet, exécutez :
```
pip install -r requirements.txt
pip install -e .
```

#### Exécuter l'application

L'application ETL est accessible à partir du CLI `energuide`. Exécutez `energuide --help` pour obtenir l'aide.

Il y a présentement deux commandes pour l'énerguide :
```
energuide extract --infile /path/to/file --outfile /path/to/other/file
```

```
energuide load --filename /path/to/file
```

Ces deux commandes sont faites pour être ensemble,`energuide load` accepte les fichiers qui sont produits par `energuide extract`.

Un exemple est disponible à`./tests/randomized_energuide_data.csv`

Par défaut la commande `energuide load` connecte en utilisant les paramètres par défaut suivants :
- username: `''` (blank)
- password: `''` (blank)
- host: `localhost`
- port: `27017`
- database: `energuide`
- collection: `dwellings`

Ces paramètres peuvent être remplacés en utilisant la ligne de commande :
```
energuide load --username my_username --filename path/to/file
```
Ils peuvent aussi être remplacés en utilisant les variables d'environnement avec le préfix `ENERGUIDE_` :
```
ENERGUIDE_USERNAME=my_username energuide load --filename path/to/file
```

Exécutez `energuide load --help` pour obtenir la liste complète des options disponibles.

#### Exécuter les tests localement

Plusieurs tests requiert un serveur local MongoDB actif. Il tentera de connecter en utilisant les variables d'environnement si elles sont identifiées, ou celles par défaut si elles ne le sont pas.

Pour exécuter les tests, exécutez :
```
pytest tests
```

Pour exécuter le 'linter', exécutez :
```
pylint src tests
```

Pour exécuter le vérificateur de type 'mypy', exécutez :
```
mypy src tests
```

#### Tests automatizés

Ce dépôt de code est connecté à CircleCI et tous les tests, 'linters' et les vérifications de type statique doivent passer avant d'être fusionnés à la branche 'master'.


### Exécuter localement

Le système peut être exécuter localement en utilisant les commandes CLI qui sont identifiées ci-haut. Mais afin que tous les composants agissent de la même façon que lorsqu'ils sont déployés sur Azure, veuillez suivre les instructions dans la section  **Exécuter localement** du module `extract_endpoint`.

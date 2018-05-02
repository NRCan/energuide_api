
[La version française suit.](#---------------------------------------------------------------------)

# Adding AIR50P and UGRAIR50PA (aka airLeakage) to the API

This guide follows the instructions provided in the add a field to ETL guide. In order to add a field to the API, you will first
need to add it to the ETL. If you've already added your field to the ETL, you're good to go, read on!

## Loading your new data to your local mongoDB

In order to access your new field, you will need data that includes it it in your database. Start by running your updated energuide `extract` & `load`
functions with the test data. From the root folder:

```
cd nrcan_etl
source env/bin/activate
energuide extract --infile tests/scrubbed_random_sample_xml.csv --outfile tests/sample_data.zip
energuide load --filename tests/sample_data.zip
```

You should receive the message `updated 11 rows in the database`.

## Adding the new field to the schema

### `api/src/schema/index.js`

1. Figure out which type (Evaluation or Dwelling) your new field should be added to. In this case, airLeakage is part of the Evaluation class, so we'll
   add it to our Evaluation query.

2. Add the new field to the Evaluation query. The syntax to add a field is `fieldName: type`, where `fieldName` is the name of the field **exactly** as it appears in
   the database, and `type` is the type of data you expect it to return (int, float, a custom defined type, etc). If the name of the field in the schema does not match the name of the field in the database, the api will not be able to retrieve the data.

airLeakage will look like this in the schema:

```
type Evaluation @cacheControl(maxAge: 90) {
  ...
  airLeakage: Rating
  ...
}
```

3. Wait, why is the `type` `rating`? To make our lives easier! During development, we noticed most of the fields we were adding had a `measurement` value and `upgrade` value.
   Rather than create a new custom type for each field, we created a reusable `Rating` type that combines `measurement` & `upgrade`. It looks like this in the schema:

```
type Rating @cacheControl(maxAge: 90) {
  measurement: Float
  upgrade: Float
}
```

If you encounter more nested data when adding fields, you can create your own custom types simply by defining them the same way that Rating is defined above.

4. To see your new field in the API, save index.js then build & run the api:

```
yarn && yarn run build
NRCAN_DB_CONNECTION_STRING="mongodb://localhost:27017" \
	NRCAN_DB_NAME="energuide" \
	NRCAN_COLLECTION_NAME="dwellings" \
	NRCAN_ENGINE_API_KEY="your_apollo_engine_api_key" yarn start
```

Navigate to http://localhost:3000/. You should now be able to query airLeakage as follows:

```
query {
  dwellings{
    results {
      evaluations {
        airLeakage
        }
      }
    }
  }
}
```

:tada:! If the field doesn't appear, be sure to check the spelling of the field name, and make sure you've run yarn build to rebuild the files.

Next lets write some tests!

## Adding a unit test for the new field

### `api/src/schema/__tests__/schema.test.js`

1. Add your new field to the `'Evaluation Type'` test. It should look like this:

```
describe('Evaluation Type', () => {
  it('is defined', () => {
    expect(typeMap).toHaveProperty('Evaluation')
  })

  it('has the expected fields', () => {
    const Evaluation = typeMap.Evaluation
    const fields = Object.keys(Evaluation.getFields())
    expect(fields).toEqual([
      ...
      airLeakage,
      ...
    ])
  })
})
```

If you are adding a new `Dwelling` field, you would add it to the `Dwelling Type` test instead.

2. In your console, run `yarn test`. All your tests should pass.

## Adding an integration test for the new field

### `api/test/queries.test.js`

1. We need to test to make sure the field returns the data we expect. To do this, we need to pick a `houseId` and matching `airLeakage` values. You can get these values
   by looking at the data in the database, or you can start up the api as described earlier and run the following query:

```
query {
  dwellings{
    results {
      houseId
      evaluations {
        airLeakage {
            measurement
            upgrade
          }
        }
      }
    }
  }
}
```

Write down the first values for `houseId`, `measurement` & `upgrade` that the API returns. These will be your values for `testHouseId`, `testMeasurement` & `testUpgrade`
in the following step.

2. Above the `'retrieves all keys for ersRating data'` test, write a test to make sure your new field retrieves the data you expect. This test will look very similar to the tests already there: make a request to the server for your new field, and assert that you get the data you expect back. This is an example of what the test may look like, where `testHouseId`, `testMeasurement` & `testUpgrade`
   are your values from the first step.

```
it('retrieves all keys for airLeakage data', async () => {
  let response = await request(server)
    .post('/graphql')
    .set('Content-Type', 'application/json; charset=utf-8')
    .send({
      query: `{
        dwelling(houseId:testHouseId){
          evaluations {
            airLeakage {
              measurement
              upgrade
            }
          }
        }
      }`,
    })
  expect(response.body).not.toHaveProperty('errors')
  let { dwelling: { evaluations } } = response.body.data
  let [first] = evaluations
  let airLeakage = first.airLeakage
  expect(airLeakage.measurement).toEqual(testMeasurement)
  expect(airLeakage.upgrade).toEqual(testUpgrade)
})

it('retrieves all keys for ersRating data', async () => {
  ...
})
```

3. In your console, run `yarn integration`, all your tests should pass.

## Adding an English & French description for the new field

### `api/src/schema/index.js`

1. Above your new field, add an i18n formatted string with the field description, like so:

```
type Evaluation @cacheControl(maxAge: 90) {
  ...
  # ${i18n.t`Air leakage at 50 pascals`}
  airLeakage: Rating
  ...
}
```

Note: This description was just pulled directly from the TSV field.

2. Run `yarn extract` to load your new description into the English & French description locales.

3. Time to add your French description! Open up `api/src/locale/fr/messages.json` and search for your english description.
   You should find something that looks like this:

```
"Air leakage at 50 pascals": {
  "translation": "",
```

In the empty translation space, add your French translation. For airLeakage, it would look like this:

```
"Air leakage at 50 pascals": {
  "translation": "Fuite d'air à 50 Pa",
```


4. Run `yarn compile` to compile your new messages. Note that this step can potentially cause errors
   on a windows machine. We are currently investigating the issue.

## Document the new field

Make sure to add your new field & description to the existing API documentation. This way the documentation stays up
to date for future developers. You can find the [English documentation here](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-en.md), and the [French documentation here](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-fr.md).

## Push all the things to github!

Last step! Commit all your changed files to github & push your branch up for a code review. Once your tests pass & your code is reviewed, merge to master,
wait a bit, and then navigate to the live api to check out your new field, yay! :tada: :tada:

## If you have any issues with the process...

Please open an issue in our github issues tracker at https://github.com/cds-snc/nrcan_api/issues

## ---------------------------------------------------------------------

# Ajout du AIR50P et du UGRAIR50PA (aussi appelé airLeakage) à l’interface de programmation d’applications (API)

Ce guide suit les instructions fournies dans le lien ajouter un champ au guide d’Extraire, transformer et charger (ETC). Pour ajouter un champ à l’API, vous devrez premièrement l’ajouter à l’ETC. Si vous avez déjà ajouté votre champ à l’ETC, vous pouvez y aller, continuer à lire!

## Chargement de vos nouvelles données à votre mongoDB locale

Pour accéder à votre champ, vous aurez besoin de données qui l’incluent dans votre base de données. Commencer par exécuter votre mise à jour des fonctions ÉnerGuide d’extraire et de charger avec les données d’essai. Du dossier racine :
```
cd nrcan_etl
source env/bin/activate
energuide extract --infile tests/scrubbed_random_sample_xml.csv --outfile tests/sample_data.zip
energuide load --filename tests/sample_data.zip
```
Vous devriez recevoir le message 11 rangées mises à jour dans la base de données.

## Ajout d’un nouveau champ au schéma

api/src/schema/index.js


1. Déterminez quel type (Évaluation ou Logement) auquel votre nouveau champ devrait s’ajouter. Dans ce cas, l’airLeakage fait partie de la classe d’Evaluation, donc nous l’ajouterons à notre requête d’évaluation.

2. Ajoutez un nouveau champ à la requête d’évaluation. La syntaxe d’ajouter un champ est fieldName : type, où le fieldName est le nom du champ exactement tel qu’il est dans la base de données, et le type est le type de données que vous prévoyez qu’il retourne (int, float, un type défini spécial, etc.). Si le nom du champ dans le schéma ne correspond pas au nom du champ dans la base de données, l’API ne sera pas en mesure de récupérer les données.

L’airLeakage ressemblera à ceci dans le schéma :
```
type Evaluation @cacheControl(maxAge: 90) {
  ...
  airLeakage: Rating
  ...
}
```

3. Attendez, pourquoi le type rating? Pour rendre nos vies plus faciles! Lors de l’élaboration, nous avons constaté que la plupart des champs que nous ajoutons avaient une valeur measurement et une valeur upgrade. Au lieu de créer un nouveau type spécial pour chaque champ, nous avons créé un type de classement réutilisable qui combine measurement et upgrade. Cela ressemble à ceci dans le schéma :
```
type Rating @cacheControl(maxAge: 90) {
  measurement: Float
  upgrade: Float
}
```
Si vous rencontrez plus de données imbriquées lors de l’ajout des champs, vous pouvez créer vos propres types tout simplement en les définissants de la même manière que le classement défini plus haut.

4. Pour voir votre nouveau champ dans l’API, sauvegardez index.js puis élaborez et exécutez l’API :
yarn && yarn run build
```
NRCAN_DB_CONNECTION_STRING="mongodb://localhost:27017" \
	NRCAN_DB_NAME="energuide" \
	NRCAN_COLLECTION_NAME="dwellings" \
	NRCAN_ENGINE_API_KEY="your_apollo_engine_api_key" yarn start
```
Naviguez jusqu’à http://localhost:3000/. Vous devriez être capable maintenant d’interroger l’airLeakage comme ceci :
```
query {
  dwellings{
    results {
      evaluations {
        airLeakage
        }
      }
    }
  }
}
```
! Si le champ n’apparaît pas, assurez-vous de vérifier l’orthographe du nom du champ, et assurez-vous que vous avez exécuté le fil élaboré pour reconstituer les dossiers.

Après, faisons quelques essais!

## Ajout d’un essai unitaire pour le nouveau champ

api/src/schema/__tests__/schema.test.js

1. Ajoutez votre nouveau champ de type 'Evaluation' au test. Cela devrait ressembler à ceci :
```
describe('Evaluation Type', () => {
  it('is defined', () => {
    expect(typeMap).toHaveProperty('Evaluation')
  })
 
  it('has the expected fields', () => {
    const Evaluation = typeMap.Evaluation
    const fields = Object.keys(Evaluation.getFields())
    expect(fields).toEqual([
      ...
      airLeakage,
      ...
    ])
  })
})
```
Si vous ajoutez un nouveau champ de logement, vous l’ajouteriez plutôt au test du Type de logement.

2.Dans votre console, exécutez yarn test. Tous vos essais devraient réussir.

## Ajout d’un essai d’intégration pour le nouveau champ

api/test/queries.test.js

1. Nous devons tester pour s’assurer que le champ retourne les données que nous prévoyons. Pour faire cela, nous devons choisir une donnée du champ houseId et les valeurs de correspondance d’airLeakage. Vous pouvez avoir ces valeurs en regardant les données dans la base de données, ou vous pouvez démarrer l’API tel que mentionné précédemment et exécuter la requête suivante :
```
query {
  dwellings{
    results {
      houseId
      evaluations {
        airLeakage {
            measurement
            upgrade
          }
        }
      }
    }
  }
}
```

Écrivez les premières valeurs pour les champs houseId, measurement et upgrade que l’API retourne. Ce seront vos valeurs pour les champs testHouseId, testMeasurement & testUpgrade dans la prochaine étape.

2. Au-dessus du test de 'retrieves all keys for ersRating data', rédigez un test pour s’assurer que votre nouveau champ puisse récupérer les données que vous prévoyiez. Cet essai ressemblera beaucoup aux tests qui existent déjà : faites une requête au serveur pour votre nouveau champ, et assurez-vous d’avoir les données que vous espériez avoir. Ceci est un exemple de ce que l’essai peut ressembler, où les champs testHouseId, testMeasurement & testUpgrade sont vos valeurs de votre première étape.

```
it('retrieves all keys for airLeakage data', async () => {
  let response = await request(server)
    .post('/graphql')
    .set('Content-Type', 'application/json; charset=utf-8')
    .send({
      query: `{
        dwelling(houseId:testHouseId){
          evaluations {
            airLeakage {
              measurement
              upgrade
            }
          }
        }
      }`,
    })
  expect(response.body).not.toHaveProperty('errors')
  let { dwelling: { evaluations } } = response.body.data
  let [first] = evaluations
  let airLeakage = first.airLeakage
  expect(airLeakage.measurement).toEqual(testMeasurement)
  expect(airLeakage.upgrade).toEqual(testUpgrade)
})
 
it('retrieves all keys for ersRating data', async () => {
  ...
})
```

3. Dans votre console, veuillez exécuter yarn integration, tous vos essais devraient réussir.


## Ajout d’une description en anglais et en français pour le nouveau champ

api/src/schema/index.js

1. Au-dessus de votre nouveau champ, ajoutez une chaîne formatée i18n avec la description du champ, comme ceci :
```
type Evaluation @cacheControl(maxAge: 90) {
  ...
  # ${i18n.t`Air leakage at 50 pascals`}
  airLeakage: Rating
  ...
}
```
Remarque : cette description a été prise directement du champ du fichier TSV.
2. Exécutez yarn extract pour charger votre nouvelle description dans les locaux de description en anglais et en français.
3.Le moment est venu d’ajouter votre description en français! Ouvrez api/src/locale/fr/messages.json et faites une recherche pour votre description anglaise. Vous devriez trouver quelque chose qui ressemble à ceci :
```
"Air leakage at 50 pascals": {
  "translation": "",
```
Dans l’espace vide de traduction (translation), ajoutez votre traduction en français. Pour l’airLeakage, cela ressemblerait à ceci:
```
"Air leakage at 50 pascals": {
  "translation": "Fuite d'air à 50 Pa",
```
4. Exécutez yarn compile pour réunir vos messages. Veuillez noter que cette étape peut potentiellement entraîner des erreurs sur un ordinateur Windows. Nous faisons actuellement des enquêtes sur ce problème.

## Documenter le nouveau champ

Assurez-vous d’ajouter votre nouveau champ et votre description à la documentation existante de l’API. De cette manière, la documentation reste à jour pour les futurs concepteurs. Vous pouvez trouver la documentation [en anglais ici](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-en.md), et la documentation [en français ici](https://github.com/cds-snc/nrcan_api/blob/master/api/docs-fr.md)

## Pousser tout sur Github!

Dernière étape! Enregistrez tous vos fichiers modifiés sur Github et poussez votre branche pour une révision de code. Une fois que vos tests ont réussi et votre code révisé, fusionnez le tout sur la branche maître (master), attendez en peu, et ensuite naviguez jusqu’à l’API en production pour vérifier votre nouveau champ, Youppie!! 

## Si vous avez des questions sur le processus...

Veuillez formuler une question dans le système de suivi des questions sur Github au https://github.com/cds-snc/nrcan_api/issues


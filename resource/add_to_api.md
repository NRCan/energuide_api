# Adding AIR50P and UGRAIR50PA (aka airLeakage) to the API
This guide follows the instructions provided in the add_to_etl.md file. In order to add a field to the API, you will first
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

If you are adding a new `Dwelling` field, you would add it to the `Dwelling Type` test instead/

2. In your console, run `yarn test`. All your tests should pass.

## Adding an integration test for the new field

### `api/test/queries.test.js`

1. We need to test to make sure the field returns the data we expect. To do this, we need to pick a `houseID` and matching `airLeakage` values. You can get these values
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

2. Above the `'retrieves all keys for ersRating data'` test, write the following test. Make sure to replace `testHouseId`, `testMeasurement` & `testUpgrade`
with the values you wrote down in step 1.

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

2. Run `yarn extract` to load your new description into the English & French description locals.

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

## Push all the things to github!

Last step! Commit all your changed files to github & push your branch up for a code review. Once your tests pass & your code is reviewed, merge to master,
wait a bit, and then navigate to the live api to check out your new field, yay! :tada: :tada:

## If you have any issues with the process...

Please open an issue in our github issues tracker at https://github.com/cds-snc/nrcan_api/issues 

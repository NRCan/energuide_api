import { MongoClient } from 'mongodb'
import request from 'supertest'
import Server from '../src/server'

/* eslint-disable import/named */
import * as enumFunctions from '../src/schema/enums' // eslint-disable-line
/* eslint-enable import/named */

let client, db, collection
const url = 'mongodb://localhost:27017'
const dbName = 'energuide'

describe('Enum values', () => {
  // There is coupling between the structure of the query object and the
  // structure of the documents in the database. That knowledge needs to
  // live somewhere. This tests that the structure of the query is in sync
  // with structure of the document.
  beforeAll(async () => {
    client = await MongoClient.connect(url)
    db = client.db(dbName)
    collection = db.collection('dwellings')
  })

  afterAll(async () => {
    client.close()
  })

  const testFields = {
    dwellingHouseId: { testValue: 189250 },
    dwellingYearBuilt: { testValue: 1900 },
    dwellingCity: { testValue: 'Dartmouth' },
    dwellingRegion: { testValue: 'NS' },
    dwellingForwardSortationArea: { testValue: 'T1L' },
    evaluationEvaluationType: { testValue: 'E' },
    evaluationFileId: { testValue: '3C10E11075' },
    evaluationErsRating: { testValue: 120 },
  }

  Object.keys(testFields).forEach(functionName => {
    describe(functionName, () => {
      it('returns a query object capable of returning data', async () => {
        let { testValue } = testFields[functionName] // eslint-disable-line
        let query = enumFunctions[functionName](testValue) //eslint-disable-line
        let result = await collection.findOne(query)
        expect(result).not.toBe(null)
      })

      it(`${functionName} is included in the filter field enum`, async () => {
        let { testValue } = testFields[functionName] // eslint-disable-line
        let server = new Server({
          client: collection,
        })
        let response = await request(server)
          .post('/graphql')
          .set('Content-Type', 'application/json; charset=utf-8')
          .send({
            query: `{
                 dwellings(
                  filters: [
                    {field: dwellingForwardSortationArea comparator: eq value: "C1A"}
                    {field: ${functionName} comparator: eq value: "${testValue}"}
                  ]
                 ) {
                   results {
                     city
                   }
                 }
               }`,
          })
        expect(response.body).not.toHaveProperty('errors')
      })
    })
  })

  const testDates = {
    evaluationEntryDate: { testValue: '2011-11-18' },
    evaluationCreationDate: { testValue: '2012-10-01T15:08:41' },
    evaluationModificationDate: { testValue: '2012-06-09T11:20:20' },
  }

  Object.keys(testDates).forEach(functionName => {
    describe(functionName, () => {
      it('returns a query object capable of returning data', async () => {
        let { testValue } = testDates[functionName] // eslint-disable-line
        let query = enumFunctions[functionName](testValue) //eslint-disable-line
        let result = await collection.findOne(query)
        expect(result).not.toBe(null)
      })
    })
  })
})

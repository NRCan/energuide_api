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
    heatedFloorAreaAreaAboveGradeMetres: { testValue: 600 },
    heatedFloorAreaAreaAboveGradeFeet: { testValue: 6458.34666336 },
    heatedFloorAreaAreaBelowGradeMetres: { testValue: 600 },
    heatedFloorAreaAreaBelowGradeFeet: { testValue: 6458.34666336 },
    wallLabel: { testValue: 'Main floor' },
    wallStructureTypeEnglish: { testValue: null },
    wallStructureTypeFrench: { testValue: null },
    wallComponentTypeSizeEnglish: { testValue: null },
    wallComponentTypeSizeFrench: { testValue: null },
    wallInsulationNominalRsi: { testValue: 3.3615 },
    wallInsulationNominalR: { testValue: 19.0874822073255 },
    wallInsulationEffectiveRsi: { testValue: 2.6892 },
    wallInsulationEffectiveR: { testValue: 15.2699857658604 },
    wallAreaMetres: { testValue: 92.97658384 },
    wallAreaFeet: { testValue: 1000.7916833561255 },
    wallPerimeterMetres: { testValue: 35.7616 },
    wallPerimeterFeet: { testValue: 117.328087744 },
    wallHeightMetres: { testValue: 2.5999 },
    wallHeightFeet: { testValue: 8.529855915999999 },
    foundationFoundationTypeEnglish: { testValue: 'Basement' },
    foundationFoundationTypeFrench: { testValue: 'Sous-sol' },
    foundationLabel: { testValue: 'Foundation - 1' },
    foundationConfigurationType: { testValue: 'BCIN' },
    foundationMaterialEnglish: { testValue: 'concrete' },
    foundationMaterialFrench: { testValue: 'béton' },
    foundationHeaderInsulationNominalRsi: { testValue: 3.3615 },
    foundationHeaderInsulationNominalR: { testValue: 19.0874822073255 },
    foundationHeaderInsulationEffectiveRsi: { testValue: 2.6892 },
    foundationHeaderInsulationEffectiveR: { testValue: 15.2699857658604 },
    foundationHeaderAreaMetres: { testValue: 7.991488000000001 },
    foundationHeaderAreaFeet: { testValue: 86.01966643346914 },
    foundationHeaderPerimeterMetres: { testValue: 34.7456 },
    foundationHeaderPerimeterFeet: { testValue: 113.99475430400001 },
    foundationHeaderHeightMetres: { testValue: 0.23 },
    foundationHeaderHeightFeet: { testValue: 0.7545932000000001 },
    foundationFloorFloorTypeEnglish: { testValue: 'Slab' },
    foundationFloorFloorTypeFrench: { testValue: 'Dalle' },
    foundationFloorAreaMetres: { testValue: 72.6432 },
    foundationFloorAreaFeet: { testValue: 781.9249472263218 },
    foundationFloorPerimeterMetres: { testValue: 34.7466 },
    foundationFloorPerimeterFeet: { testValue: 113.998035144 },
    // TODO: Uncomment and add appropriate values when issue #315 is resloved
    // foundationFloorInsulationNominalRsi: { testValue: null },
    // foundationFloorInsulationNominalR: { testValue: null },
    // foundationFloorInsulationEffectiveRsi: { testValue: null },
    // foundationFloorInsulationEffectiveR: { testValue: null },
    // foundationFloorWidthMetres: { testValue: null },
    // foundationFloorWidthFeet: { testValue: null },
    // foundationFloorLengthMetres: { testValue: null },
    // foundationFloorLengthFeet: { testValue: null },
    foundationWallWallTypeEnglish: { testValue: 'Interior' },
    foundationWallWallTypeFrench: { testValue: 'Intérieur' },
    foundationWallInsulationNominalRsi: { testValue: 2.175 },
    foundationWallInsulationNominalR: { testValue: 12.350222757974999 },
    foundationWallInsulationEffectiveRsi: { testValue: 1.74 },
    foundationWallInsulationEffectiveR: { testValue: 9.88017820638 },
    foundationWallPercentage: { testValue: 100 },
    foundationWallAreaMetres: { testValue: 87.1618461 },
    foundationWallAreaFeet: { testValue: 938.2023632203881 },
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

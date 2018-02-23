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

  const testData = {
    dwellingHouseId: { testValue: 189250 },
    dwellingYearBuilt: { testValue: 1900 },
    dwellingCity: { testValue: 'Charlottetown' },
    dwellingRegion: { testValue: 'PE' },
    dwellingForwardSortationArea: { testValue: 'C1A' },
    ventilationTypeEnglish: { testValue: 'Heat recovery ventilator' },
    ventilationTypeFrench: { testValue: 'Ventilateur-récupérateur de chaleur' },
    ventilationAirFlowRateLps: { testValue: 220 },
    ventilationAirFlowRateCfm: { testValue: 466.1536 },
    ventilationEfficiency: { testValue: 55 },
    floorLabel: { testValue: 'Rm over garage' },
    floorInsulationNominalRsi: { testValue: 2.11 },
    floorInsulationNominalR: { testValue: 11.981135641069999 },
    floorInsulationEffectiveRsi: { testValue: 2.61 },
    floorInsulationEffectiveR: { testValue: 14.82026730957 },
    floorAreaMetres: { testValue: 9.2903 },
    floorAreaFeet: { testValue: 99.99996334435568 },
    floorLengthMetres: { testValue: 3.048 },
    floorLengthFeet: { testValue: 10.00000032 },
    waterHeatingTypeEnglish: { testValue: 'Natural gas storage tank' },
    waterHeatingTypeFrench: { testValue: 'Réservoir au gaz naturel' },
    waterHeatingTankVolumeLitres: { testValue: 151.4 },
    waterHeatingTankVolumeGallon: { testValue: 39.995640800000004 },
    waterHeatingEfficiency: { testValue: 0.554 },
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
  }

  Object.keys(testData).forEach(functionName => {
    describe(functionName, () => {
      it('returns a query object capable of returning data', async () => {
        let { testValue } = testData[functionName] // eslint-disable-line
        let query = enumFunctions[functionName](testValue) //eslint-disable-line
        let result = await collection.findOne(query)
        expect(result).not.toBe(null)
      })

      it(`${functionName} is included in the filter field enum`, async () => {
        let { testValue } = testData[functionName] // eslint-disable-line
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
})

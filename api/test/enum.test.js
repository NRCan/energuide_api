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
    dwellingCity: { testValue: 'Charlottetown' },
    dwellingRegion: { testValue: 'PE' },
    dwellingForwardSortationArea: { testValue: 'C1A' },
    evaluationEvaluationType: { testValue: 'E' },
    evaluationFileId: { testValue: '3C10E11075' },
    evaluationErsRating: { testValue: 120 },
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
    heatingLabel: { testValue: 'Heating/Cooling System' },
    heatingHeatingTypeEnglish: { testValue: 'Furnace' },
    heatingHeatingTypeFrench: { testValue: 'Fournaise' },
    heatingEnergySourceEnglish: { testValue: 'Natural Gas' },
    heatingEnergySourceFrench: { testValue: 'Chauffage au gaz naturel' },
    heatingEquipmentTypeEnglish: { testValue: 'Induced draft fan furnace' },
    heatingEquipmentTypeFrench: { testValue: 'Fournaise à tirage induit' },
    heatingOutputSizeKW: { testValue: 8.5 },
    heatingOutputSizeBtu: { testValue: 29003.207 },
    heatingEfficiency: { testValue: 80 },
    heatingSteadyState: { testValue: 'Steady State' },
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
    ceilingLabel: { testValue: 'Ceiling01' },
    ceilingTypeEnglish: { testValue: 'Attic/gable' },
    ceilingTypeFrench: { testValue: 'Combles/pignon' },
    ceilingInsulationNominalRsi: { testValue: 6.3998 },
    ceilingInsulationNominalR: { testValue: 36.3397497041326 },
    ceilingInsulationEffectiveRsi: { testValue: 6.3998 },
    ceilingInsulationEffectiveR: { testValue: 36.3397497041326 },
    ceilingAreaMetres: { testValue: 77.1204 },
    ceilingAreaFeet: { testValue: 830.1171300283143 },
    ceilingLengthMetres: { testValue: 14.528 },
    ceilingLengthFeet: { testValue: 47.66404352 },
    doorTypeEnglish: { testValue: 'Steel Medium density spray foam core' },
    doorTypeFrench: {
      testValue: 'Acier / âme en mousse à vaporiser de densité moyenne',
    },
    doorInsulationRsi: { testValue: 1.14 },
    doorInsulationR: { testValue: 6.4732202041799995 },
    doorUFactor: { testValue: 0.8771929824561404 },
    doorUFactorImperial: { testValue: 0.15448261737709199 },
    doorAreaMetres: { testValue: 1.764 },
    doorAreaFeet: { testValue: 18.9875391902784 },
    windowLabel: { testValue: 'East0001' },
    windowInsulationRsi: { testValue: 0.2685 },
    windowInsulationR: { testValue: 1.5246137059845 },
    windowGlazingTypesEnglish: { testValue: 'Double/double with 1 coat' },
    windowGlazingTypesFrench: { testValue: 'Double/double, 1 couche' },
    windowCoatingsTintsEnglish: { testValue: 'Clear' },
    windowCoatingsTintsFrench: { testValue: 'Transparent' },
    windowFillTypeEnglish: { testValue: '13 mm Air' },
    windowFillTypeFrench: { testValue: "13 mm d'air" },
    windowSpacerTypeEnglish: { testValue: 'Metal' },
    windowSpacerTypeFrench: { testValue: 'Métal' },
    windowTypeEnglish: { testValue: 'Picture' },
    windowTypeFrench: { testValue: 'Fixe' },
    windowFrameMaterialEnglish: { testValue: 'Aluminum' },
    windowFrameMaterialFrench: { testValue: 'Aluminium' },
    windowAreaMetres: { testValue: 1.31104735596684 },
    windowAreaFeet: { testValue: 14.111997194858986 },
    windowWidthMetres: { testValue: 1.0746954 },
    windowWidthFeet: { testValue: 3.5259036561359998 },
    windowHeightMetres: { testValue: 1.2199246000000001 },
    windowHeightFeet: { testValue: 4.002377424664 },
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

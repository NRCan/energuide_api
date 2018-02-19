import { MongoClient } from 'mongodb'

/* eslint-disable import/named */
import {
  dwellingHouseId,
  dwellingYearBuilt,
  dwellingCity,
  dwellingRegion,
  dwellingForwardSortationArea,
  ventilationTypeEnglish,
  ventilationTypeFrench,
  ventilationAirFlowRateLps,
  ventilationAirFlowRateCfm,
  ventilationEfficiency,
} from '../src/schema/enums'
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

  describe('dwellingHouseId', () => {
    it('returns a query object', () => {
      expect(dwellingHouseId({ $eq: 189250 })).toEqual({
        houseId: { $eq: 189250 },
      })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = dwellingHouseId.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object which returns a value from the test data', async () => {
      let query = dwellingHouseId(189250)
      let result = await collection.findOne(query)
      expect(result.houseId).toEqual(189250)
    })
  })

  describe('dwellingYearBuilt', () => {
    it('returns a query object', () => {
      expect(dwellingYearBuilt(1900)).toEqual({ yearBuilt: 1900 })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = dwellingYearBuilt.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object which returns a value from the test data', async () => {
      let query = dwellingYearBuilt(1900)
      let result = await collection.findOne(query)
      expect(result.yearBuilt).toEqual(1900)
    })
  })

  describe('dwellingCity', () => {
    //  "city": "Charlottetown",

    it('returns a query object', () => {
      expect(dwellingCity('Charlottetown')).toEqual({ city: 'Charlottetown' })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = dwellingYearBuilt.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object which returns a value from the test data', async () => {
      let query = dwellingCity('Charlottetown')
      let result = await collection.findOne(query)
      expect(result.city).toEqual('Charlottetown')
    })
  })

  describe('dwellingRegion', () => {
    //  "region": "PE",

    it('returns a query object', () => {
      expect(dwellingRegion('PE')).toEqual({ region: 'PE' })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = dwellingRegion.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object which returns a value from the test data', async () => {
      let query = dwellingRegion('PE')
      let result = await collection.findOne(query)
      expect(result.region).toEqual('PE')
    })
  })

  describe('dwellingForwardSortationArea', () => {
    it('returns a query object', () => {
      expect(dwellingForwardSortationArea('C1A')).toEqual({
        forwardSortationArea: 'C1A',
      })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = dwellingForwardSortationArea.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object capable of returning data', async () => {
      let query = dwellingForwardSortationArea('C1A')
      let result = await collection.findOne(query)
      expect(result.forwardSortationArea).toEqual('C1A')
    })
  })

  describe('ventilationTypeEnglish', () => {
    it('returns a query object', () => {
      expect(ventilationTypeEnglish('foo')).toEqual({
        evaluations: {
          $elemMatch: {
            ventilations: {
              $elemMatch: {
                typeEnglish: 'foo',
              },
            },
          },
        },
      })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = ventilationTypeEnglish.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object capable of returning data', async () => {
      let query = ventilationTypeEnglish('Heat recovery ventilator')
      let result = await collection.findOne(query)
      expect(result).toBeTruthy()
    })
  })

  describe('ventilationTypeFrench', () => {
    it('returns a query object', () => {
      expect(ventilationTypeFrench('fou')).toEqual({
        evaluations: {
          $elemMatch: {
            ventilations: {
              $elemMatch: {
                typeFrench: 'fou',
              },
            },
          },
        },
      })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = ventilationTypeFrench.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object capable of returning data', async () => {
      let query = ventilationTypeFrench('Ventilateur-récupérateur de chaleur')
      let result = await collection.findOne(query)
      expect(result).toBeTruthy()
    })
  })

  describe('ventilationAirFlowRateLps', () => {
    it('returns a query object', () => {
      expect(ventilationAirFlowRateLps(200)).toEqual({
        evaluations: {
          $elemMatch: {
            ventilations: {
              $elemMatch: {
                airFlowRateLps: 200,
              },
            },
          },
        },
      })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = ventilationAirFlowRateLps.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object capable of returning data', async () => {
      let query = ventilationAirFlowRateLps(220)
      let result = await collection.findOne(query)
      expect(result).toBeTruthy()
    })
  })

  describe('ventilationAirFlowRateCfm', () => {
    it('returns a query object', () => {
      expect(ventilationAirFlowRateCfm(200)).toEqual({
        evaluations: {
          $elemMatch: {
            ventilations: {
              $elemMatch: {
                airFlowRateCfm: 200,
              },
            },
          },
        },
      })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = ventilationAirFlowRateLps.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object capable of returning data', async () => {
      let query = ventilationAirFlowRateCfm(466.1536)
      let result = await collection.findOne(query)
      expect(result).toBeTruthy()
    })
  })

  describe('ventilationEfficiency', () => {
    it('returns a query object', () => {
      expect(ventilationEfficiency(200)).toEqual({
        evaluations: {
          $elemMatch: {
            ventilations: {
              $elemMatch: {
                efficiency: 200,
              },
            },
          },
        },
      })
    })

    it('has a toString function that produces an eval friendly expression', () => {
      let str = ventilationEfficiency.toString()
      let characters = [...str]
      expect(characters[0]).toEqual('(')
      expect(characters[characters.length - 1]).toEqual(')')
    })

    it('returns a query object capable of returning data', async () => {
      let query = ventilationEfficiency(55)
      let result = await collection.findOne(query)
      expect(result).toBeTruthy()
    })
  })
})

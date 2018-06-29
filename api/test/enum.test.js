import { MongoClient } from 'mongodb'
import { i18n, unpackCatalog } from 'lingui-i18n'
import Schema from '../src/schema'
/* eslint-disable import/named */
import {
  dwellingHouseId,
  dwellingYearBuilt,
  dwellingCity,
  dwellingRegion,
  dwellingForwardSortationArea,
  evaluationEvaluationType,
  evaluationFileId,
  evaluationHouseType,
  evaluationCreationDate,
  evaluationModificationDate,
  evaluationHeatedFloorArea, // eslint-disable-line
  evaluationEntryDate,
} from '../src/schema/enums'

i18n.load({
  fr: unpackCatalog(require('../src/locale/fr/messages.js')),
  en: unpackCatalog(require('../src/locale/en/messages.js')),
})

const schema = new Schema(i18n)
const typeMap = schema.getTypeMap()
const { Field } = typeMap
const enumValues = Field.getValues().map(v => v.name)

let client, db, collection
const url = 'mongodb://localhost:27017'
const dbName = 'energuide'

describe('Enum values', () => {
  // There is coupling between the structure of the mongo query object and the
  // structure of the documents in the database. That knowledge needs to
  // live somewhere. That place is currently in what we've been calling enum
  // functions.
  // We've created functions that accept a value and return a mongodb query
  // object for each field that a user can include in a filter.
  // The enums presented to the user map internally to a stringified version of
  // those functions, which we can then eval to create another chunk of the
  // larger mongo query object.
  // This approach is a "clever" way of meeting the requirement for a
  // generalized query capability, and when paired with a database like CosmosDB
  // that indexes every single field, should even be reasonably performant.
  beforeAll(async () => {
    client = await MongoClient.connect(url)
    db = client.db(dbName)
    collection = db.collection('dwellings')
  })

  afterAll(async () => {
    client.close()
  })

  describe('dwellingHouseId', () => {
    it('returns a query object capable of returning data', async () => {
      let query = dwellingHouseId(1024170) //eslint-disable-line
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('dwellingHouseId')
    })
  })

  describe('dwellingYearBuilt', () => {
    it('returns a query object capable of returning data', async () => {
      let query = dwellingYearBuilt(1921)
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('dwellingHouseId')
    })
  })

  describe('dwellingCity', () => {
    it('returns a query object capable of returning data', async () => {
      let query = dwellingCity('Anagance')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('dwellingCity')
    })
  })

  describe('dwellingRegion', () => {
    it('returns a query object capable of returning data', async () => {
      let query = dwellingRegion('NB')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('dwellingRegion')
    })
  })

  describe('dwellingForwardSortationArea', () => {
    it('returns a query object capable of returning data', async () => {
      let query = dwellingForwardSortationArea('O7I')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('dwellingForwardSortationArea')
    })
  })

  describe('evaluationEvaluationType', () => {
    it('returns a query object capable of returning data', async () => {
      let query = evaluationEvaluationType('D')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('evaluationEvaluationType')
    })
  })

  describe('evaluationFileId', () => {
    it('returns a query object capable of returning data', async () => {
      let query = evaluationFileId('1B07D10023')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('evaluationFileId')
    })
  })

  describe('evaluationHouseType', () => {
    it('returns a query object capable of returning data', async () => {
      let query = evaluationHouseType('Single detached')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('evaluationHouseType')
    })
  })

  describe('evaluationCreationDate', () => {
    it('returns a query object capable of returning data', async () => {
      let query = evaluationCreationDate('2011-03-14T14:26:52')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('evaluationCreationDate')
    })
  })

  describe('evaluationModificationDate', () => {
    it('returns a query object capable of returning data', async () => {
      let query = evaluationModificationDate('2008-11-25T18:44:30')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('evaluationModificationDate')
    })
  })

  describe('evaluationHeatedFloorArea', () => {
    // This test should pass but the test data doesn't have a value
    //   it('returns a query object capable of returning data', async () => {
    //     let query = evaluationHeatedFloorArea()
    //     let result = await collection.findOne(query)
    //     expect(result).not.toBe(null)
    //   })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('evaluationHeatedFloorArea')
    })
  })

  describe('evaluationEntryDate', () => {
    it('returns a query object capable of returning data', async () => {
      let query = evaluationEntryDate('2009-03-28')
      let result = await collection.findOne(query)
      expect(result).not.toBe(null)
    })

    it('one of the enum values on the Field type', () => {
      expect(enumValues).toContain('evaluationEntryDate')
    })
  })
})

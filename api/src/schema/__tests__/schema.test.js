import Schema from '../'
import { i18n, unpackCatalog } from 'lingui-i18n'

i18n.load({
  fr: unpackCatalog(require('../../locale/fr/messages.js')),
  en: unpackCatalog(require('../../locale/en/messages.js')),
})

const schema = new Schema(i18n)
const typeMap = schema.getTypeMap()

describe('Schema', () => {
  describe('Dwelling Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Dwelling')
    })
    it('has the expected fields', () => {
      const Dwelling = typeMap.Dwelling
      const fields = Object.keys(Dwelling.getFields())
      expect(fields).toEqual([
        'houseId',
        'yearBuilt',
        'city',
        'region',
        'forwardSortationArea',
        'evaluations',
      ])
    })
  })

  describe('Evaluation Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Evaluation')
    })

    it('has the expected fields', () => {
      const Evaluation = typeMap.Evaluation
      const fields = Object.keys(Evaluation.getFields())
      expect(fields).toEqual([
        'evaluationType',
        'entryDate',
        'fileId',
        'houseType',
        'creationDate',
        'modificationDate',
        'energyUpgrades',
        'heatedFloorArea',
        'ersRating',
        'eghRating',
        'greenhouseGasEmissions',
        'walls',
      ])
    })
  })

  describe('PaginatedResultSet', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('PaginatedResultSet')
    })

    it('has the expected fields', () => {
      const { PaginatedResultSet } = typeMap
      const fields = Object.keys(PaginatedResultSet.getFields())
      expect(fields).toEqual([
        'hasNext',
        'hasPrevious',
        'next',
        'previous',
        'results',
      ])
    })
  })

  describe('Rating Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Rating')
    })

    it('has the expected fields', () => {
      const Rating = typeMap.Rating
      const fields = Object.keys(Rating.getFields())
      expect(fields).toEqual(['measurement', 'upgrade'])
    })
  })

  describe('GreenhouseGasEmissions Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('GreenhouseGasEmissions')
    })

    it('has the expected fields', () => {
      const GreenhouseGasEmissions = typeMap.GreenhouseGasEmissions
      const fields = Object.keys(GreenhouseGasEmissions.getFields())
      expect(fields).toEqual(['measurement', 'upgrade'])
    })
  })

  describe('Wall Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Wall')
    })

    it('has the expected fields', () => {
      const Wall = typeMap.Wall
      const fields = Object.keys(Wall.getFields())
      expect(fields).toEqual(['measurement', 'upgrade'])
    })
  })

  describe('WallMeasurement Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('WallMeasurement')
    })

    it('has the expected fields', () => {
      const WallMeasurement = typeMap.WallMeasurement
      const fields = Object.keys(WallMeasurement.getFields())
      expect(fields).toEqual(['insulation', 'heatLost'])
    })
  })

  describe('Insulation Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Insulation')
    })

    it('has the expected fields', () => {
      const Insulation = typeMap.Insulation
      const fields = Object.keys(Insulation.getFields())
      expect(fields).toEqual(['percentage', 'rValue'])
    })
  })

  describe('Upgrade', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Upgrade')
    })

    it('has the expected fields', () => {
      const { Upgrade } = typeMap
      const fields = Object.keys(Upgrade.getFields())
      expect(fields).toEqual(['upgradeType', 'cost', 'priority'])
    })
  })
})

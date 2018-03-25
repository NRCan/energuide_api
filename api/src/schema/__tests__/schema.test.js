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

  describe('Wall Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Wall')
    })

    it('has the expected fields', () => {
      const Wall = typeMap.Wall
      const fields = Object.keys(Wall.getFields())
      expect(fields).toEqual([
        'label',
        'structureTypeEnglish',
        'structureTypeFrench',
        'componentTypeSizeEnglish',
        'componentTypeSizeFrench',
        'insulationNominalRsi',
        'insulationNominalR',
        'insulationEffectiveRsi',
        'insulationEffectiveR',
        'areaMetres',
        'areaFeet',
        'perimeterMetres',
        'perimeterFeet',
        'heightMetres',
        'heightFeet',
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
        'creationDate',
        'modificationDate',
        'walls',
        'heatedFloorArea',
        'energyUpgrades',
        'ersRating',
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

  describe('HeatedFloorArea', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('HeatedFloorArea')
    })

    it('has the expected fields', () => {
      const { HeatedFloorArea } = typeMap
      const fields = Object.keys(HeatedFloorArea.getFields())
      expect(fields).toEqual([
        'areaAboveGradeMetres',
        'areaAboveGradeFeet',
        'areaBelowGradeMetres',
        'areaBelowGradeFeet',
      ])
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

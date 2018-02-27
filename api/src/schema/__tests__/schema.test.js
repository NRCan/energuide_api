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

  describe('Door Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Door')
    })
    it('has the expected fields', () => {
      const Door = typeMap.Door
      const fields = Object.keys(Door.getFields())
      expect(fields).toEqual([
        'typeEnglish',
        'typeFrench',
        'insulationRsi',
        'insulationR',
        'uFactor',
        'uFactorImperial',
        'areaMetres',
        'areaFeet',
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

  describe('Ceiling Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Ceiling')
    })

    it('has the expected fields', () => {
      const Ceiling = typeMap.Ceiling
      const fields = Object.keys(Ceiling.getFields())
      expect(fields).toEqual([
        'label',
        'typeEnglish',
        'typeFrench',
        'insulationNominalRsi',
        'insulationNominalR',
        'insulationEffectiveRsi',
        'insulationEffectiveR',
        'areaMetres',
        'areaFeet',
        'lengthMetres',
        'lengthFeet',
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
        'creationDate',
        'modificationDate',
        'ceilings',
        'walls',
        'floors',
        'doors',
        'windows',
        'heatedFloorArea',
        'ventilations',
        'waterHeatings',
        'energyUpgrades',
      ])
    })
  })

  describe('Window Type', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Window')
    })

    it('has the expected fields', () => {
      const Window = typeMap.Window
      const fields = Object.keys(Window.getFields())
      expect(fields).toEqual([
        'label',
        'insulationRsi',
        'insulationR',
        'glazingTypesEnglish',
        'glazingTypesFrench',
        'coatingsTintsEnglish',
        'coatingsTintsFrench',
        'fillTypeEnglish',
        'fillTypeFrench',
        'spacerTypeEnglish',
        'spacerTypeFrench',
        'typeEnglish',
        'typeFrench',
        'frameMaterialEnglish',
        'frameMaterialFrench',
        'areaMetres',
        'areaFeet',
        'widthMetres',
        'widthFeet',
        'heightMetres',
        'heightFeet',
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

  describe('Ventilation', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Ventilation')
    })

    it('has the expected fields', () => {
      const { Ventilation } = typeMap
      const fields = Object.keys(Ventilation.getFields())
      expect(fields).toEqual([
        'typeEnglish',
        'typeFrench',
        'airFlowRateLps',
        'airFlowRateCfm',
      ])
    })
  })

  describe('WaterHeater', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('WaterHeater')
    })

    it('has the expected fields', () => {
      const { WaterHeater } = typeMap
      const fields = Object.keys(WaterHeater.getFields())
      expect(fields).toEqual([
        'typeEnglish',
        'typeFrench',
        'tankVolumeLitres',
        'tankVolumeGallon',
        'efficiency',
      ])
    })
  })

  describe('Floor', () => {
    it('is defined', () => {
      expect(typeMap).toHaveProperty('Floor')
    })

    it('has the expected fields', () => {
      const { Floor } = typeMap
      const fields = Object.keys(Floor.getFields())
      expect(fields).toEqual([
        'label',
        'insulationNominalRsi',
        'insulationNominalR',
        'insulationEffectiveRsi',
        'insulationEffectiveR',
        'areaMetres',
        'areaFeet',
        'lengthMetres',
        'lengthFeet',
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

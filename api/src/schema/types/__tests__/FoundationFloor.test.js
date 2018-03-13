import { createFoundationFloor } from '../FoundationFloor'
import { createI18NFloat } from '../I18NFloat'
import { createI18NString } from '../I18NString'
import { i18n, unpackCatalog } from 'lingui-i18n'
import { makeExecutableSchema } from 'graphql-tools'

i18n.load({
  fr: unpackCatalog(require('../../../locale/fr/messages.js')),
  en: unpackCatalog(require('../../../locale/en/messages.js')),
})

let schema
describe('Schema Types', () => {
  describe('FoundationFloor', () => {
    beforeEach(() => {
      const FoundationFloor = createFoundationFloor(i18n)
      schema = makeExecutableSchema({
        typeDefs: [FoundationFloor, `scalar I18NFloat`, `scalar String`],
        resolvers: [
          {
            I18NFloat: createI18NFloat(i18n),
            String: createI18NString(i18n),
          },
        ],
      })
    })

    it('is parsable', () => {
      expect(schema.getTypeMap()).toHaveProperty('FoundationFloor')
    })

    it('has the expected fields', () => {
      const { FoundationFloor } = schema.getTypeMap()
      const fields = Object.keys(FoundationFloor.getFields())
      expect(fields).toEqual([
        'floorTypeEnglish',
        'floorTypeFrench',
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
        'lengthMetres',
        'lengthFeet',
      ])
    })
  })
})

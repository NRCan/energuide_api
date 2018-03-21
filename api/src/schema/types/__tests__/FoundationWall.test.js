import { createFoundationWall } from '../FoundationWall'
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
  describe('FoundationWall', () => {
    beforeEach(() => {
      const FoundationWall = createFoundationWall(i18n)
      schema = makeExecutableSchema({
        typeDefs: [FoundationWall, `scalar I18NFloat`, `scalar String`],
        resolvers: [
          {
            I18NFloat: createI18NFloat(i18n),
            String: createI18NString(i18n),
          },
        ],
      })
    })

    it('is parsable', () => {
      expect(schema.getTypeMap()).toHaveProperty('FoundationWall')
    })

    it('has the expected fields', () => {
      const { FoundationWall } = schema.getTypeMap()
      const fields = Object.keys(FoundationWall.getFields())
      expect(fields).toEqual([
        'wallTypeEnglish',
        'wallTypeFrench',
        'insulationNominalRsi',
        'insulationNominalR',
        'insulationEffectiveRsi',
        'insulationEffectiveR',
        'areaMetres',
        'areaFeet',
        'percentage',
      ])
    })
  })
})

import { createHeader } from '../Header'
import { createI18NFloat } from '../I18NFloat'
import { i18n, unpackCatalog } from 'lingui-i18n'
import { makeExecutableSchema } from 'graphql-tools'

i18n.load({
  fr: unpackCatalog(require('../../../locale/fr/messages.js')),
  en: unpackCatalog(require('../../../locale/en/messages.js')),
})
let schema
describe('Schema Types', () => {
  describe('Header', () => {
    beforeEach(() => {
      const Header = createHeader(i18n)
      schema = makeExecutableSchema({
        typeDefs: [Header, `scalar I18NFloat`],
        resolvers: [{I18NFloat: createI18NFloat(i18n)}],
      })
    })

    it('is parsable', () => {
      expect(schema.getTypeMap()).toHaveProperty('Header')
    })

    it('has the expected fields', () => {
      const { Header } = schema.getTypeMap()
      const fields = Object.keys(Header.getFields())
      expect(fields).toEqual([
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
})

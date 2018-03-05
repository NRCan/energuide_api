import { createFoundation } from '../Foundation'
import { createI18NFloat } from '../I18NFloat'
import { createI18NString } from '../I18NString'
import { createFoundationFloor } from '../FoundationFloor'
import { createFoundationWall } from '../FoundationWall'
import { createHeader } from '../Header'
import { i18n, unpackCatalog } from 'lingui-i18n'
import { makeExecutableSchema } from 'graphql-tools'

i18n.load({
  fr: unpackCatalog(require('../../../locale/fr/messages.js')),
  en: unpackCatalog(require('../../../locale/en/messages.js')),
})

let schema
describe('Schema Types', () => {
  describe('Foundation', () => {
    beforeEach(() => {
      schema = makeExecutableSchema({
        typeDefs: [
          createFoundation(i18n),
          `scalar I18NString`,
          `scalar I18NFloat`,
          createFoundationFloor(i18n),
          createFoundationWall(i18n),
          createHeader(i18n),
        ],
        resolvers: [
          {
            I18NFloat: createI18NFloat(i18n),
            I18NString: createI18NString(i18n),
          },
        ],
      })
    })

    it('is parsable', () => {
      expect(schema.getTypeMap()).toHaveProperty('Foundation')
    })

    it('has the expected fields', () => {
      const { Foundation } = schema.getTypeMap()
      const fields = Object.keys(Foundation.getFields())
      expect(fields).toEqual([
        'foundationTypeEnglish',
        'foundationTypeFrench',
        'label',
        'configurationType',
        'materialEnglish',
        'materialFrench',
        'floors',
        'walls',
        'header',
      ])
    })
  })
})

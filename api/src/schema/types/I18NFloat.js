import { GraphQLFloat } from 'graphql'

export const createI18NFloat = i18n => {
  const I18NFloat = Object.create(GraphQLFloat)
  I18NFloat.description = i18n.t`
    The 'Float' scalar type represents signed double-precision fractional
    values as specified by
    [IEEE 754](http://en.wikipedia.org/wiki/IEEE_floating_point).
  `
  return I18NFloat
}

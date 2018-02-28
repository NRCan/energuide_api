import { GraphQLInt } from 'graphql'

export const createI18NInt = i18n => {
  const I18NInt = Object.create(GraphQLInt)
  I18NInt.description = i18n.t`
    The 'Int' scalar type represents non-fractional signed whole numeric
    values. Int can represent values between -(2^31) and 2^31 - 1.
  `
  return I18NInt
}

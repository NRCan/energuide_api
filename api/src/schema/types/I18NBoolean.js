import { GraphQLBoolean } from 'graphql'

export const createI18NBoolean = i18n => {
  const I18NBoolean = Object.create(GraphQLBoolean)
  I18NBoolean.description = i18n.t`
    The 'Boolean' scalar type represents 'true' or 'false'.
  `
  return I18NBoolean
}

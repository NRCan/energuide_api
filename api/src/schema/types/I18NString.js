import { GraphQLString } from 'graphql'

export const createI18NString = i18n => {
  const I18NString = Object.create(GraphQLString)
  I18NString.description = i18n.t`
    The 'String' scalar type represents textual data, represented as UTF-8
    character sequences. The String type is most often used by GraphQL to
    represent free-form human-readable text.
  `
  return I18NString
}

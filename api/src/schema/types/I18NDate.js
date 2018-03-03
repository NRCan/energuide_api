import { GraphQLDate } from 'graphql-iso-date'

export const createI18NDate = i18n => {
  const I18NDate = GraphQLDate
  I18NDate.description = i18n.t`
    'A date string, such as 2007-12-03, compliant with the 'full-date' format
    outlined in section 5.6 of the RFC 3339 profile of the ISO 8601 standard
    for representation of dates and times using the Gregorian calendar.'
  `
  return I18NDate
}

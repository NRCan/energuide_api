import MongoPaging from 'mongo-cursor-pagination'
import { GraphQLError } from 'graphql'

/* eslint-disable import/named */
import {
  dwellingHouseId,
  dwellingYearBuilt,
  dwellingCity,
  dwellingRegion,
  dwellingForwardSortationArea,
  evaluationEvaluationType,
  evaluationFileId,
  evaluationErsRating,
  evaluationHouseType,
  evaluationEntryDate,
  evaluationCreationDate,
  evaluationModificationDate,
} from './enums'
/* eslint-enable import/named */

import { createI18NFloat } from './types/I18NFloat'
import { createI18NInt } from './types/I18NInt'
import { createI18NString } from './types/I18NString'
import { createI18NBoolean } from './types/I18NBoolean'
import { createI18NDate } from './types/I18NDate'

const Resolvers = i18n => {
  return {
    Int: createI18NInt(i18n),
    String: createI18NString(i18n),
    Float: createI18NFloat(i18n),
    Boolean: createI18NBoolean(i18n),
    Date: createI18NDate(i18n),
    Query: {
      dwelling: async (root, { houseId }, { client }) => {
        let query = {
          houseId,
        }

        return client.findOne(query)
      },
      dwellings: async (root, args, { client }) => {
        // TODO: look into the creation & handling of this next param
        // This is an opaque string that passes through the GraphQL type system
        // and is passed directly into library code to be decoded and used while
        // talking to the database.
        // ಠ_ಠ
        const { filters, dateRange, limit, next, previous } = args

        if (next && previous) {
          throw new GraphQLError(
            i18n.t`
              Cannot submit values for both 'next' and 'previous'.
            `,
          )
        }

        let query = {
          $and: [{}],
        }

        if (dateRange) {
          // ISO string format looks like "2012-10-01T15:08:41.000Z"
          const startDateQuery = dateRange.startDate
            ? { $gte: dateRange.startDate.toISOString().split('T')[0] }
            : {}
          const endDateQuery = dateRange.endDate
            ? { $lte: dateRange.endDate.toISOString().split('T')[0] }
            : {}

          const dateQuery = Object.assign({}, startDateQuery, endDateQuery)

          if (Object.keys(dateQuery).length === 0) {
            throw new GraphQLError(
              i18n.t`
                A 'dateRange' must include a 'startDate' or an 'endDate'.
                `,
            )
          }

          if (
            dateQuery['$gte'] &&
            dateQuery['$lte'] &&
            dateQuery['$gte'] >= dateQuery['$lte']
          ) {
            throw new GraphQLError(
              i18n.t`
                The 'endDate' cannot be equal to or earlier than the 'startDate'.
                `,
            )
          }

          // eslint-disable-next-line security/detect-eval-with-expression
          let queryGenerator = eval(dateRange.field) // eslint-disable-line no-eval
          let attrQuery = queryGenerator(dateQuery)
          query['$and'].push(attrQuery)
        }

        if (filters && filters.length > 0) {
          filters.forEach(filter => {
            let value = filter.value
            // if the value is a number
            // - optionally starting with a minus sign
            // - containing zero or one decimal places
            // convert it to a float instead of a string
            if (filter.value.match(/^-?\d+$|^-?\d+\.\d+$/)) {
              value = parseFloat(filter.value)
            }
            // We are evaling our own code here, not user input.
            // Filter.field is our code, stringified and stored in an enum.
            // The user choses one of the enum values and we convert the string
            // back to a function which accepts a matcher and generates the
            // query we need to find that field.
            // eslint-disable-next-line security/detect-eval-with-expression
            let queryGenerator = eval(filter.field) // eslint-disable-line no-eval
            let attrQuery = queryGenerator({
              [filter.comparator]: value,
            })
            query['$and'].push(attrQuery)
          })
        }

        let result = await MongoPaging.find(client, {
          query,
          next,
          previous,
          limit,
        })

        return result
      },
    },
    DateField: {
      evaluationEntryDate: evaluationEntryDate.toString(),
      evaluationCreationDate: evaluationCreationDate.toString(),
      evaluationModificationDate: evaluationModificationDate.toString(),
    },
    Field: {
      dwellingHouseId: dwellingHouseId.toString(),
      dwellingYearBuilt: dwellingYearBuilt.toString(),
      dwellingCity: dwellingCity.toString(),
      dwellingRegion: dwellingRegion.toString(),
      dwellingForwardSortationArea: dwellingForwardSortationArea.toString(),
      evaluationEvaluationType: evaluationEvaluationType.toString(),
      evaluationFileId: evaluationFileId.toString(),
      evaluationErsRating: evaluationErsRating.toString(),
      evaluationHouseType: evaluationHouseType.toString(),
    },
    Comparator: {
      gt: '$gt',
      lt: '$lt',
      eq: '$eq',
    },
  }
}

export { Resolvers }

import ForwardSortationArea from './types/ForwardSortationArea'
import MongoPaging from 'mongo-cursor-pagination'
import { GraphQLError } from 'graphql'
import { comparators, hasMoreThanOneComparator } from '../utilities'
/* eslint-disable import/named */
import {
  dwellingHouseId,
  dwellingYearBuilt,
  dwellingCity,
  dwellingRegion,
  dwellingForwardSortationArea,
  ventilationTypeEnglish,
  ventilationTypeFrench,
  ventilationAirFlowRateLps,
  ventilationAirFlowRateCfm,
  ventilationEfficiency,
} from './enums'
/* eslint-enable import/named */

const resolvers = {
  ForwardSortationArea,
  Query: {
    evaluationsFor: async (root, { account }, { client }) => {
      let query = {
        houseId: account,
      }

      return client.findOne(query)
    },
    dwellingsInFSA: async (root, args, { client }) => {
      // TODO: look into the creation & handling of this next param
      // This is an opaque string that passes through the GraphQL type system
      // and is passed directly into library code to be decoded and used while
      // talking to the database.
      // ಠ_ಠ
      const { filter, forwardSortationArea, limit, next } = args

      if (hasMoreThanOneComparator(filter)) {
        return new GraphQLError(
          `You can only use ${Object.keys(comparators)} one at a time`,
        )
      }

      let query = {
        $and: [
          {
            forwardSortationArea,
          },
        ],
      }

      if (filter) {
        for (let key in filter) {
          // make sure the key exists in the comparators' keys
          if (Object.keys(comparators).includes(key)) {
            // if the value is a number
            // - optionally starting with a minus sign
            // - containing zero or one decimal places
            // convert it to a float instead of a string
            if (filter[key].match(/^-?\d+\.?\d+$/)) {
              filter[key] = parseFloat(filter[key])
            }

            // We are evaling our own code here, not user input.
            // Filter.field is our code, stringified and stored in an enum.
            // The user choses one of the enum values and we convert the string
            // back to a function which accepts a matcher and generates the
            // query we need to find that field.
            // eslint-disable-next-line no-eval
            let queryGenerator = eval(filter.field)
            let attrQuery = queryGenerator({
              [comparators[key]]: filter[key],
            })
            query['$and'].push(attrQuery)
          }
        }
      }

      let result = await MongoPaging.find(client, {
        query,
        next,
        limit,
      })

      return result
    },
  },
  Field: {
    dwellingHouseId: dwellingHouseId.toString(),
    dwellingYearBuilt: dwellingYearBuilt.toString(),
    dwellingCity: dwellingCity.toString(),
    dwellingRegion: dwellingRegion.toString(),
    dwellingForwardSortationArea: dwellingForwardSortationArea.toString(),
    ventilationTypeEnglish: ventilationTypeEnglish.toString(),
    ventilationTypeFrench: ventilationTypeFrench.toString(),
    ventilationAirFlowRateLps: ventilationAirFlowRateLps.toString(),
    ventilationAirFlowRateCfm: ventilationAirFlowRateCfm.toString(),
    ventilationEfficiency: ventilationEfficiency.toString(),
  },
}

export default resolvers

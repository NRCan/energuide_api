import ForwardSortationArea from './types/ForwardSortationArea'
import MongoPaging from 'mongo-cursor-pagination'
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

      let query = {
        $and: [
          {
            forwardSortationArea,
          },
        ],
      }

      if (filter) {
        let value = filter.value
        // if the value is a number
        // - optionally starting with a minus sign
        // - containing zero or one decimal places
        // convert it to a float instead of a string
        if (filter.value.match(/^-?\d+\.?\d+$/)) {
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
  Comparator: {
    gt: '$gt',
    lt: '$lt',
    eq: '$eq',
  },
}

export default resolvers

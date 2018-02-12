import ForwardSortationArea from './types/ForwardSortationArea'
import MongoPaging from 'mongo-cursor-pagination'
import { GraphQLError } from 'graphql'
import {
  comparators,
  createQuery,
  hasMoreThanOneComparator,
} from '../utilities'

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

      let query = createQuery(forwardSortationArea, filter)

      let result = await MongoPaging.find(client, {
        query,
        next,
        limit,
      })

      return result
    },
  },
  Field: {
    houseId: 'houseId',
    yearBuilt: 'yearBuilt',
    city: 'city',
    region: 'region',
    forwardSortationArea: 'forwardSortationArea',
  },
}

export default resolvers

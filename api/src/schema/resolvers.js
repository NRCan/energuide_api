import ForwardSortationArea from './types/ForwardSortationArea'
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
      const { filter, forwardSortationArea } = args

      if (hasMoreThanOneComparator(filter)) {
        return new GraphQLError(
          `You can only use ${Object.keys(comparators)} one at a time`,
        )
      }

      let query = createQuery(forwardSortationArea, filter)

      let cursor = await client.find(query)

      return cursor.toArray()
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

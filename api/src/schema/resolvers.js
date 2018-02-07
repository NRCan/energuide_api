import PostalCode from './types/PostalCode'
import ForwardSortationArea from './types/ForwardSortationArea'
import { GraphQLError } from 'graphql'
import {
  comparators,
  createQuery,
  hasMoreThanOneComparator,
} from '../utilities'

const resolvers = {
  PostalCode,
  ForwardSortationArea,
  Query: {
    evaluationsFor: async (root, { account, postalCode }, { client }) => {
      let query = {
        houseId: account,
        // XXX This is a temporary hack to work around the lack of postal codes in the data.
        forwardSortationArea: postalCode.split(' ')[0],
      }

      let cursor = await client.find(query)

      let results = await cursor.toArray()
      return results[0] // XXX: clean this up too.
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

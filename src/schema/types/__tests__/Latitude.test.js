import Latitude from '../Latitude'
import {
  graphql,
  GraphQLSchema,
  GraphQLObjectType,
  GraphQLString,
  GraphQLNonNull,
} from 'graphql'

var testSchema = new GraphQLSchema({
  query: new GraphQLObjectType({
    name: 'Root',
    fields: {
      test: {
        type: GraphQLString,
        args: {
          lat: {
            type: new GraphQLNonNull(Latitude),
          },
        },
        resolve: (source, { lat }, root, ast) => {
          return lat
        },
      },
    },
  }),
})

describe('Latitude Type', () => {
  describe('parseLiteral', () => {
    it('accepts latitudes supplied as Float literals', async () => {
      let query = `{
         test(lat: 45.421106)
        }`

      let results = await graphql(testSchema, query)
      expect(results.data.test).toEqual('45.421106')
    })

    it('Accepts latitudes supplied as integer literals', async () => {
      let query = `{
         test(lat: 45)
        }`

      let results = await graphql(testSchema, query)
      expect(results.data.test).toEqual('45')
    })

    it('rejects latitudes supplied as string literals', async () => {
      let query = `{
         test(lat: "45.0")
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })

    it('rejects latitudes lower than -90', async () => {
      let query = `{
         test(lat: -91.0)
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })

    it('rejects latitudes higher than 90', async () => {
      let query = `{
         test(lat: 91.0)
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })
  })

  describe('parseValue', () => {
    it('accepts latitudes supplied as Float values', async () => {
      let query = `query test($lat: Latitude!) {
         test(lat: $lat)
        }`

      let results = await graphql(testSchema, query, {}, {}, { lat: 45.421106 })
      expect(results.data.test).toEqual('45.421106')
    })

    it('Accepts latitudes supplied as integer values', async () => {
      let query = `query test($lat: Latitude!) {
         test(lat: $lat)
        }`

      let results = await graphql(testSchema, query, {}, {}, { lat: 45 })
      expect(results.data.test).toEqual('45')
    })

    it('rejects latitudes supplied as string literals', async () => {
      let query = `query test($lat: Latitude!) {
         test(lat: "45.0")
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })

    it('rejects latitudes lower than -90', async () => {
      let query = `{
         test(lat: -91.0)
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })

    it('rejects latitudes higher than 90', async () => {
      let query = `{
         test(lat: 91.0)
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })
  })
})

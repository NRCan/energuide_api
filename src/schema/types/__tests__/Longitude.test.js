import Longitude from '../Longitude'
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
          lng: {
            type: new GraphQLNonNull(Longitude),
          },
        },
        resolve: (source, { lng }, root, ast) => {
          return lng
        },
      },
    },
  }),
})

describe('Longitude Type', () => {
  describe('parseLiteral', () => {
    it('accepts longitude literals supplied as float', async () => {
      let query = `{
         test(lng: -75.690308)
        }`

      let results = await graphql(testSchema, query)
      expect(results.data.test).toEqual('-75.690308')
    })

    it('accepts longitude literals supplied as integers', async () => {
      let query = `{
         test(lng: -75.690308)
        }`

      let results = await graphql(testSchema, query)
      expect(results.data.test).toEqual('-75.690308')
    })

    it('rejects longitude literals supplied as strings', async () => {
      let query = `{
         test(lng: "-75.690308")
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })

    it('rejects longitude literals lower than -180', async () => {
      let query = `{
         test(lng: -181.0)
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })

    it('rejects longitude literals higher than 180', async () => {
      let query = `{
         test(lng: 181.0)
        }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })
  })

  describe('parseValue', () => {
    it('accepts longitude values supplied as floats', async () => {
      let query = `query test($lng: Longitude!) {
         test(lng: $lng)
        }`

      let results = await graphql(testSchema, query, {}, {}, { lng: -75.690308 })
      expect(results.data.test).toEqual('-75.690308')
    })

    it('Accepts longitude values supplied as integers', async () => {
      let query = `query test($lng: Longitude!) {
         test(lng: $lng)
        }`

      let results = await graphql(testSchema, query, {}, {}, { lng: -75.690308 })
      expect(results.data.test).toEqual('-75.690308')
    })

    it('rejects longitude values supplied as strings', async () => {
      let query = `query test($lng: Longitude!) {
         test(lng: $lng)
        }`

      let results = await graphql(testSchema, query, {}, {}, { lng: "-75.690308" })
      expect(results).toHaveProperty('errors')
    })

    it('rejects longitude values lower than -180', async () => {
      let query = `query test($lng: Longitude!) {
         test(lng: $lng)
        }`

      let results = await graphql(testSchema, query, {}, {}, { lng: -181.01 })
      expect(results).toHaveProperty('errors')
    })

    it('rejects longitude values higher than 180', async () => {
      let query = `query test($lng: Longitude!) {
         test(lng: 181.0)
        }`

      let results = await graphql(testSchema, query, {}, {}, { lng: 181.01 })
      expect(results).toHaveProperty('errors')
    })
  })
})

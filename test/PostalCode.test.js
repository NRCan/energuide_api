import PostalCode from '../src/schema/types/PostalCode'
import {
  graphql,
  GraphQLSchema,
  GraphQLObjectType,
  GraphQLString,
} from 'graphql'

var testSchema = new GraphQLSchema({
  query: new GraphQLObjectType({
    name: 'Root',
    fields: {
      test: {
        type: GraphQLString,
        args: {
          postalCode: {
            type: PostalCode,
          },
        },
        resolve: (source, { postalCode }, root, ast) => {
          return postalCode
        },
      },
    },
  }),
})

describe('PostalCode Type', () => {
  it('cheerfully accepts a properly formated postal code', async () => {
    let query = `{
         test(postalCode: "M8H 1N1")
        }`

    let { data: { test } } = await graphql(testSchema, query)

    expect(test).toEqual('M8H 1N1')
  })

  describe('rejects literals with invalid characters', () => {
    const forbiddenLetters = [...'DFIOQU']
    forbiddenLetters.forEach(forbiddenLetter => {
      it(`rejects a postal code that include the letter ${forbiddenLetter}`, async () => {
        let query = `{
         test(postalCode: "M8${forbiddenLetter} 1N1")
      }`

        let result = await graphql(testSchema, query)

        expect(result).toHaveProperty('errors')
      })
    })

    const cannotStart = [...'WZ']
    cannotStart.forEach(forbiddenLetter => {
      it(`rejects a postal code that start with the letter ${forbiddenLetter}`, async () => {
        let query = `{
         test(postalCode: "${forbiddenLetter}8H 1N1")
      }`

        let result = await graphql(testSchema, query)

        expect(result).toHaveProperty('errors')
      })
    })
  })

  describe('rejects values with invalid characters', () => {
    const forbiddenLetters = [...'DFIOQU']
    forbiddenLetters.forEach(forbiddenLetter => {
      it(`rejects a postal code that include the letter ${forbiddenLetter}`, async () => {
        let query = `query($pc: PostalCode!) {
         test(postalCode: $pc)
      }`

        let result = await graphql(
          testSchema,
          query,
          {},
          { pc: `M8${forbiddenLetter} 1N1` },
        )

        expect(result).toHaveProperty('errors')
      })
    })

    const cannotStart = [...'WZ']
    cannotStart.forEach(forbiddenLetter => {
      it(`rejects a postal code that start with the letter ${forbiddenLetter}`, async () => {
        let query = `query($pc: PostalCode!) {
         test(postalCode: $pc)
      }`

        let result = await graphql(
          testSchema,
          query,
          {},
          { pc: `${forbiddenLetter}8H 1N1` },
        )

        expect(result).toHaveProperty('errors')
      })
    })
  })
})

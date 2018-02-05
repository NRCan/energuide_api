import PostalCode from '../src/schema/types/PostalCode'
import {
  graphql,
  GraphQLSchema,
  GraphQLObjectType,
  GraphQLString,
  GraphQLNonNull,
} from 'graphql'

const testSchema = new GraphQLSchema({
  query: new GraphQLObjectType({
    name: 'Root',
    fields: {
      test: {
        type: GraphQLString,
        args: {
          postalCode: {
            type: new GraphQLNonNull(PostalCode),
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
  describe('parseLiteral', () => {
    it('accepts proper postal codes supplied as literals', async () => {
      let query = `{ test(postalCode: "M8H 1N1") }`

      let results = await graphql(testSchema, query)
      expect(results.data.test).toEqual('M8H 1N1')
    })

    it('rejects invalid codes supplied as literals', async () => {
      let query = `{ test(postalCode: "DDD DDD") }`

      let results = await graphql(testSchema, query)
      expect(results).toHaveProperty('errors')
    })

    describe('rejects literals with invalid characters', () => {
      const forbiddenLetters = [...'DFIOQU']
      forbiddenLetters.forEach(forbiddenLetter => {
        it(`rejects a postal code that include the letter ${forbiddenLetter}`, async () => {
          let query = `{ test(postalCode: "M8${forbiddenLetter} 1N1") } `

          let result = await graphql(testSchema, query)

          expect(result).toHaveProperty('errors')
        })
      })

      const cannotStart = [...'WZ']
      cannotStart.forEach(forbiddenLetter => {
        it(`rejects a postal code that start with the letter ${forbiddenLetter}`, async () => {
          let query = `{ test(postalCode: "${forbiddenLetter}8H 1N1") }`

          let result = await graphql(testSchema, query)

          expect(result).toHaveProperty('errors')
        })
      })
    })
  })

  describe('parseValue', () => {
    it('accepts postal codes supplied as values', async () => {
      let query = `
        query test_query($pc: PostalCode!) {
          test(postalCode: $pc)
        }
      `

      let results = await graphql(testSchema, query, {}, {}, { pc: 'M8H 1N1' })
      expect(results.data.test).toEqual('M8H 1N1')
    })

    it('has a parseValue function that properly validates variables', async () => {
      let query = `
        query test_query($pc: PostalCode!) {
          test(postalCode: $pc)
        }
      `

      let results = await graphql(testSchema, query, {}, {}, { pc: 'DDD DDD' })
      expect(results).toHaveProperty('errors')
    })

    describe('rejects values with invalid characters', () => {
      const forbiddenLetters = [...'DFIOQU']
      forbiddenLetters.forEach(forbiddenLetter => {
        it(`rejects a postal code that include the letter ${forbiddenLetter}`, async () => {
          let query = `
            query($pc: PostalCode!) {
              test(postalCode: $pc)
            }
          `

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
          let query = `
            query($pc: PostalCode!) {
              test(postalCode: $pc)
            }
          `

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
})

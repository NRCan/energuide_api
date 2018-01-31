import ForwardSortationArea from '../src/schema/types/ForwardSortationArea'
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
          forwardSortationArea: {
            type: new GraphQLNonNull(ForwardSortationArea),
          },
        },
        resolve: (source, { forwardSortationArea }, root, ast) => {
          return forwardSortationArea
        },
      },
    },
  }),
})

describe('ForwardSortationArea Type', () => {
  describe('parseLiteral', () => {
    it('cheerfully accepts a proper FSA literal', async () => {
      let query = `{
         test(forwardSortationArea: "M8H")
        }`

      let { data: { test } } = await graphql(testSchema, query)

      expect(test).toEqual('M8H')
    })

    it('rejects invalid FSA literals', async () => {
      let query = `{
         test(forwardSortationArea: "DDD")
        }`

      let results = await graphql(testSchema, query)

      expect(results).toHaveProperty('errors')
    })

    describe('rejects literals that include invalid characters', () => {
      const forbiddenLetters = [...'DFIOQU']
      forbiddenLetters.forEach(forbiddenLetter => {
        it(`rejects an FSA literals that includes the letter ${forbiddenLetter}`, async () => {
          let query = `query {
            test(forwardSortationArea: "M8${forbiddenLetter}")
          }`

          let result = await graphql(testSchema, query)

          expect(result).toHaveProperty('errors')
        })
      })

      const cannotStart = [...'WZ']
      cannotStart.forEach(forbiddenLetter => {
        it(`rejects an FSA values that starts with the letter ${forbiddenLetter}`, async () => {
          let query = `query($fsa: ForwardSortationArea!) {
            test(forwardSortationArea: $fsa)
          }`

          let result = await graphql(testSchema, query)

          expect(result).toHaveProperty('errors')
        })
      })
    })
  })

  describe('parseValue', () => {
    it('cheerfully accepts a proper FSA value', async () => {
      let query = `query test($fsa: ForwardSortationArea!) {
         test(forwardSortationArea: $fsa)
        }`

      let { data: { test } } = await graphql(
        testSchema,
        query,
        {},
        {},
        { fsa: 'M8H' },
      )

      expect(test).toEqual('M8H')
    })

    it('rejects invalid FSA values', async () => {
      let query = `query test($fsa: ForwardSortationArea!) {
         test(forwardSortationArea: $fsa)
        }`

      let results = await graphql(testSchema, query, {}, {}, { fsa: 'DDD' })

      expect(results).toHaveProperty('errors')
    })

    describe('rejects values that include invalid characters', () => {
      const forbiddenLetters = [...'DFIOQU']
      forbiddenLetters.forEach(forbiddenLetter => {
        it(`rejects an FSA values that includes the letter ${forbiddenLetter}`, async () => {
          let query = `query($fsa: ForwardSortationArea!) {
         test(forwardSortationArea: $fsa)
      }`

          let result = await graphql(
            testSchema,
            query,
            {},
            {},
            { pc: `M8${forbiddenLetter}` },
          )

          expect(result).toHaveProperty('errors')
        })
      })

      const cannotStart = [...'WZ']
      cannotStart.forEach(forbiddenLetter => {
        it(`rejects an FSA values that starts with the letter ${forbiddenLetter}`, async () => {
          let query = `query($fsa: ForwardSortationArea!) {
         test(forwardSortationArea: $fsa)
      }`

          let result = await graphql(
            testSchema,
            query,
            {},
            {},
            { pc: `${forbiddenLetter}8H` },
          )

          expect(result).toHaveProperty('errors')
        })
      })
    })
  })

  it('does not accept a full postal code', async () => {
    let query = `{
         test(forwardSortationArea: "K1C 2J5")
        }`

    let response = await graphql(testSchema, query)

    expect(response).toHaveProperty('errors')
  })

})

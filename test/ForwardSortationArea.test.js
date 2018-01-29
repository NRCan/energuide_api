import ForwardSortationArea from '../src/schema/types/ForwardSortationArea'
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
          forwardSortationArea: {
            type: ForwardSortationArea,
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
  it('cheerfully accepts a proper FSA', async () => {
    let query = `{
         test(forwardSortationArea: "M8H")
        }`

    let { data: { test } } = await graphql(testSchema, query)

    expect(test).toEqual('M8H')
  })

  it('does not accept a full postal code', async () => {
    let query = `{
         test(forwardSortationArea: "K1C 2J5")
        }`

    let response = await graphql(testSchema, query)

    expect(response).toHaveProperty('errors')
  })

  describe('rejects literals with invalid characters', () => {
    const forbiddenLetters = [...'DFIOQU']
    forbiddenLetters.forEach(forbiddenLetter => {
      it(`rejects an FSA that includes the letter ${forbiddenLetter}`, async () => {
        let query = `{
         test(forwardSortationArea: "M8${forbiddenLetter}")
      }`

        let result = await graphql(testSchema, query)

        expect(result).toHaveProperty('errors')
      })
    })

    const cannotStart = [...'WZ']
    cannotStart.forEach(forbiddenLetter => {
      it(`rejects an FSA that starts with the letter ${forbiddenLetter}`, async () => {
        let query = `{
         test(forwardSortationArea: "${forbiddenLetter}8H")
      }`

        let result = await graphql(testSchema, query)

        expect(result).toHaveProperty('errors')
      })
    })
  })

  describe('rejects values with invalid characters', () => {
    const forbiddenLetters = [...'DFIOQU']
    forbiddenLetters.forEach(forbiddenLetter => {
      it(`rejects an FSA that includes the letter ${forbiddenLetter}`, async () => {
        let query = `query($fsa: ForwardSortationArea!) {
         test(forwardSortationArea: $fsa)
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
      it(`rejects an FSA that starts with the letter ${forbiddenLetter}`, async () => {
        let query = `query($fsa: ForwardSortationArea!) {
         test(forwardSortationArea: $fsa)
      }`

        let result = await graphql(
          testSchema,
          query,
          {},
          { pc: `${forbiddenLetter}8H` },
        )

        expect(result).toHaveProperty('errors')
      })
    })
  })
})


import request from 'supertest'
import Server from '../server'
import {
  GraphQLInt,
  GraphQLFloat,
  GraphQLString,
  GraphQLBoolean,
} from 'graphql'
import { GraphQLDate } from 'graphql-iso-date'

let mockServer = new Server({
  client: jest.fn(),
})

const makeRequest = function({ typeName, server = mockServer, lang = 'en' }) {
  let req = request(server)
    .post('/graphql')
    .set('Content-Type', 'application/json; charset=utf-8')

  if (lang) {
    req.set('Accept-Language', lang)
  }

  return req.send({
    query: `query {
       __type(name: "${typeName}") {
         name
         description
       }
    }`,
  })
}

const replaceBackTicksWithSingleQuotes = function(str) {
  return str.replace(/`/g, "'").trim()
}

describe('configuration', () => {
  describe('graphql default scalar value', () => {
    it('GraphQLInt returns the same description as I18NInt', async () => {
      let response = await makeRequest({ typeName: 'Int' })

      let { __type: { name, description } } = response.body.data
      expect(name).toEqual(GraphQLInt.name)
      expect(description).toEqual(
        replaceBackTicksWithSingleQuotes(GraphQLInt.description),
      )
    })

    it('GraphQLFloat returns the same description as I18NFloat', async () => {
      let response = await makeRequest({ typeName: 'I18NFloat' })

      let { __type: { description } } = response.body.data
      expect(description).toEqual(
        replaceBackTicksWithSingleQuotes(GraphQLFloat.description),
      )
    })

    it('GraphQLString returns the same description as I18NString', async () => {
      let response = await makeRequest({ typeName: 'String' })

      let { __type: { name, description } } = response.body.data
      expect(name).toEqual(GraphQLString.name)
      expect(description).toEqual(
        replaceBackTicksWithSingleQuotes(GraphQLString.description),
      )
    })

    it('GraphQLBoolean returns the same description as I18NBoolean', async () => {
      let response = await makeRequest({ typeName: 'Boolean' })

      let { __type: { name, description } } = response.body.data
      expect(name).toEqual(GraphQLBoolean.name)
      expect(description).toEqual(
        replaceBackTicksWithSingleQuotes(GraphQLBoolean.description),
      )
    })
  })

  describe('graphql iso date field', () => {
    it('GraphQLDate returns the same description as I18NDate', async () => {
      let response = await makeRequest({ typeName: 'Date' })

      let { __type: { name, description } } = response.body.data
      // name is overwritten (we are not using Object.create()) so this assertion is useless
      // expect(name).toEqual(GraphQLDate.name)
      expect(description).toEqual(
        replaceBackTicksWithSingleQuotes(GraphQLDate.description),
      )
    })
  })

  describe('i18n', () => {
    it('returns french description when french language header sent', async () => {
      let response = await makeRequest({ typeName: 'Evaluation', lang: 'fr' })

      let { __type: { description } } = response.body.data

      expect(description).toEqual(
        "Informations détaillées sur les caractéristiques spécifiques d'un logement donné",
      )
    })

    it('returns english description when english language header sent', async () => {
      let response = await makeRequest({ typeName: 'Evaluation', lang: 'en' })

      let { __type: { description } } = response.body.data
      expect(description).toEqual(
        'Detailed information about specific features of a given dwelling',
      )
    })

    it('defaults to english if no language header is set', async () => {
      let response = await makeRequest({ typeName: 'Evaluation', lang: '' })

      let { __type: { description } } = response.body.data
      expect(description).toEqual(
        'Detailed information about specific features of a given dwelling',
      )
    })
  })
})

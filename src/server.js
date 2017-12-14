import express from 'express'
import bodyParser from 'body-parser'
import { graphqlExpress, graphiqlExpress } from 'apollo-server-express'
import { makeExecutableSchema } from 'graphql-tools'
import Schema from './schema'
import { i18n , unpackCatalog } from 'lingui-i18n'
import requestLanguage from 'express-request-language'

i18n.load({ 
  fr: unpackCatalog(require('./locale/fr/messages.js')),
  en: unpackCatalog(require('./locale/en/messages.js')),
})

function Server(context = {}) {
  const server = express()
  server
  .use(
    requestLanguage({
      languages: i18n.availableLanguages.sort(),
    }),
  )
  .use(
    '/graphql',
    bodyParser.json(),
    graphqlExpress(request => {
      i18n.activate(request.language)
      return {
        schema: new Schema(i18n),
        context,
      }
    }),
  )
  server.get('/graphiql', graphiqlExpress({ endpointURL: '/graphql' }))
  return server
}

export default Server

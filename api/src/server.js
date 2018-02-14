import express from 'express'
import bodyParser from 'body-parser'
import cors from 'cors'
import { graphqlExpress, graphiqlExpress } from 'apollo-server-express'
import Schema from './schema'
import { i18n, unpackCatalog } from 'lingui-i18n'
import requestLanguage from 'express-request-language'

i18n.load({
  fr: unpackCatalog(require('./locale/fr/messages.js')),
  en: unpackCatalog(require('./locale/en/messages.js')),
})

function Server(context = {}, ...middlewares) {
  const server = express()
  middlewares.forEach(middleware => server.use(middleware))
  server
    .use(
      requestLanguage({
        languages: i18n.availableLanguages.sort(),
      }),
    )
    .use(cors())
    .use(
      '/graphql',
      bodyParser.json(),
      graphqlExpress(request => {
        i18n.activate(request.language)
        return {
          schema: new Schema(i18n),
          context,
          tracing: true,
          cacheControl: true,
        }
      }),
    )
  server.get('/graphiql', graphiqlExpress({ endpointURL: '/graphql' }))

  // TODO: Remove after demo is over (which is easy because we are super agile)
  server.get('/welcome', function(req, res) {
    res.send(
      '<h1 style="font-size:2.5em;">Welcome to the super agile <strong style="color:inherited;">ENER-CAN API</strong>!</h1>',
    )
  })

  return server
}

export default Server

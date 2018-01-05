import { MongoClient } from 'mongodb'
import Server from './server'
import { Engine } from 'apollo-engine'

const apiKey = process.env.NRCAN_ENGINE_API_KEY
if (!apiKey) throw new Error('No Apollo Engine API key was found in the ENV.')

const engine = new Engine({
  engineConfig: {
    apiKey,
    logging: {
      level: 'ERROR',
    },
  },
  graphqlPort: 3000,
  endpoint: '/graphql',
  frontend: {
    extensions: {
      strip: ['cacheControl', 'tracing'], // Extensions to remove from responses served to clients
    },
  },
})

const url = process.env.NRCAN_DB_CONNECTION_STRING
if (!url) throw new Error('No DB connection string found in the ENV.')

MongoClient.connect(url)
  .then(async client => {
    // start Apollo Engine
    await engine.start()
    const db = client.db('nrcan_api')
    const collection = db.collection('buildings')
    const server = new Server(
      {
        client: collection,
      },
      engine.expressMiddleware(),
    )
    server.listen(3000)
  })
  .catch(console.log)

process.on('exit', function() {
  engine.stop()
})

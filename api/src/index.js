import { MongoClient } from 'mongodb'
import Server from './server'
import { ApolloEngine } from 'apollo-engine'

const apiKey = process.env.NRCAN_ENGINE_API_KEY
if (!apiKey) throw new Error('No Apollo Engine API key was found in the ENV.')

const engine = new ApolloEngine({
  apiKey,
})

const url = process.env.NRCAN_DB_CONNECTION_STRING
if (!url)
  throw new Error('NRCAN_DB_CONNECTION_STRING was not defined in the ENV.')

const dbName = process.env.NRCAN_DB_NAME
if (!dbName) throw new Error('NRCAN_DB_NAME was not defined in the ENV.')

const collectionName = process.env.NRCAN_COLLECTION_NAME
if (!dbName)
  throw new Error('NRCAN_COLLECTION_NAME was not defined in the ENV.')

MongoClient.connect(url)
  .then(async client => {
    // start Apollo Engine
    const db = client.db(dbName)
    const collection = db.collection(collectionName)
    const server = new Server({
      client: collection,
    })

    engine.listen({
      port: 3000,
      graphqlPaths: ['/graphql'],
      expressApp: server,
      launcherOptions: {
        startupTimeout: 3000,
      },
    })
  })
  .catch(console.log)

process.on('exit', function() {
  engine.stop()
})

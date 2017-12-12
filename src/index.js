import sql from 'mssql'
import Server from './server'
import { Engine } from 'apollo-engine'

const engine = new Engine({
  engineConfig: {
    apiKey: process.env.NRCAN_ENGINE_API_KEY,
    logging: {
      level: 'DEBUG', // Engine Proxy logging level. DEBUG, INFO, WARN or ERROR
    },
  },
  graphqlPort: 3000,
  endpoint: '/graphql', // GraphQL endpoint suffix - '/graphql' by default
  dumpTraffic: true, // Debug configuration that logs traffic between Proxy and GraphQL server
  frontend: {
    extensions: {
      // Configuration for GraphQL response extensions
      strip: ['cacheControl', 'tracing'], // Extensions to remove from responses served to clients
    },
  },
})

const config = {
  user: process.env.NRCAN_API_USERNAME,
  password: process.env.NRCAN_API_PASSWORD,
  server: process.env.NRCAN_API_HOST,
  database: process.env.NRCAN_API_DATABASE,
  options: {
    encrypt: true,
  },
}

sql
  .connect(config)
  .then(async connection => {
    await engine.start()
    const server = new Server(
      {
        sql,
      },
      engine.expressMiddleware(),
    )
    server.listen(3000)
  })
  .catch(console.log)

process.on('exit', function() {
  engine.stop()
})

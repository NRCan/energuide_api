import sql from 'mssql'
import Server from './server'
import { Engine } from 'apollo-engine'

const engine = new Engine({
  engineConfig: {
    apiKey: process.env.NRCAN_ENGINE_API_KEY,
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

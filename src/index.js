import sql from 'mssql'
import Server from './server'

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
  .then(connection => {
    const server = new Server({
      sql,
    })
    server.listen(3000)
  })
  .catch(console.log)

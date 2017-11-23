import request from 'supertest'
import sql from 'mssql'
import Server from '../src/server'
import data from './data'

const config = {
  user: process.env.NRCAN_API_USERNAME,
  password: process.env.NRCAN_API_PASSWORD,
  server: process.env.NRCAN_API_HOST,
  database: 'nrcan_test',
}

let pool

describe('Server', () => {
  beforeAll(async () => {
    pool = await sql.connect(config)
  })

  beforeEach(async () => {
    try {
      const transaction = pool.transaction()
      await transaction.begin()
      let request = transaction.request()
      await request.query(data)
      await transaction.commit()
    } catch (e) {
      console.log(e)
    }
  })

  afterEach(async () => {
    try {
      const transaction = pool.transaction()
      await transaction.begin()
      let request = transaction.request()
      await request.batch('truncate table new_evaluationBase')
      await request.batch('truncate table new_homeownerBase')
      await transaction.commit()
    } catch (e) {
      console.log(e)
    }
  })


  afterAll(async () => {
    // https://github.com/patriksimek/node-mssql/issues/457
    pool.close()
  })

  it('has GraphQL middleware mounted at /graphql', async () => {
    let server = new Server({
      sql,
    })

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `{ 
        __schema {
          queryType { 
            fields {
              name
            }
          }
        }
      }`,
      })

    expect(response.status).toEqual(200)
  })

  it('returns evaluations with nicely camel-cased names', async () => {
    let server = new Server({
      sql,
    })

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `{ 
        evaluations {
          yearBuilt
        }
      }`,
      })

    let { evaluations } = response.body.data
    expect(evaluations[0].yearBuilt).toEqual('2010')
  })
})

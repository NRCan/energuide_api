import { MongoClient } from 'mongodb'
import request from 'supertest'
import Server from '../src/server'
import testData from './data'

let client, db, collection
const url = 'mongodb://localhost:27017'
// const url = process.env.COSMOSDB_URL
const dbName = 'nrcan_test'

describe('Server', () => {
  beforeEach(async () => {
    client = await MongoClient.connect(url)
    db = client.db(dbName)
    collection = db.collection('buildings')
    // CosmosDB apparently automatically indexes everything
    // but for Mongo we need to add an index
    await collection.createIndex({ location: '2dsphere' })
  })

  afterEach(async () => {
    await collection.remove()
    client.close()
  })

  it('has GraphQL middleware mounted at /graphql', async () => {
    let server = new Server({
      client,
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

  it('has Cross Origin Resource Sharing enabled for all domains', async () => {
    let server = Server()

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

    let { headers } = response
    expect(headers['access-control-allow-origin']).toEqual('*')
  })

  it('returns evaluations with nicely camel-cased names', async () => {
    await collection.insertMany(testData)

    let server = new Server({
      client: collection,
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

    let { evaluations: [first] } = response.body.data
    expect(first.yearBuilt).toEqual('1980')
  })

})

describe('Description language', () => {
  it('returns french description when french language header sent', async () => {
    let lang = 'fr'
    let server = Server()

    let response = await request(server)
      .post('/graphql')
      .set('Accept-Language', lang)
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `query {
           __type(name: "Evaluation") {
             name
             description
           }
        }`,
      })

    let { __type: { description } } = response.body.data
    expect(description).toEqual('Ceci est une description des évaluations')
  })

  it('returns english description when english language header sent', async () => {
    let lang = 'en'
    let server = Server()

    let response = await request(server)
      .post('/graphql')
      .set('Accept-Language', lang)
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `query {
           __type(name: "Evaluation") {
             name
             description
           }
        }`,
      })

    let { __type: { description } } = response.body.data
    expect(description).toEqual('This is a description of evaluations')
  })

  it('defaults to english if no language header is set', async () => {
    let server = Server()

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `query {
           __type(name: "Evaluation") {
             name
             description
           }
        }`,
      })

    let { __type: { description } } = response.body.data
    expect(description).toEqual('This is a description of evaluations')
  })
})

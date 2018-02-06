import { MongoClient } from 'mongodb'
import request from 'supertest'
import Server from '../src/server'
import testData from './data'

let client, db, collection
const url = 'mongodb://localhost:27017'
const dbName = 'test_' + Date.now()

describe('queries', () => {
  beforeEach(async () => {
    client = await MongoClient.connect(url)
    db = client.db(dbName)
    collection = db.collection('buildings')
  })

  afterEach(async () => {
    await db.dropDatabase()
    client.close()
  })

  it('retrieves evaluations given an account id and a postalcode', async () => {
    await collection.insertMany(testData)

    let server = new Server({
      client: collection,
    })

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `{
         evaluationsFor(account: 761266 postalCode: "M8H 1N1") {
          yearBuilt
          mailingAddressPostalCode
        }
      }`,
      })

    let { evaluationsFor } = response.body.data
    expect(evaluationsFor.yearBuilt).toEqual('1980')
  })

  it('filters the results', async () => {
    await collection.insertMany(testData)

    let server = new Server({
      client: collection,
    })

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `{
         evaluationsInFSA(
           forwardSortationArea: "M8H"
           filter: {field: yearBuilt gt: "1979"}
         ) {
          yearBuilt
          mailingAddressPostalCode
        }
      }`,
      })

    let { evaluationsInFSA: [first] } = response.body.data
    expect(first.yearBuilt).toEqual('1980')
  })

  it('complains about multiple comparators', async () => {

    await collection.insertMany(testData)

    let server = new Server({
      client: collection,
    })

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `{
         evaluationsInFSA(
           forwardSortationArea: "M8H"
           filter: {field: yearBuilt gt: "1979" lt: "1979"}
         ) {
          yearBuilt
          mailingAddressPostalCode
        }
      }`,
      })
    expect(response.body).toHaveProperty('errors')
  })

  it('gets evalutations within a Forward Sortation Area', async () => {

    await collection.insertMany(testData)

    let server = new Server({
      client: collection,
    })

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `{
           evaluations:evaluationsInFSA(
             forwardSortationArea: "M8H"
           ) {
          yearBuilt
        }
      }`,
      })

    let { evaluations: [first] } = response.body.data
    expect(first.yearBuilt).toEqual('1980')
  })
})

import { MongoClient } from 'mongodb'
import request from 'supertest'
import Server from '../src/server'
import testData from './data'

let client, db, collection
const url = 'mongodb://localhost:27017'
// const url = process.env.COSMOSDB_URL
const dbName = 'test_' + Date.now()

describe('queries', () => {
  beforeEach(async () => {
    client = await MongoClient.connect(url)
    db = client.db(dbName)
    collection = db.collection('buildings')
    // CosmosDB apparently automatically indexes everything
    // but for Mongo we need to add an index
    await collection.createIndex({ location: '2dsphere' })
  })

  afterEach(async () => {
    await db.dropDatabase()
    // for COSMOSDB you will want to use:
    // await collection.remove()
    client.close()
  })

  it('returns evaluations with nicely camel-cased names', async () => {
    let geocoded = testData.slice()
    geocoded[0].location = {
      type: 'Point',
      coordinates: [-79.348650200148, 43.8036022863624],
    }

    await collection.insertMany(geocoded)

    let server = new Server({
      client: collection,
    })

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `{ 
           evaluations(withinPolygon: [
            {lng: -150.82031249999997, lat: -0.3515602939922709}
            {lng: -41.8359375, lat: -0.3515602939922709},
            {lng: -41.8359375, lat: 73.62778879339942},
            {lng: -150.82031249999997, lat: 73.62778879339942},
            {lng: -150.82031249999997, lat: -0.3515602939922709},
          ]) {
          yearBuilt
        }
      }`,
      })

    let { evaluations: [first] } = response.body.data
    expect(first.yearBuilt).toEqual('1980')
  })

  it('returns evaluations within the given bounds', async () => {
    let geocoded = testData.slice()
    geocoded[0].location = {
      type: 'Point',
      coordinates: [-79.348650200148, 43.8036022863624],
    }

    await collection.insertMany(geocoded)

    // Ask for the one closest to Toronto

    let server = new Server({
      client: collection,
    })

    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({
        query: `{ 
           evaluations(withinPolygon: [
            {lng: -150.82031249999997, lat: -0.3515602939922709}
            {lng: -41.8359375, lat: -0.3515602939922709},
            {lng: -41.8359375, lat: 73.62778879339942},
            {lng: -150.82031249999997, lat: 73.62778879339942},
            {lng: -150.82031249999997, lat: -0.3515602939922709},
          ]) {
          yearBuilt
        }
      }`,
      })

    // We expect 1 result: Ottawa
    let { evaluations: [first] } = response.body.data
    expect(first.yearBuilt).toEqual('1980')
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

    // We expect 1 result: Ottawa
    let { evaluationsFor } = response.body.data
    expect(evaluationsFor.yearBuilt).toEqual('1980')
  })
})

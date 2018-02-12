import { MongoClient } from 'mongodb'
import request from 'supertest'
import Server from '../src/server'

let client, db, collection, server
const url = 'mongodb://localhost:27017'
const dbName = 'energuide'

describe('queries', () => {
  beforeAll(async () => {
    client = await MongoClient.connect(url)
    db = client.db(dbName)
    collection = db.collection('dwellings')
    server = new Server({
      client: collection,
    })
  })

  afterAll(async () => {
    client.close()
  })

  describe('evaluationsFor', () => {
    it('retrieves evaluations given an account id and a postalcode', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluations:evaluationsFor(account: 189250) {
            yearBuilt
          }
        }`,
        })
      let { evaluations } = response.body.data
      expect(evaluations.yearBuilt).toEqual(1900)
    })
  })

  describe('dwellingsInFSA', () => {
    describe('pagination', () => {
      beforeEach(async () => {
        await collection.save({
          houseId: 1000000,
          yearBuilt: 3000,
          city: 'Charlottetown',
          region: 'PE',
          forwardSortationArea: 'C1A',
        })
      })

      afterEach(async () => {
        await collection.deleteOne({
          houseId: 1000000,
          yearBuilt: 3000,
          city: 'Charlottetown',
          region: 'PE',
          forwardSortationArea: 'C1A',
        })
      })

      it('uses limit and next to paginate results', async () => {
        let response = await request(server)
          .post('/graphql')
          .set('Content-Type', 'application/json; charset=utf-8')
          .send({
            query: `{
              dwellings:dwellingsInFSA(
               forwardSortationArea: "C1A"
               limit: 1
              ) {
                hasNext
                next
                results {
                  yearBuilt
                }
              }
            }`,
          })

        // use the value of "next" to fetch the next result
        let response2 = await request(server)
          .post('/graphql')
          .set('Content-Type', 'application/json; charset=utf-8')
          .send({
            query: `{
              dwellings:dwellingsInFSA(
               forwardSortationArea: "C1A"
               limit: 1
               next: "${response.body.data.dwellings.next}"
              ) {
                hasNext
                next
                results {
                  yearBuilt
                }
              }
            }`,
          })

        let { dwellings: first } = response.body.data
        let { dwellings: second } = response2.body.data
        expect(first.results[0].yearBuilt).toEqual(3000)
        expect(second.results[0].yearBuilt).toEqual(1900)
      })
    })

    it('returns the dwellings in the given Forward Sortation Area', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          dwellings:dwellingsInFSA(
           forwardSortationArea: "C1A"
          ) {
            results {
							yearBuilt
						}
          }
        }`,
        })

      let { dwellings } = response.body.data
      expect(dwellings.results.length).toEqual(1)
    })

    describe('filter', () => {
      describe('gt: greater than', () => {
        it('filters out results where the selected field has a value greater than the selected value', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings:dwellingsInFSA(
                  forwardSortationArea: "C1A"
                  filter: {field: yearBuilt gt: "1900"}
                 ) {
										results {
											yearBuilt
										}
                 }
               }`,
            })

          let { dwellings } = response.body.data
          expect(dwellings.results.length).toEqual(0)
        })

        it('works on string fields', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings:dwellingsInFSA(
                  forwardSortationArea: "C1A"
                  filter: {field: city eq: "Charlottetown"}
                 ) {
									 results {
										 yearBuilt
									 }
                 }
               }`,
            })
          let { dwellings: { results: [first] } } = response.body.data
          expect(first.yearBuilt).toEqual(1900)
        })
      })

      describe('lt: less than', () => {
        it('filters out results where the selected field has a value less than the selected value', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings:dwellingsInFSA(
                  forwardSortationArea: "C1A"
                  filter: {field: yearBuilt lt: "2000"}
                 ) {
									 results {
                     yearBuilt
									 }
                 }
               }`,
            })
          let { dwellings: { results: [first] } } = response.body.data
          expect(first.yearBuilt).toEqual(1900)
        })
      })

      describe('eq: equal to', () => {
        it('filters out results where the selected field has a value equal to the selected value', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings:dwellingsInFSA(
                  forwardSortationArea: "C1A"
                  filter: {field: yearBuilt eq: "1900"}
                 ) {
                   results {
										 yearBuilt
								   }
                 }
               }`,
            })

          let { dwellings: { results: [first] } } = response.body.data
          expect(first.yearBuilt).toEqual(1900)
        })
      })

      it('complains about multiple comparators', async () => {
        let response = await request(server)
          .post('/graphql')
          .set('Content-Type', 'application/json; charset=utf-8')
          .send({
            query: `{
               dwellingsInFSA(
                forwardSortationArea: "M8H"
                filter: {field: yearBuilt gt: "1979" lt: "1979"}
              ) {
								results {
								 yearBuilt
							 }
             }
           }`,
          })
        expect(response.body).toHaveProperty('errors')
      })
    })

    it('gets evalutations within a Forward Sortation Area', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
           dwellings:dwellingsInFSA(
             forwardSortationArea: "C1A"
           ) {
					results {
						yearBuilt
					}
        }
      }`,
        })

      let { dwellings: { results: [first] } } = response.body.data
      expect(first.yearBuilt).toEqual(1900)
    })
  })
})

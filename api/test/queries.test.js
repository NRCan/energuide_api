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

  describe('Dwelling data', () => {
    it('retrieves all top level keys of the dwelling data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluations:dwelling(houseId: 1024170) {
              houseId
              yearBuilt
              city
              region
              forwardSortationArea
            }
        }`,
        })

      expect(response.body).not.toHaveProperty('errors')
      let { evaluations } = response.body.data
      expect(evaluations).toEqual({
        city: 'Anagance',
        forwardSortationArea: 'O7I',
        houseId: 1024170,
        region: 'NB',
        yearBuilt: 1921,
      })
    })

    it('retrieves all top level keys of the evaluation data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          dwelling(houseId: 1024170) {
            evaluations {
              evaluationType
              entryDate
              creationDate
              modificationDate
              fileId
              houseType
              heatedFloorArea
            }
          }
        }`,
        })

      let { dwelling } = response.body.data
      let [first] = dwelling.evaluations
      expect(first).toEqual({
        creationDate: '2011-03-14T14:26:52',
        entryDate: '2010-10-12',
        evaluationType: 'D',
        modificationDate: null,
        fileId: '1B07D10023',
        houseType: 'Single detached',
        heatedFloorArea: null,
      })
    })

    it('retrieves all keys for ersRating data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
            dwelling(houseId:1499786){
              evaluations {
                ersRating {
                  measurement
                  upgrade
                }
              }
            }
          }`,
        })
      expect(response.body).not.toHaveProperty('errors')
      let { dwelling: { evaluations } } = response.body.data
      let [first] = evaluations
      let ersRating = first.ersRating
      expect(ersRating.measurement).toEqual(133)
    })

    it('retrieves all keys for wall data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
            dwelling(houseId: 1024170) {
            evaluations {
              walls {
                measurement {
                  insulation {
                    percentage
                    rValue
                  }
                  heatLost
                }
                upgrade {
                  insulation {
                    percentage
                    rValue
                  }
                  heatLost
                }
              }
            }
          }
        }`,
        })

      expect(response.body).not.toHaveProperty('errors')
      let { dwelling: { evaluations } } = response.body.data
      let [first] = evaluations
      let wall = first.walls
      expect(wall).toEqual({
        measurement: {
          heatLost: 16997.4,
          insulation: [
            {
              percentage: 100,
              rValue: 12,
            },
          ],
        },
        upgrade: {
          heatLost: 11082.7,
          insulation: [
            {
              percentage: 100,
              rValue: 18,
            },
          ],
        },
      })
    })

    it('retrieves all top level keys of the upgrade data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          dwelling(houseId: 1556256) {
            evaluations {
              energyUpgrades {
                upgradeType
                cost
                priority
              }
            }
          }
        }`,
        })

      expect(response.body).not.toHaveProperty('errors')
      let { dwelling: { evaluations } } = response.body.data
      let [first] = evaluations
      let [upgrade] = first.energyUpgrades
      expect(upgrade).toEqual({
        upgradeType: 'CathedralCeilingsFlat',
        cost: 0,
        priority: 1,
      })
    })
  })

  describe('dwelling', () => {
    it('retrieves evaluations given an houseId id', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluations:dwelling(houseId: 1024170) {
            yearBuilt
          }
        }`,
        })
      let { evaluations } = response.body.data
      expect(evaluations.yearBuilt).toEqual(1921)
    })
  })

  describe('dwellingsInFSA', () => {
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

    it('gets evalutations within a Forward Sortation Area', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
           dwellings(
             filters: [{field: dwellingForwardSortationArea comparator: eq value: "C1A"}]
           ) {
          results {
            yearBuilt
          }
        }
      }`,
        })

      let { dwellings: { results: [first] } } = response.body.data
      expect(first.yearBuilt).toEqual(3000)
    })

    describe('pagination', () => {
      beforeEach(async () => {
        await collection.save({
          houseId: 1000000,
          yearBuilt: 3000,
          city: 'Charlottetown',
          region: 'PE',
          forwardSortationArea: 'A2A',
        })
        await collection.save({
          houseId: 2000000,
          yearBuilt: 3100,
          city: 'Charlottetown',
          region: 'PE',
          forwardSortationArea: 'A2A',
        })
      })

      afterEach(async () => {
        await collection.deleteOne({
          houseId: 1000000,
          yearBuilt: 3000,
          city: 'Charlottetown',
          region: 'PE',
          forwardSortationArea: 'A2A',
        })
        await collection.deleteOne({
          houseId: 2000000,
          yearBuilt: 3100,
          city: 'Charlottetown',
          region: 'PE',
          forwardSortationArea: 'A2A',
        })
      })

      const makeRequestForOnePage = function({
        next = '',
        previous = '',
      } = {}) {
        let query = `{
          dwellings(
           filters: [{field: dwellingForwardSortationArea comparator: eq value: "A2A"}]
           limit: 1
           ${next}
           ${previous}
          ) {
            hasNext
            next
            hasPrevious
            previous
            results {
              yearBuilt
            }
          }
        }`

        return request(server)
          .post('/graphql')
          .set('Content-Type', 'application/json; charset=utf-8')
          .send({
            query,
          })
      }

      it('uses limit and next to paginate results', async () => {
        let response = await makeRequestForOnePage()

        // use the value of "next" to fetch the next results
        let response2 = await makeRequestForOnePage({
          next: `next: "${response.body.data.dwellings.next}"`,
        })

        let { dwellings: first } = response.body.data
        let { dwellings: second } = response2.body.data
        expect(first.results[0].yearBuilt).toEqual(3100)
        expect(second.results[0].yearBuilt).toEqual(3000)

        expect(first.hasNext).toBe(true)
        expect(second.hasNext).toBe(false)
      })

      it('uses limit and previous to paginate results', async () => {
        let response = await makeRequestForOnePage()

        let response2 = await makeRequestForOnePage({
          next: `next: "${response.body.data.dwellings.next}"`,
        })

        // use the value of "previous" to fetch the previous results
        let response3 = await makeRequestForOnePage({
          previous: `previous: "${response2.body.data.dwellings.previous}"`,
        })

        let { dwellings: first } = response.body.data
        let { dwellings: second } = response2.body.data
        let { dwellings: third } = response3.body.data
        expect(first).toEqual(third)
        expect(second.results[0].yearBuilt).toEqual(3000)

        expect(first.hasPrevious).toBe(false)
        expect(second.hasPrevious).toBe(true)
        expect(third.hasPrevious).toBe(false)
      })

      it('Returns error key if values exist for both next and previous', async () => {
        let response = await makeRequestForOnePage()

        let response2 = await makeRequestForOnePage({
          next: `next: "${response.body.data.dwellings.next}"`,
          previous: `previous: "${response.body.data.dwellings.previous}"`,
        })

        let { dwellings: first } = response.body.data
        expect(first.results[0].yearBuilt).toEqual(3100)

        expect(response2.body.data.dwellings).toBe(null)
        expect(response2.body.errors).not.toBe(null)
        expect(response2.body.errors[0].message).toEqual(
          "Cannot submit values for both 'next' and 'previous'.",
        )
        // returned status code is still 200
        expect(response2.status).toBe(200)
      })
    })

    it('returns the dwellings in the given Forward Sortation Area', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          dwellings(
            filters: [{field: dwellingForwardSortationArea comparator: eq value: "O7I"}]
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

    describe('filters', () => {
      it('allows for multiple filters', async () => {
        let response = await request(server)
          .post('/graphql')
          .set('Content-Type', 'application/json; charset=utf-8')
          .send({
            query: `{
               dwellings(
                filters: [
                  {field: dwellingCity comparator: eq value: "Anagance"}
                  {field: dwellingYearBuilt comparator: eq value: "1921"}
                ]
               ) {
                 results {
                   city
                   yearBuilt
                 }
               }
             }`,
          })
        let { dwellings: { results: [first] } } = response.body.data
        expect(first.city).toEqual('Anagance')
        expect(first.yearBuilt).toEqual(1921)
      })

      describe('gt: greater than', () => {
        it('returns dwellings where the field is greater than the given value', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings(
                   filters: [
                    {field: dwellingForwardSortationArea comparator: eq value: "O7I"}
                    {field: dwellingYearBuilt comparator: gt value: "1900"}
                   ]
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

        it('works on string fields', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings(
                   filters: [
                    {field: dwellingForwardSortationArea comparator: eq value: "O7I"}
                    {field: dwellingCity comparator: eq value: "Anagance"}
                   ]
                  ) {
                   results {
                     city
                   }
                 }
               }`,
            })

          let { dwellings: { results: [first] } } = response.body.data
          expect(first.city).toEqual('Anagance')
        })

        it('correctly handles integer values', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings(
                   filters: [
                    {field: dwellingForwardSortationArea comparator: eq value: "O7I"}
                    {field: dwellingYearBuilt comparator: gt value: "1" }
                   ]
                 ) {
                  results {
                    yearBuilt
                  }
                }
               }`,
            })

          let { data } = response.body
          let { dwellings } = data
          expect(dwellings.results.length).toBeGreaterThan(0)
        })
      })

      describe('lt: less than', () => {
        beforeEach(async () => {
          await collection.save({
            houseId: 1000000,
            yearBuilt: 1800,
            city: 'Charlottetown',
            region: 'PE',
            forwardSortationArea: 'B3A',
          })
        })

        afterEach(async () => {
          await collection.deleteOne({
            houseId: 1000000,
            yearBuilt: 1800,
            city: 'Charlottetown',
            region: 'PE',
            forwardSortationArea: 'B3A',
          })
        })

        it('returns dwellings where the field is less than the given value', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings(
                   filters: [
                     {field: dwellingForwardSortationArea comparator: eq value: "B3A"}
                     {field: dwellingYearBuilt comparator: lt value: "2000"}
                   ]
                 ) {
                     results {
                       yearBuilt
                    }
                 }
               }`,
            })
          let { dwellings: { results: [first] } } = response.body.data
          expect(first.yearBuilt).toEqual(1800)
        })
      })

      describe('eq: equal to', () => {
        it('returns dwellings where the field is equal to the given value', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings(
                   filters: [
                     {field: dwellingForwardSortationArea comparator: eq value: "O7I"}
                     {field: dwellingYearBuilt comparator: eq value: "1921"}
                   ]
                 ) {
                   results {
                     yearBuilt
                   }
                 }
               }`,
            })

          let { dwellings: { results: [first] } } = response.body.data
          expect(first.yearBuilt).toEqual(1921)
        })

        it('works on string fields', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings(
                  filters: [
                    {field: dwellingForwardSortationArea comparator: eq value: "O7I"}
                    {field: dwellingCity comparator: eq value: "Anagance"}
                  ]
                 ) {
                   results {
                     city
                   }
                 }
               }`,
            })
          let { dwellings: { results: [first] } } = response.body.data
          expect(first.city).toEqual('Anagance')
        })
      })
    })

    describe('date filters', () => {
      const makeRequestForDateRange = function({
        startDate = 'startDate: "2011-04-01"',
        endDate = '',
      } = {}) {
        // default creationDate is "2012-10-01T15:08:41"
        let query = `{
          dwellings(
           filters: [{field: dwellingForwardSortationArea comparator: eq value: "O7I"}]
           dateRange: {
             field: evaluationCreationDate
             ${startDate}
             ${endDate}
           }
          ) {
            results {
              evaluations {
                creationDate
                fileId
              }
            }
          }
        }`

        return request(server)
          .post('/graphql')
          .set('Content-Type', 'application/json; charset=utf-8')
          .send({
            query,
          })
      }

      function expectEvaluationIsReturned(_response) {
        let {
          creationDate,
          fileId,
        } = _response.body.data.dwellings.results[0].evaluations[0]
        expect(creationDate).toEqual('2011-03-14T14:26:52')
        expect(fileId).toEqual('1B07D10023')
      }

      function expectEvaluationIsNotReturned(_response) {
        expect(_response.body.data.dwellings.results).toEqual([])
        expect(_response.body.errors).toBe(undefined)
      }

      const validStartDates = ['2011-01-01', '2010-09-30', '2009-10-01']
      validStartDates.forEach(_startDate => {
        it(`will return results for a startDate earlier than or equal to 2011-04-01: ${_startDate}`, async () => {
          let response = await makeRequestForDateRange({
            startDate: `startDate: "${_startDate}"`,
          })

          let { data } = response.body
          let { dwellings } = data
          expect(dwellings.results.length).toBeGreaterThan(0)
        })
      })

      it(`will not return results for a startDate later than 2011-04-01`, async () => {
        let response = await makeRequestForDateRange({
          startDate: 'startDate: "2011-04-01"',
        })

        expectEvaluationIsNotReturned(response)
      })

      const validEndDates = ['2013-01-01', '2012-10-02']
      validEndDates.forEach(_endDate => {
        it(`will return results for a endDate later than 2011-04-01: ${_endDate}`, async () => {
          let response = await makeRequestForDateRange({
            startDate: '',
            endDate: `endDate: "${_endDate}"`,
          })

          let { data } = response.body
          let { dwellings } = data
          expect(dwellings.results.length).toBeGreaterThan(0)
        })
      })

      /*
      Because we are doing string comparisons in the database,
      "2012-10-01" <= "2012-10-01T15:08:41" is true, but
      "2012-10-01" >= "2012-10-01T15:08:41" is false
      */
      const invalidEndDates = ['2011-02-01', '2010-03-30', '2011-01-01']
      invalidEndDates.forEach(_endDate => {
        it(`will not return results for a endDate earlier than or equal to 2011-03-01: ${_endDate}`, async () => {
          let response = await makeRequestForDateRange({
            startDate: '',
            endDate: `endDate: "${_endDate}"`,
          })

          expectEvaluationIsNotReturned(response)
        })
      })

      it(`will return results if both a valid startDate and endDate are submitted`, async () => {
        let response = await makeRequestForDateRange({
          startDate: 'startDate: "2011-03-01"',
          endDate: 'endDate: "2011-04-01"',
        })

        expectEvaluationIsReturned(response)
      })

      it(`will return an error if the startDate and the endDate are equal to each other`, async () => {
        let response = await makeRequestForDateRange({
          startDate: 'startDate: "2012-10-01"',
          endDate: 'endDate: "2012-10-01"',
        })

        expect(response.body.data.dwellings).toBe(null)
        expect(response.body.errors[0].message).toEqual(
          "The 'endDate' cannot be equal to or earlier than the 'startDate'.",
        )
        // status code is 200 for errors we throw manually
        expect(response.status).toBe(200)
      })

      it(`will return an error if the startDate comes after the endDate`, async () => {
        let response = await makeRequestForDateRange({
          startDate: 'startDate: "2012-10-02"',
          endDate: 'endDate: "2012-10-01"',
        })

        expect(response.body.data.dwellings).toBe(null)
        expect(response.body.errors[0].message).toEqual(
          "The 'endDate' cannot be equal to or earlier than the 'startDate'.",
        )
        // status code is 200 for errors we throw manually
        expect(response.status).toBe(200)
      })

      it(`will return an error if neither a startDate or endDate is submitted`, async () => {
        let response = await makeRequestForDateRange({
          startDate: '',
          endDate: '',
        })

        expect(response.body.data.dwellings).toBe(null)
        expect(response.body.errors[0].message).toEqual(
          "A 'dateRange' must include a 'startDate' or an 'endDate'.",
        )
        // status code is 200 for errors we throw manually
        expect(response.status).toBe(200)
      })

      const invalidDates = [
        'not a date',
        1,
        true,
        '2012-10-01T15:08:41', // timestamp is not a valid YYYY-MM-DD string
        '2012/10/01', // slashes used instead of dashes
        '2012-09-31', // September 31st isn't a date
        '2012-31-12', // Month and day are reversed
      ]
      invalidDates.forEach(_invalidDate => {
        it(`will throw a validation error if an invalid date is submitted: ${_invalidDate}`, async () => {
          let response = await makeRequestForDateRange({
            startDate: `startDate: "${_invalidDate}"`,
          })

          expect(response.body.errors[0].message).toContain(
            'Expected type Date',
          )
          expect(response.status).toBe(400)
        })
      })
    })
  })
})

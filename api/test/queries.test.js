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
          evaluations:evaluationsFor(account: 189250) {
              houseId
              yearBuilt
              city
              region
              forwardSortationArea
            }
        }`,
        })

      let { evaluations } = response.body.data
      expect(evaluations).toEqual({
        city: 'Charlottetown',
        forwardSortationArea: 'C1A',
        houseId: 189250,
        region: 'PE',
        yearBuilt: 1900,
      })
    })

    it('retrieves all top level keys of the evaluation data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluations:evaluationsFor(account: 189250) {
            evaluations {
              evaluationType
              entryDate
              creationDate
              modificationDate
            }
          }
        }`,
        })

      let { evaluations } = response.body.data
      expect(evaluations).toEqual({
        evaluations: [
          {
            creationDate: '2012-10-01T15:08:41',
            entryDate: '2011-11-18',
            evaluationType: 'E',
            modificationDate: '2012-06-09T11:20:20',
          },
          {
            creationDate: '2012-10-01T15:08:39',
            entryDate: '2011-08-18',
            evaluationType: 'D',
            modificationDate: '2012-06-09T11:20:20',
          },
        ],
      })
    })

    it('retrieves all top level keys of the ceiling data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluations:evaluationsFor(account: 189250) {
            evaluations {
              ceilings {
                label
                typeEnglish
                typeFrench
                nominalRsi
                nominalR
                effectiveRsi
                effectiveR
                areaMetres
                areaFeet
                lengthMetres
                lengthFeet
              }
            }
          }
        }`,
        })

      let { evaluations } = response.body.data
      expect(evaluations).toEqual({
        evaluations: [
          {
            ceilings: [
              {
                areaFeet: 830.1171300283143,
                areaMetres: 77.1204,
                effectiveR: 36.3397497041326,
                effectiveRsi: 6.3998,
                label: 'Ceiling01',
                lengthFeet: 47.66404352,
                lengthMetres: 14.528,
                nominalR: 36.3397497041326,
                nominalRsi: 6.3998,
                typeEnglish: 'Attic/gable',
                typeFrench: 'Combles/pignon',
              },
            ],
          },
          {
            ceilings: [
              {
                areaFeet: 830.1171300283143,
                areaMetres: 77.1204,
                effectiveR: 36.3397497041326,
                effectiveRsi: 6.3998,
                label: 'Ceiling01',
                lengthFeet: 47.66404352,
                lengthMetres: 14.528,
                nominalR: 36.3397497041326,
                nominalRsi: 6.3998,
                typeEnglish: 'Attic/gable',
                typeFrench: 'Combles/pignon',
              },
            ],
          },
        ],
      })
    })

    it('retrieves all top level keys of the wall data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluations:evaluationsFor(account: 189250) {
            evaluations {
              walls {
                label
                structureTypeEnglish
                structureTypeFrench
                componentTypeSizeEnglish
                componentTypeSizeFrench
                nominalRsi
                nominalR
                effectiveRsi
                effectiveR
                areaMetres
                areaFeet
                perimeter
                height
              }
            }
          }
        }`,
        })

      let { evaluations } = response.body.data
      expect(evaluations).toEqual({
        evaluations: [
          {
            walls: [
              {
                areaFeet: 1000.7916833561255,
                areaMetres: 92.97658384,
                componentTypeSizeEnglish: null,
                componentTypeSizeFrench: null,
                effectiveR: 15.2699857658604,
                effectiveRsi: 2.6892,
                height: 2.5999,
                label: 'Main floor',
                nominalR: 19.0874822073255,
                nominalRsi: 3.3615,
                perimeter: 35.7616,
                structureTypeEnglish: null,
                structureTypeFrench: null,
              },
            ],
          },
          {
            walls: [
              {
                areaFeet: 1000.7916833561255,
                areaMetres: 92.97658384,
                componentTypeSizeEnglish: null,
                componentTypeSizeFrench: null,
                effectiveR: 15.2699857658604,
                effectiveRsi: 2.6892,
                height: 2.5999,
                label: 'Main floor',
                nominalR: 19.0874822073255,
                nominalRsi: 3.3615,
                perimeter: 35.7616,
                structureTypeEnglish: null,
                structureTypeFrench: null,
              },
            ],
          },
        ],
      })
    })

    it('retrieves all top level keys of the door data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluations:evaluationsFor(account: 189250) {
            evaluations {
              doors {
                typeEnglish
                typeFrench
                rsi
                rValue
                uFactor
                uFactorImperial
                areaMetres
                areaFeet
              }
            }
          }
        }`,
        })

      let { evaluations } = response.body.data
      expect(evaluations).toEqual({
        evaluations: [
          {
            doors: [
              {
                areaFeet: 18.9875391902784,
                areaMetres: 1.764,
                rValue: 6.4732202041799995,
                rsi: 1.14,
                typeEnglish: 'Steel Medium density spray foam core',
                typeFrench:
                  'Acier / âme en mousse à vaporiser de densité moyenne',
                uFactor: 0.8771929824561404,
                uFactorImperial: 0.15448261737709199,
              },
              {
                areaFeet: 18.9875391902784,
                areaMetres: 1.764,
                rValue: 6.4732202041799995,
                rsi: 1.14,
                typeEnglish: 'Steel Medium density spray foam core',
                typeFrench:
                  'Acier / âme en mousse à vaporiser de densité moyenne',
                uFactor: 0.8771929824561404,
                uFactorImperial: 0.15448261737709199,
              },
            ],
          },
          {
            doors: [
              {
                areaFeet: 18.9875391902784,
                areaMetres: 1.764,
                rValue: 6.4732202041799995,
                rsi: 1.14,
                typeEnglish: 'Steel Medium density spray foam core',
                typeFrench:
                  'Acier / âme en mousse à vaporiser de densité moyenne',
                uFactor: 0.8771929824561404,
                uFactorImperial: 0.15448261737709199,
              },
              {
                areaFeet: 18.9875391902784,
                areaMetres: 1.764,
                rValue: 6.4732202041799995,
                rsi: 1.14,
                typeEnglish: 'Steel Medium density spray foam core',
                typeFrench:
                  'Acier / âme en mousse à vaporiser de densité moyenne',
                uFactor: 0.8771929824561404,
                uFactorImperial: 0.15448261737709199,
              },
            ],
          },
        ],
      })
    })

    it('retrieves all top level keys of the window data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluations:evaluationsFor(account: 189250) {
            evaluations {
              windows {
                label
                rsi
                rvalue
                glazingTypesEnglish
                glazingTypesFrench
                coatingsTintsEnglish
                coatingsTintsFrench
                fillTypeEnglish
                fillTypeFrench
                spacerTypeEnglish
                spacerTypeFrench
                typeEnglish
                typeFrench
                frameMaterialEnglish
                frameMaterialFrench
                areaMetres
                areaFeet
                width
                height
              }
            }
          }
        }`,
        })

      let { evaluations: { evaluations: [first] } } = response.body.data
      let [eastWindow] = first.windows
      expect(eastWindow).toEqual({
        label: 'East0001',
        rsi: 0.2685,
        rvalue: 1.5246137059845,
        glazingTypesEnglish: 'Double/double with 1 coat',
        glazingTypesFrench: 'Double/double, 1 couche',
        coatingsTintsEnglish: 'Clear',
        coatingsTintsFrench: 'Transparent',
        fillTypeEnglish: '13 mm Air',
        fillTypeFrench: "13 mm d'air",
        spacerTypeEnglish: 'Metal',
        spacerTypeFrench: 'Métal',
        typeEnglish: 'Picture',
        typeFrench: 'Fixe',
        frameMaterialEnglish: 'Aluminum',
        frameMaterialFrench: 'Aluminium',
        areaMetres: 1.31104735596684,
        areaFeet: 14.111997194858986,
        width: 1.0746954,
        height: 1.2199246000000001,
      })
    })
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

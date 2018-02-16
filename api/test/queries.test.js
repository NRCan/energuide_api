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
          evaluationsFor(account: 189250) {
            evaluations {
              ceilings {
                label
                typeEnglish
                typeFrench
                insulationNominalRsi
                insulationNominalR
                insulationEffectiveRsi
                insulationEffectiveR
                areaMetres
                areaFeet
                lengthMetres
                lengthFeet
              }
            }
          }
        }`,
        })

      let { evaluationsFor: { evaluations } } = response.body.data
      let [first] = evaluations
      let [ceiling] = first.ceilings
      expect(ceiling).toEqual({
        areaFeet: 830.1171300283143,
        areaMetres: 77.1204,
        insulationEffectiveR: 36.3397497041326,
        insulationEffectiveRsi: 6.3998,
        insulationNominalR: 36.3397497041326,
        insulationNominalRsi: 6.3998,
        label: 'Ceiling01',
        lengthFeet: 47.66404352,
        lengthMetres: 14.528,
        typeEnglish: 'Attic/gable',
        typeFrench: 'Combles/pignon',
      })
    })

    it('retrieves all top level keys of the wall data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluationsFor(account: 189250) {
            evaluations {
              walls {
                label
                structureTypeEnglish
                structureTypeFrench
                componentTypeSizeEnglish
                componentTypeSizeFrench
                insulationNominalRsi
                insulationNominalR
                insulationEffectiveRsi
                insulationEffectiveR
                areaMetres
                areaFeet
                perimeterMetres
                perimeterFeet
                heightMetres
                heightFeet
              }
            }
          }
        }`,
        })

      let { evaluationsFor: { evaluations } } = response.body.data
      let [first] = evaluations
      let [wall] = first.walls
      expect(wall).toEqual({
        areaFeet: 1000.7916833561255,
        areaMetres: 92.97658384,
        componentTypeSizeEnglish: null,
        componentTypeSizeFrench: null,
        heightFeet: 8.529855915999999,
        heightMetres: 2.5999,
        insulationEffectiveR: 15.2699857658604,
        insulationEffectiveRsi: 2.6892,
        insulationNominalR: 19.0874822073255,
        insulationNominalRsi: 3.3615,
        label: 'Main floor',
        perimeterFeet: 117.328087744,
        perimeterMetres: 35.7616,
        structureTypeEnglish: null,
        structureTypeFrench: null,
      })
    })

    it('retrieves all top level keys of the door data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluationsFor(account: 189250) {
            evaluations {
              doors {
                typeEnglish
                typeFrench
                insulationRsi
                insulationR
                uFactor
                uFactorImperial
                areaMetres
                areaFeet
              }
            }
          }
        }`,
        })

      let { evaluationsFor: { evaluations } } = response.body.data
      let [first] = evaluations
      let [door] = first.doors
      expect(door).toEqual({
        areaFeet: 18.9875391902784,
        areaMetres: 1.764,
        insulationR: 6.4732202041799995,
        insulationRsi: 1.14,
        typeEnglish: 'Steel Medium density spray foam core',
        typeFrench: 'Acier / âme en mousse à vaporiser de densité moyenne',
        uFactor: 0.8771929824561404,
        uFactorImperial: 0.15448261737709199,
      })
    })

    it('retrieves all top level keys of the waterheater data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluationsFor(account: 189250) {
            evaluations {
               waterHeatings {
                  typeEnglish
                  typeFrench
                  tankVolumeLitres
                  tankVolumeGallon
                  efficiency
                }
            }
          }
        }`,
        })

      let { evaluationsFor: { evaluations } } = response.body.data
      let [first] = evaluations
      let [waterHeatings] = first.waterHeatings
      expect(waterHeatings).toEqual({
        tankVolumeGallon: 39.995640800000004,
        efficiency: 0.554,
        tankVolumeLitres: 151.4,
        typeEnglish: 'Natural gas storage tank',
        typeFrench: 'Réservoir au gaz naturel',
      })
    })

    it('retrieves all top level keys of the floor data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluationsFor(account: 189250) {
            evaluations {
              floors {
                label
                insulationNominalRsi
                insulationNominalR
                insulationEffectiveRsi
                insulationEffectiveR
                areaMetres
                areaFeet
                lengthMetres
                lengthFeet
              }
            }
          }
        }`,
        })

      let { evaluationsFor: { evaluations } } = response.body.data
      let [first] = evaluations
      let [floor] = first.floors
      expect(floor).toEqual({
        areaFeet: 99.99996334435568,
        areaMetres: 9.2903,
        insulationEffectiveR: 14.82026730957,
        insulationEffectiveRsi: 2.61,
        insulationNominalR: 11.981135641069999,
        insulationNominalRsi: 2.11,
        label: 'Rm over garage',
        lengthFeet: 10.00000032,
        lengthMetres: 3.048,
      })
    })

    it('retrieves all top level keys of the heated floor area data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluationsFor(account: 189250) {
            evaluations {
              heatedFloorArea {
                areaAboveGradeMetres
                areaBelowGradeMetres
                areaAboveGradeFeet
                areaBelowGradeFeet
              }
            }
          }
        }`,
        })

      let { evaluationsFor: { evaluations } } = response.body.data
      let [first] = evaluations
      // there is only one heatedFloorArea object, unlike most other evaluation types
      let heatedFloorArea = first.heatedFloorArea
      expect(heatedFloorArea).toEqual({
        areaAboveGradeMetres: 600,
        areaBelowGradeMetres: 600,
        areaAboveGradeFeet: 6458.34666336,
        areaBelowGradeFeet: 6458.34666336,
      })
    })

    it('retrieves all top level keys of the ventilations data', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: `{
          evaluationsFor(account: 189250) {
            evaluations {
              ventilations {
                typeEnglish
                typeFrench
                airFlowRateLps
                airFlowRateCfm
              }
            }
          }
        }`,
        })

      let { evaluationsFor: { evaluations } } = response.body.data
      let [first] = evaluations
      let [ventilations] = first.ventilations
      expect(ventilations).toEqual({
        airFlowRateCfm: 466.1536,
        airFlowRateLps: 220,
        typeEnglish: 'Heat recovery ventilator',
        typeFrench: 'Ventilateur-récupérateur de chaleur',
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
                insulationRsi
                insulationR
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
                widthMetres
                widthFeet
                heightMetres
                heightFeet
              }
            }
          }
        }`,
        })

      let { evaluations: { evaluations: [first] } } = response.body.data
      let [eastWindow] = first.windows
      expect(eastWindow).toEqual({
        areaFeet: 14.111997194858986,
        areaMetres: 1.31104735596684,
        coatingsTintsEnglish: 'Clear',
        coatingsTintsFrench: 'Transparent',
        fillTypeEnglish: '13 mm Air',
        fillTypeFrench: "13 mm d'air",
        frameMaterialEnglish: 'Aluminum',
        frameMaterialFrench: 'Aluminium',
        glazingTypesEnglish: 'Double/double with 1 coat',
        glazingTypesFrench: 'Double/double, 1 couche',
        heightFeet: 4.002377424664,
        heightMetres: 1.2199246000000001,
        insulationR: 1.5246137059845,
        insulationRsi: 0.2685,
        label: 'East0001',
        spacerTypeEnglish: 'Metal',
        spacerTypeFrench: 'Métal',
        typeEnglish: 'Picture',
        typeFrench: 'Fixe',
        widthFeet: 3.5259036561359998,
        widthMetres: 1.0746954,
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
                  filter: {field: dwellingYearBuilt gt: "1900"}
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
                  filter: {field: dwellingCity eq: "Charlottetown"}
                 ) {
                   results {
                     city
                   }
                 }
               }`,
            })
          let { dwellings: { results: [first] } } = response.body.data
          expect(first.city).toEqual('Charlottetown')
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
                  filter: {field: dwellingYearBuilt lt: "2000"}
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
                  filter: {field: dwellingYearBuilt eq: "1900"}
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

    describe('filter', () => {
      describe('eq: equal to', () => {
        it('fails like the real server', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                dwellingsInFSA(
                  forwardSortationArea: "C1A"
                  filter: {
                    field: ventilationTypeEnglish
                    eq: "220"
                  }
                ) {
                  results {
                    houseId
                  }
                }
               }`,
            })

          expect(response.body).not.toHaveProperty('errors')
        })

        it('works on string fields', async () => {
          let response = await request(server)
            .post('/graphql')
            .set('Content-Type', 'application/json; charset=utf-8')
            .send({
              query: `{
                 dwellings:dwellingsInFSA(
                  forwardSortationArea: "C1A"
                  filter: {field: dwellingCity eq: "Charlottetown"}
                 ) {
                   results {
                     city
                   }
                 }
               }`,
            })
          let { dwellings: { results: [first] } } = response.body.data
          expect(first.city).toEqual('Charlottetown')
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
                  filter: {field: dwellingYearBuilt lt: "2000"}
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
                  filter: {field: dwellingYearBuilt eq: "1900"}
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

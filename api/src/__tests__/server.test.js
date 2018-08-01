import request from 'supertest'
import Server from '../server'

let server = new Server({
  client: { findOne: jest.fn(() => Promise.resolve({ foo: 'bar' })) },
})

describe('Server config', () => {
  describe('/', () => {
    it('redirects to /graphiql', async () => {
      let response = await request(server).get('/')
      expect(response.headers.location).toEqual('/graphiql')
      expect(response.status).toEqual(302)
    })
  })

  describe('/alive', () => {
    it('simply returns yes if the server is running', async () => {
      // for use with Kubernetes liveness probes.
      let response = await request(server).get('/alive')
      expect(response.status).toEqual(200)
      expect(response.text).toEqual('yes')
    })
  })

  describe('/ready', () => {
    it('checks to see if it can return data from the database', async () => {
      // for use with Kubernetes readiness probes.
      let response = await request(server).get('/ready')
      expect(response.status).toEqual(200)
      expect(response.text).toEqual('yes')
    })

    it('returns 500 if no data is returned', async () => {
      // for use with Kubernetes readiness probes.
      let noData = new Server({
        client: { findOne: jest.fn(() => Promise.resolve(null)) },
      })

      let response = await request(noData).get('/ready')
      expect(response.status).toEqual(500)
      let { error } = response.body
      expect(error).toMatch(/no data/i)
    })

    it('returns 500 if an exception is raised', async () => {
      // for use with Kubernetes readiness probes.
      let broken = new Server({
        client: {
          findOne: jest.fn(() => {
            throw new Error('sadness')
          }),
        },
      })
      let response = await request(broken).get('/ready')
      expect(response.status).toEqual(500)
      let { error } = response.body
      expect(error).toMatch(/sadness/i)
    })
  })

  describe('/graphql', () => {
    it('has GraphQL middleware mounted', async () => {
      let response = await request(server)
        .post('/graphql')
        .set('Content-Type', 'application/json; charset=utf-8')
        .send({
          query: ` {
          __schema {
            queryType {
              fields {
                name
              }
            }
          }
        } `,
        })

      expect(response.status).toEqual(200)
    })

    it('has Cross Origin Resource Sharing enabled for all domains', async () => {
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
  })

  describe('/graphiql', () => {
    it('serves the Graphiql IDE from the /graphiql endpoint', async () => {
      let response = await request(server)
        .get('/graphiql')
        .set('Accept', '*/*')

      expect(response.text).toMatch(/<title>GraphiQL<\/title>/)
    })
  })
})

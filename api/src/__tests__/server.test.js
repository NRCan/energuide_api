import request from 'supertest'
import Server from '../server'

let server = new Server({
  client: jest.fn(),
})

describe('Server config', () => {
  describe('/', () => {
    it('redirects to /graphiql', async () => {
      let response = await request(server).get('/')
      expect(response.headers.location).toEqual('/graphiql')
      expect(response.status).toEqual(302)
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

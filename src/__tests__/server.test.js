import request from 'supertest'
import Server from '../server'

let server = new Server({
  client: jest.fn(),
})

describe('configuration', () => {
  it('has GraphQL middleware mounted at /graphql', async () => {
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

  it('serves the Graphiql IDE from the /graphiql endpoint', async () => {
    let response = await request(server)
      .get('/graphiql')
      .set('Accept', '*/*')

    expect(response.text).toMatch(/<title>GraphiQL<\/title>/)
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

describe('i18n', () => {
  it('returns french description when french language header sent', async () => {
    let lang = 'fr'

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

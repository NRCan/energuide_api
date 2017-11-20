import request from 'supertest'
import Server from '../src/server'

describe('Server', () => {
  it('has GraphQL middleware mounted at /graphql', async () => {
    let server = new Server()
    let response = await request(server)
      .post('/graphql')
      .set('Content-Type', 'application/json; charset=utf-8')
      .send({"query": `{ 
        hello
      }`})

    expect(response.status).toEqual(200)
  })
})

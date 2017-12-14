import request from 'supertest'
import Server from '../src/server'

describe('Description language', () => {

	it('returns french description when french language header sent', async () => {
		let lang = 'fr'
		let server = Server()

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
	
		let description = response.body.data.__type.description
		expect(description).toEqual('Ceci est une description des évaluations')
	})

	it('returns english description when english language header sent', async () => {
		let lang = 'en'
		let server = Server()

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
	
		let description = response.body.data.__type.description 
		expect(description).toEqual('This is a description of evaluations')
	})

	it('defaults to english if no language header is set', async () => {
		let server = Server()

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
	
		let description = response.body.data.__type.description 
		expect(description).toEqual('This is a description of evaluations')
	})
})
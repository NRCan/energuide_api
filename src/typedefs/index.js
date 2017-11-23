const typeDefs = `
  type Query {
    evaluations: [Evaluation]
  }

  type Evaluation {
    yearBuilt: String
    floorArea: String
    footprint: String
    furnaceType: String
    furnaceFuel: String
  }
`

export default typeDefs

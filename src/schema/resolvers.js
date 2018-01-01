const resolvers = {
  Query: {
    evaluations: async (root, args, { client }) => {
      let results = await client.find()
      return results.toArray()
    },
  },
  Evaluation: {
    yearBuilt: root => root.YEARBUILT,
    floorArea: root => root.FLOORAREA,
    footprint: root => root.FOOTPRINT,
    furnaceType: root => root.FURNACETYPE,
    furnaceFuel: root => root.FURNACEFUEL,
  },
}

export default resolvers

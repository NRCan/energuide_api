const resolvers = {
  Query: {
    evaluations: async (root, args, { sql }) => {
      let results
      try {
        results = await sql.query`select * from new_evaluationBase;`
      } catch (err) {
        throw new Error(err)
      }

      return results.recordset
    },
  },
  Evaluation: {
    yearBuilt: root => root.new_YEARBUILT,
    floorArea: root => root.new_FLOORAREA,
    footprint: root => root.new_FOOTPRINT,
    furnaceType: root => root.new_FURNACETYPE,
    furnaceFuel: root => root.new_FURNACEFUEL,
  },
}

export default resolvers

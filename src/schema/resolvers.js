import Longitude from './types/Longitude'
import Latitude from './types/Latitude'

const resolvers = {
  Longitude,
  Latitude,
  Query: {
    evaluations: async (root, { withinPolygon }, { client }) => {
      let coordinates = withinPolygon.map(el => [el.lng, el.lat])
      let cursor = await client.find({
        'location.coordinates': {
          $geoWithin: {
            $geometry: {
              type: 'Polygon',
              coordinates: [coordinates],
            },
          },
        },
      })

      let results = await cursor.toArray()
      return results
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

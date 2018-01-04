import resolvers from './resolvers'
import { makeExecutableSchema } from 'graphql-tools'

const Schema = i18n => {
  const typeDefs = `
    scalar Longitude
    scalar Latitude

    input GeoPoint {
      lat: Latitude!
      lng: Longitude!
    }

    type Query {
      evaluations(withinPolygon: [GeoPoint]!): [Evaluation]
    }
    
    # ${i18n.t`This is a description of evaluations`}
    type Evaluation {
      # ${i18n.t`Year house was built in`}
      yearBuilt: String
      # ${i18n.t`Square footage of home`}
      floorArea: String
      # ${i18n.t`Footprint`}
      footprint: String
      # ${i18n.t`Type of furnace in home`}
      furnaceType: String
      # ${i18n.t`Type of fuel that furnace runs on`}
      furnaceFuel: String
    }
  `

  return makeExecutableSchema({ typeDefs, resolvers })
}

export default Schema

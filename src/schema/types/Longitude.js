import { GraphQLScalarType } from 'graphql'
import { GraphQLError } from 'graphql/error'
import { Kind } from 'graphql/language'

function isLongitude(value) {
  return value >= -180.0 && value <= 180.0
}

const Longitude = new GraphQLScalarType({
  name: 'Longitude',
  description:
    'The Longitude type represents a east–west position of' +
    ' a geographic coordinate. Valid values are between -180.0 and +180.0',
  serialize: Number,
  parseValue: value => {
    let number = Number(Number(value).toFixed(8))

    // Make sure this is a Float
    if ((typeof value === 'string')) {
      return new GraphQLError(
        'Invalid Longitude value: Must be floating point number or an Integer.',
      )
    }

    // Must be within range
    if (isLongitude(number)) {
      return parseFloat(number)
    } else {
      return new GraphQLError(
        'Invalid Longitude value: Must be inside valid range of -180.0 to +180.0',
      )
    }
  },
  parseLiteral: ast => {
    let value = Number(Number(ast.value).toFixed(8))

    // Make sure this is a Float
    if (!(ast.kind === Kind.FLOAT || ast.kind === Kind.INT)) {
      return new GraphQLError(
        'Invalid Longitude value: Must be floating point number or an Integer.',
      )
    }

    // Must be within range
    if (isLongitude(value)) {
      return parseFloat(value)
    } else {
      return new GraphQLError(
        'Invalid Longitude value: Must be inside valid range of -180.0 to +180.0',
      )
    }
  },
})

export default Longitude

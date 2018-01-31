import { GraphQLScalarType } from 'graphql'
import { GraphQLError } from 'graphql/error'
import { Kind } from 'graphql/language'

function isLatitude(value) {
  return value >= -90.0 && value <= 90.0
}

const Latitude = new GraphQLScalarType({
  name: 'Latitude',
  description:
    'The Latitude type represents a north–south position of' +
    ' a geographic coordinate. Valid values are between -90.0 and +90.0',
  serialize: Number,
  parseValue: value => {
    let number = Number(Number(value).toFixed(8))

    // Must be within range
    if (isLatitude(number)) {
      return parseFloat(number)
    } else {
      return new GraphQLError(
        'Invalid Latitude value: Must be inside valid range of -90.0 to +90.0',
      )
    }
  },
  parseLiteral: ast => {
    let value = Number(Number(ast.value).toFixed(8))

    // Make sure this is a Float
    if (!(ast.kind === Kind.FLOAT || ast.kind === Kind.INT)) {
      return new GraphQLError(
        'Invalid Latitude value: Must be floating point number or an Integer.',
      )
    }

    // Must be within range
    if (isLatitude(value)) {
      return parseFloat(value)
    } else {
      return new GraphQLError(
        'Invalid Latitude value: Must be inside valid range of -90.0 to +90.0',
      )
    }
  },
})

export default Latitude

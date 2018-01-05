import { GraphQLScalarType } from 'graphql'

import { GraphQLError } from 'graphql/error'
import { Kind } from 'graphql/language'

const Longitude = new GraphQLScalarType({
  name: 'Longitude',
  description:
    'The Longitude type represents a east–west position of' +
    ' a geographic coordinate. Valid values are between -180.0 and +180.0',
  serialize: Number,
  parseValue: Number,
  parseLiteral: ast => {
    let value = Number(Number(ast.value).toFixed(8))

    // Make sure this is a Float
    if (ast.kind !== Kind.FLOAT) {
      throw new GraphQLError(
        `Query error: Must be an float. Got a ${ast.kind}`,
        [ast],
      )
    }

    // Must be within range
    if (!(value >= -180.0 && value <= 180.0)) {
      throw new GraphQLError(
        'Query error: A valid longitude is between +180 and -180',
        [ast],
      )
    }

    return value
  },
})

export default Longitude

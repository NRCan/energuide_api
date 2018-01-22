import { GraphQLScalarType, GraphQLError } from 'graphql'
import { Kind } from 'graphql/language'

function isPostalCode({ kind, value }) {
  // Is it a string?
  if (kind !== Kind.STRING) {
    return null
  }
  // Regex taken from The Regular Expressions Cookbook:
  // https://www.safaribooksonline.com/library/view/regular-expressions-cookbook/9781449327453/ch04s15.html
  if (value.match(/^(?!.*[DFIOQU])[A-VXY][0-9][A-Z] ?[0-9][A-Z][0-9]$/)) {
    return value
  } else {
    throw new GraphQLError('Not a valid Postal Code')
  }
}

const PostalCode = new GraphQLScalarType({
  name: 'PostalCode',
  description: 'A Canadian Postal Code as defined by Canada Post.',
  serialize: String,
  parseValue: isPostalCode, // TODO: is this truely needed?
  parseLiteral: isPostalCode,
})

export default PostalCode

import { GraphQLScalarType, GraphQLError } from 'graphql'
import { Kind } from 'graphql/language'

function isFSA({ kind, value }) {
  // Is it a string?
  if (kind !== Kind.STRING) {
    return null
  }
  // Regex taken from The Regular Expressions Cookbook:
  // https://www.safaribooksonline.com/library/view/regular-expressions-cookbook/9781449327453/ch04s15.html
  if (value.match(/^(?!.*[DFIOQU])[A-VXY][0-9][A-Z]$/)) {
    return value
  } else {
    throw new GraphQLError('Not a valid Forward Sortation Area')
  }
}

const ForwardSortationArea = new GraphQLScalarType({
  name: 'ForwardSortationArea',
  description:
    'A Forward Sortation Area as defined by Canada Post. Basically the first 3 digits of a postal code.',
  serialize: String,
  parseValue: isFSA, // TODO: is this truely needed?
  parseLiteral: isFSA,
})

export default ForwardSortationArea

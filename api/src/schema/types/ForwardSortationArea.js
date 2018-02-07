import { GraphQLScalarType, GraphQLError } from 'graphql'
import { Kind } from 'graphql/language'

function isFSA(value) {
  return value.match(/^(?!.*[DFIOQU])[A-VXY][0-9][A-Z]$/)
}

const ForwardSortationArea = new GraphQLScalarType({
  name: 'ForwardSortationArea',
  description:
    'A Forward Sortation Area as defined by Canada Post. Basically the first 3 digits of a postal code.',
  serialize: String,
  parseValue: value => {
    if (isFSA(value)) {
      return value
    } else {
      throw new GraphQLError('Not a valid Forward Sortation Area')
    }
  },
  parseLiteral: ({ kind, value }) => {
    if (kind === Kind.STRING && isFSA(value)) {
      return value
    } else {
      throw new GraphQLError('Not a valid Forward Sortation Area')
    }
  },
})

export default ForwardSortationArea

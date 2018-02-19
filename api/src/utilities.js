// Mongodb filter map:
export const comparators = {
  gt: '$gt',
  lt: '$lt',
  eq: '$eq',
}

export function hasMoreThanOneComparator(filter) {
  if (filter) {
    return (
      Object.keys(filter)
        .filter(x => x !== 'field') // Remove field. It's supposed to be there.
        .filter(x => Object.keys(comparators).includes(x)).length > 1
    ) // more than one left?
  } else {
    return false
  }
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

export function generateName(type, attr) {
  let capitalized = capitalizeFirstLetter(attr)
  return `${type}${capitalized}`
}

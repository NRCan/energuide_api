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

export function createQuery(fsa, filter) {
  let query = {
    $and: [
      {
        forwardSortationArea: fsa,
      },
    ],
  }

  // { field: 'yearBuilt', gt: '1990' }
  if (filter) {
    for (let key in filter) {
      // make sure the key exists in the comparators' keys
      if (Object.keys(comparators).includes(key)) {
        // if the value is a number
        // - optionally starting with a minus sign
        // - containing zero or one decimal places
        // convert it to a float instead of a string
        if (filter[key].match(/^-?\d+\.?\d+$/)) {
          filter[key] = parseFloat(filter[key])
        }

        query['$and'].push({
          [filter.field]: { [comparators[key]]: filter[key] },
        })
      }
    }
  }

  return query
}

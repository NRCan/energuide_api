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
  // XXX: not all fields are integers.
  if (filter) {
    if (filter.gt) {
      query['$and'].push({
        [filter.field]: { [comparators.gt]: parseInt(filter.gt) },
      })
    }
    if (filter.lt) {
      query['$and'].push({
        [filter.field]: { [comparators.lt]: parseInt(filter.lt) },
      })
    }
    if (filter.eq) {
      query['$and'].push({
        [filter.field]: { [comparators.eq]: parseInt(filter.eq) },
      })
    }
  }

  return query
}

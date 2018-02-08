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
  // TODO: DRY this up.
  if (filter) {
    let value

    if (filter.gt) {
      if (filter.gt.match(/^-?\d+\.?\d+$/)) {
        value = parseFloat(filter.gt)
      }
      query['$and'].push({
        [filter.field]: { [comparators.gt]: value || filter.gt },
      })
    }
    if (filter.lt) {
      if (filter.lt.match(/^-?\d+\.?\d+$/)) {
        value = parseFloat(filter.lt)
      }
      query['$and'].push({
        [filter.field]: { [comparators.lt]: value || filter.lt },
      })
    }
    if (filter.eq) {
      if (filter.eq.match(/^-?\d+\.?\d+$/)) {
        value = parseFloat(filter.eq)
      }
      query['$and'].push({
        [filter.field]: { [comparators.eq]: value || filter.eq },
      })
    }
  }

  return query
}

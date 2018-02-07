import {
  comparators,
  createQuery,
  hasMoreThanOneComparator,
} from '../utilities'

describe('Utilities', () => {
  describe('comparators', () => {
    it('exports a comparators object', () => {
      let keys = Object.keys(comparators)
      expect(keys).toContain('gt', 'lt', 'eq')
    })
    it('maps generic comparators to Mongo specific ones', () => {
      expect(comparators.gt).toEqual('$gt')
      expect(comparators.lt).toEqual('$lt')
      expect(comparators.eq).toEqual('$eq')
    })
  })

  describe('createQuery', () => {
    describe('with a greater than filter', () => {
      it('returns a MongoDB $gt query object', () => {
        let fsa = 'C1A'
        let filter = { field: 'yearBuilt', gt: '2000' }

        let query = createQuery(fsa, filter)

        expect(query).toEqual({
          $and: [{ forwardSortationArea: 'C1A' }, { yearBuilt: { $gt: 2000 } }],
        })
      })
    })

    describe('with a less than filter', () => {
      it('returns a MongoDB $lt query object', () => {
        let fsa = 'C1A'
        let filter = { field: 'yearBuilt', lt: '2000' }

        let query = createQuery(fsa, filter)

        expect(query).toEqual({
          $and: [{ forwardSortationArea: 'C1A' }, { yearBuilt: { $lt: 2000 } }],
        })
      })
    })

    describe('with an equal to filter', () => {
      it('returns a MongoDB $eq query object', () => {
        let fsa = 'C1A'
        let filter = { field: 'yearBuilt', eq: '2000' }

        let query = createQuery(fsa, filter)

        expect(query).toEqual({
          $and: [{ forwardSortationArea: 'C1A' }, { yearBuilt: { $eq: 2000 } }],
        })
      })
    })

    describe('with no filter', () => {
      it('returns a MongoDB $eq query object', () => {
        let fsa = 'C1A'

        let query = createQuery(fsa, undefined)

        expect(query).toEqual({
          $and: [{ forwardSortationArea: 'C1A' }],
        })
      })
    })
  })

  describe('hasMoreThanOneComparator()', () => {
    it('returns true if more than one comparator appears in a filter object', () => {
      let filter = { field: 'yearBuilt', gt: '1990', lt: '1990' }
      expect(hasMoreThanOneComparator(filter)).toEqual(true)
    })

    it('returns false if there is only one comparator', () => {
      let filter = { field: 'yearBuilt', gt: '1990' }
      expect(hasMoreThanOneComparator(filter)).toEqual(false)
    })

    it('returns false if fed a falsy value', () => {
      expect(hasMoreThanOneComparator(false)).toEqual(false)
    })

    it('returns false if fed a undefined', () => {
      // for some reason this breaks the world in a way that falsy values don't
      expect(hasMoreThanOneComparator(undefined)).toEqual(false)
    })
  })
})

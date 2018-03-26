import { generateName } from '../utilities'

const tostr = Function.prototype.toString

function attachToString(func) {
  func.toString = function() {
    return `(${tostr.apply(func)})`
  }
  return func
}

// The fields on the dwelling type
const dwellingFields = [
  'houseId',
  'yearBuilt',
  'city',
  'region',
  'forwardSortationArea',
]

dwellingFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function('matcher', `return { ${attr}: matcher }`)
  module.exports[generateName('dwelling', attr)] = attachToString(fn)
})

// The fields on the evaluation type
const evaluationFields = ['evaluationType', 'fileId', 'ersRating']
// The date-specific fields on the evaluation type
const evaluationDateFields = ['entryDate', 'creationDate', 'modificationDate']

/*
  Since our date fields are just represented as strings in the database, we
  are using identical logic to match on them as we do when we match on our
  other string fields.
*/
evaluationFields.concat(evaluationDateFields).forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function('matcher', `return {"evaluations.${attr}": matcher}`)
  module.exports[generateName('evaluation', attr)] = attachToString(fn)
})

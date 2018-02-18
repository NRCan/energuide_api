import { generateName } from '../utilities'

const tostr = Function.prototype.toString

function attachToString(fn) {
  fn.toString = function() {
    return `(${tostr.apply(fn)})`
  }
  return fn
}

// The task at hand is to create a mapping between some publically exposed name
// (like dwelling_yearBuilt) and a mongodb query.
// The issue is that a friendly name is just enough to be unambiguous but our
// query requires knowledge of the structure of the document.
//
// There are three concerns here:
// 1) mapping from a type name to a location in a nested document
// 2) map the fields to a function that accepts a matcher and returns a query
// object
// 3) make sure that each function has a toString implementation that wraps the
// function body in an expression so it can be eval'd later

// Where in the hierarchy this type sits
function dwelling(attrFn) {
  return attrFn()
}
// The fields on the type
const dwellingFields = [
  'houseId',
  'yearBuilt',
  'city',
  'region',
  'forwardSortationArea',
]

// Define functions for each field.
dwellingFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function('matcher', `return { ${attr}: matcher }`)
  module.exports[generateName('dwelling', attr)] = attachToString(
    dwelling(() => fn),
  )
})

// Where in the hierarchy this type sits
function ventilation(attrFn) {
  return {
    evaluations: {
      $elemMatch: {
        ventilations: {
          $elemMatch: attrFn(),
        },
      },
    },
  }
}
// The fields on the type
const ventilationFields = [
  'typeEnglish',
  'typeFrench',
  'airFlowRateLps',
  'airFlowRateCfm',
  'efficiency',
]

// Define functions for each field.
ventilationFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function('matcher', `return { ${attr}: matcher }`)
  module.exports[generateName('ventilation', attr)] = attachToString(matcher =>
    ventilation(() => fn(matcher)),
  )
})

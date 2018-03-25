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

// The fields on the HeatedFloorArea  type
const heatedFloorAreaFields = [
  'areaAboveGradeMetres',
  'areaAboveGradeFeet',
  'areaBelowGradeMetres',
  'areaBelowGradeFeet',
]

heatedFloorAreaFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function(
    'matcher',
    `return {"evaluations.heatedFloorArea.${attr}": matcher}`,
  )
  module.exports[generateName('heatedFloorArea', attr)] = attachToString(fn)
})

// The fields on the Wall type
const wallFields = [
  'label',
  'structureTypeEnglish',
  'structureTypeFrench',
  'componentTypeSizeEnglish',
  'componentTypeSizeFrench',
  'insulationNominalRsi',
  'insulationNominalR',
  'insulationEffectiveRsi',
  'insulationEffectiveR',
  'areaMetres',
  'areaFeet',
  'perimeterMetres',
  'perimeterFeet',
  'heightMetres',
  'heightFeet',
]

wallFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function(
    'matcher',
    `
  return {
    evaluations: {
      $elemMatch: {
        walls: {
          $elemMatch:{ ${attr}: matcher },
        },
      },
    },
  }
  `,
  )
  module.exports[generateName('wall', attr)] = attachToString(fn)
})

// The fields on the Ceiling type
const ceilingFields = [
  'label',
  'typeEnglish',
  'typeFrench',
  'insulationNominalRsi',
  'insulationNominalR',
  'insulationEffectiveRsi',
  'insulationEffectiveR',
  'areaMetres',
  'areaFeet',
  'lengthMetres',
  'lengthFeet',
]

ceilingFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function(
    'matcher',
    `return {"evaluations.ceilings.${attr}": matcher}`,
  )
  module.exports[generateName('ceiling', attr)] = attachToString(fn)
})

// The fields on the Window type
const windowFields = [
  'label',
  'insulationRsi',
  'insulationR',
  'glazingTypesEnglish',
  'glazingTypesFrench',
  'coatingsTintsEnglish',
  'coatingsTintsFrench',
  'fillTypeEnglish',
  'fillTypeFrench',
  'spacerTypeEnglish',
  'spacerTypeFrench',
  'typeEnglish',
  'typeFrench',
  'frameMaterialEnglish',
  'frameMaterialFrench',
  'areaMetres',
  'areaFeet',
  'widthMetres',
  'widthFeet',
  'heightMetres',
  'heightFeet',
]

windowFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function(
    'matcher',
    `
  return {
    evaluations: {
      $elemMatch: {
        windows: {
          $elemMatch:{ ${attr}: matcher },
        },
      },
    },
  }
  `,
  )
  module.exports[generateName('window', attr)] = attachToString(fn)
})

// The fields on the Foundation type
const foundationFields = [
  'foundationTypeEnglish',
  'foundationTypeFrench',
  'label',
  'configurationType',
  'materialEnglish',
  'materialFrench',
]

foundationFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function(
    'matcher',
    `
    return {
      evaluations: {
        $elemMatch: {
          foundations: {
            $elemMatch:{ ${attr}: matcher },
          },
        },
      },
    }
  `,
  )
  module.exports[generateName('foundation', attr)] = attachToString(fn)
})

const headerFields = [
  'insulationNominalRsi',
  'insulationNominalR',
  'insulationEffectiveRsi',
  'insulationEffectiveR',
  'areaMetres',
  'areaFeet',
  'perimeterMetres',
  'perimeterFeet',
  'heightMetres',
  'heightFeet',
]

headerFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function(
    'matcher',
    `return { "evaluations.foundations.header.${attr}": matcher }`,
  )
  module.exports[generateName('foundationHeader', attr)] = attachToString(fn)
})

// The fields on the Foundation Floor type
const foundationFloorFields = [
  'floorTypeEnglish',
  'floorTypeFrench',
  'insulationNominalRsi',
  'insulationNominalR',
  'insulationEffectiveRsi',
  'insulationEffectiveR',
  'areaMetres',
  'areaFeet',
  'perimeterMetres',
  'perimeterFeet',
  'widthMetres',
  'widthFeet',
  'lengthMetres',
  'lengthFeet',
]

foundationFloorFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function(
    'matcher',
    `
      return {
        evaluations: {
          $elemMatch: {
            foundations: {
              $elemMatch: {
                floors: { $elemMatch: { ${attr}: matcher } },
              },
            },
          },
        },
      }
  `,
  )
  module.exports[generateName('foundationFloor', attr)] = attachToString(fn)
})

const foundationWallFields = [
  'wallTypeEnglish',
  'wallTypeFrench',
  'insulationNominalRsi',
  'insulationNominalR',
  'insulationEffectiveRsi',
  'insulationEffectiveR',
  'percentage',
  'areaMetres',
  'areaFeet',
]

foundationWallFields.forEach(attr => {
  // eslint-disable-next-line no-new-func
  let fn = new Function(
    'matcher',
    `
    return {
      evaluations: {
        $elemMatch: {
          foundations: {
            $elemMatch:{
              walls: {
                $elemMatch: { ${attr}: matcher }
              },
            },
          },
        },
      },
    }
  `,
  )
  module.exports[generateName('foundationWall', attr)] = attachToString(fn)
})

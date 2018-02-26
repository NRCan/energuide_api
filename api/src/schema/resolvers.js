import MongoPaging from 'mongo-cursor-pagination'
import {
  GraphQLInt,
  GraphQLFloat,
  GraphQLString,
  GraphQLBoolean,
} from 'graphql'

/* eslint-disable import/named */
import {
  dwellingHouseId,
  dwellingYearBuilt,
  dwellingCity,
  dwellingRegion,
  dwellingForwardSortationArea,
  ventilationTypeEnglish,
  ventilationTypeFrench,
  ventilationAirFlowRateLps,
  ventilationAirFlowRateCfm,
  ventilationEfficiency,
  floorLabel,
  floorInsulationNominalRsi,
  floorInsulationNominalR,
  floorInsulationEffectiveRsi,
  floorInsulationEffectiveR,
  floorAreaMetres,
  floorAreaFeet,
  floorLengthMetres,
  floorLengthFeet,
  waterHeatingTypeEnglish,
  waterHeatingTypeFrench,
  waterHeatingTankVolumeLitres,
  waterHeatingTankVolumeGallon,
  waterHeatingEfficiency,
  heatingLabel,
  heatingHeatingTypeEnglish,
  heatingHeatingTypeFrench,
  heatingEnergySourceEnglish,
  heatingEnergySourceFrench,
  heatingEquipmentTypeEnglish,
  heatingEquipmentTypeFrench,
  heatingOutputSizeKW,
  heatingOutputSizeBtu,
  heatingEfficiency,
  heatingSteadyState,
  heatedFloorAreaAreaAboveGradeMetres,
  heatedFloorAreaAreaAboveGradeFeet,
  heatedFloorAreaAreaBelowGradeMetres,
  heatedFloorAreaAreaBelowGradeFeet,
  wallLabel,
  wallStructureTypeEnglish,
  wallStructureTypeFrench,
  wallComponentTypeSizeEnglish,
  wallComponentTypeSizeFrench,
  wallInsulationNominalRsi,
  wallInsulationNominalR,
  wallInsulationEffectiveRsi,
  wallInsulationEffectiveR,
  wallAreaMetres,
  wallAreaFeet,
  wallPerimeterMetres,
  wallPerimeterFeet,
  wallHeightMetres,
  wallHeightFeet,
  ceilingLabel,
  ceilingTypeEnglish,
  ceilingTypeFrench,
  ceilingInsulationNominalRsi,
  ceilingInsulationNominalR,
  ceilingInsulationEffectiveRsi,
  ceilingInsulationEffectiveR,
  ceilingAreaMetres,
  ceilingAreaFeet,
  ceilingLengthMetres,
  ceilingLengthFeet,
} from './enums'
/* eslint-enable import/named */

const I18NInt = Object.create(GraphQLInt)
const I18NFloat = Object.create(GraphQLFloat)
const I18NString = Object.create(GraphQLString)
const I18NBoolean = Object.create(GraphQLBoolean)

const Resolvers = i18n => {
  I18NInt.description = i18n.t`
    The 'Int' scalar type represents non-fractional signed whole numeric
    values. Int can represent values between -(2^31) and 2^31 - 1.
  `

  I18NFloat.description = i18n.t`
    The 'Float' scalar type represents signed double-precision fractional
    values as specified by
    [IEEE 754](http://en.wikipedia.org/wiki/IEEE_floating_point).
  `

  I18NString.description = i18n.t`
    The 'String' scalar type represents textual data, represented as UTF-8
    character sequences. The String type is most often used by GraphQL to
    represent free-form human-readable text.
  `

  I18NBoolean.description = i18n.t`
    The 'Boolean' scalar type represents 'true' or 'false'.
  `

  return {
    I18NInt,
    I18NString,
    I18NFloat,
    I18NBoolean,
    Query: {
      dwelling: async (root, { houseId }, { client }) => {
        let query = {
          houseId,
        }

        return client.findOne(query)
      },
      dwellings: async (root, args, { client }) => {
        // TODO: look into the creation & handling of this next param
        // This is an opaque string that passes through the GraphQL type system
        // and is passed directly into library code to be decoded and used while
        // talking to the database.
        // ಠ_ಠ
        const { filters, limit, next } = args

        let query = {
          $and: [{}],
        }

        if (filters && filters.length > 0) {
          filters.forEach(filter => {
            let value = filter.value
            // if the value is a number
            // - optionally starting with a minus sign
            // - containing zero or one decimal places
            // convert it to a float instead of a string
            if (filter.value.match(/^-?\d+$|^-?\d+\.\d+$/)) {
              value = parseFloat(filter.value)
            }
            // We are evaling our own code here, not user input.
            // Filter.field is our code, stringified and stored in an enum.
            // The user choses one of the enum values and we convert the string
            // back to a function which accepts a matcher and generates the
            // query we need to find that field.
            // eslint-disable-next-line security/detect-eval-with-expression
            let queryGenerator = eval(filter.field) // eslint-disable-line no-eval
            let attrQuery = queryGenerator({
              [filter.comparator]: value,
            })
            query['$and'].push(attrQuery)
          })
        }

        let result = await MongoPaging.find(client, {
          query,
          next,
          limit,
        })

        return result
      },
    },
    Evaluation: {
      energyUpgrades: async root => {
        return root.energyUgrades
      },
    },
    Field: {
      dwellingHouseId: dwellingHouseId.toString(),
      dwellingYearBuilt: dwellingYearBuilt.toString(),
      dwellingCity: dwellingCity.toString(),
      dwellingRegion: dwellingRegion.toString(),
      dwellingForwardSortationArea: dwellingForwardSortationArea.toString(),
      ventilationTypeEnglish: ventilationTypeEnglish.toString(),
      ventilationTypeFrench: ventilationTypeFrench.toString(),
      ventilationAirFlowRateLps: ventilationAirFlowRateLps.toString(),
      ventilationAirFlowRateCfm: ventilationAirFlowRateCfm.toString(),
      ventilationEfficiency: ventilationEfficiency.toString(),
      floorLabel: floorLabel.toString(),
      floorInsulationNominalRsi: floorInsulationNominalRsi.toString(),
      floorInsulationNominalR: floorInsulationNominalR.toString(),
      floorInsulationEffectiveRsi: floorInsulationEffectiveRsi.toString(),
      floorInsulationEffectiveR: floorInsulationEffectiveR.toString(),
      floorAreaMetres: floorAreaMetres.toString(),
      floorAreaFeet: floorAreaFeet.toString(),
      floorLengthMetres: floorLengthMetres.toString(),
      floorLengthFeet: floorLengthFeet.toString(),
      waterHeatingTypeEnglish: waterHeatingTypeEnglish.toString(),
      waterHeatingTypeFrench: waterHeatingTypeFrench.toString(),
      waterHeatingTankVolumeLitres: waterHeatingTankVolumeLitres.toString(),
      waterHeatingTankVolumeGallon: waterHeatingTankVolumeGallon.toString(),
      waterHeatingEfficiency: waterHeatingEfficiency.toString(),
      heatingLabel: heatingLabel.toString(),
      heatingHeatingTypeEnglish: heatingHeatingTypeEnglish.toString(),
      heatingHeatingTypeFrench: heatingHeatingTypeFrench.toString(),
      heatingEnergySourceEnglish: heatingEnergySourceEnglish.toString(),
      heatingEnergySourceFrench: heatingEnergySourceFrench.toString(),
      heatingEquipmentTypeEnglish: heatingEquipmentTypeEnglish.toString(),
      heatingEquipmentTypeFrench: heatingEquipmentTypeFrench.toString(),
      heatingOutputSizeKW: heatingOutputSizeKW.toString(),
      heatingOutputSizeBtu: heatingOutputSizeBtu.toString(),
      heatingEfficiency: heatingEfficiency.toString(),
      heatingSteadyState: heatingSteadyState.toString(),
      heatedFloorAreaAreaAboveGradeMetres: heatedFloorAreaAreaAboveGradeMetres.toString(),
      heatedFloorAreaAreaAboveGradeFeet: heatedFloorAreaAreaAboveGradeFeet.toString(),
      heatedFloorAreaAreaBelowGradeMetres: heatedFloorAreaAreaBelowGradeMetres.toString(),
      heatedFloorAreaAreaBelowGradeFeet: heatedFloorAreaAreaBelowGradeFeet.toString(),
      wallLabel: wallLabel.toString(),
      wallStructureTypeEnglish: wallStructureTypeEnglish.toString(),
      wallStructureTypeFrench: wallStructureTypeFrench.toString(),
      wallComponentTypeSizeEnglish: wallComponentTypeSizeEnglish.toString(),
      wallComponentTypeSizeFrench: wallComponentTypeSizeFrench.toString(),
      wallInsulationNominalRsi: wallInsulationNominalRsi.toString(),
      wallInsulationNominalR: wallInsulationNominalR.toString(),
      wallInsulationEffectiveRsi: wallInsulationEffectiveRsi.toString(),
      wallInsulationEffectiveR: wallInsulationEffectiveR.toString(),
      wallAreaMetres: wallAreaMetres.toString(),
      wallAreaFeet: wallAreaFeet.toString(),
      wallPerimeterMetres: wallPerimeterMetres.toString(),
      wallPerimeterFeet: wallPerimeterFeet.toString(),
      wallHeightMetres: wallHeightMetres.toString(),
      wallHeightFeet: wallHeightFeet.toString(),
      ceilingLabel: ceilingLabel.toString(),
      ceilingTypeEnglish: ceilingTypeEnglish.toString(),
      ceilingTypeFrench: ceilingTypeFrench.toString(),
      ceilingInsulationNominalRsi: ceilingInsulationNominalRsi.toString(),
      ceilingInsulationNominalR: ceilingInsulationNominalR.toString(),
      ceilingInsulationEffectiveRsi: ceilingInsulationEffectiveRsi.toString(),
      ceilingInsulationEffectiveR: ceilingInsulationEffectiveR.toString(),
      ceilingAreaMetres: ceilingAreaMetres.toString(),
      ceilingAreaFeet: ceilingAreaFeet.toString(),
      ceilingLengthMetres: ceilingLengthMetres.toString(),
      ceilingLengthFeet: ceilingLengthFeet.toString(),
    },
    Comparator: {
      gt: '$gt',
      lt: '$lt',
      eq: '$eq',
    },
  }
}

export { Resolvers }

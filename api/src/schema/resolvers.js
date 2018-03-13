import MongoPaging from 'mongo-cursor-pagination'
import { GraphQLError } from 'graphql'

/* eslint-disable import/named */
import {
  dwellingHouseId,
  dwellingYearBuilt,
  dwellingCity,
  dwellingRegion,
  dwellingForwardSortationArea,
  evaluationEvaluationType,
  evaluationFileId,
  evaluationErsRating,
  evaluationEntryDate,
  evaluationCreationDate,
  evaluationModificationDate,
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
  waterHeatingEfficiencyEf,
  waterHeatingEfficiencyPercentage,
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
  doorTypeEnglish,
  doorTypeFrench,
  doorInsulationRsi,
  doorInsulationR,
  doorUFactor,
  doorUFactorImperial,
  doorAreaMetres,
  doorAreaFeet,
  windowLabel,
  windowInsulationRsi,
  windowInsulationR,
  windowGlazingTypesEnglish,
  windowGlazingTypesFrench,
  windowCoatingsTintsEnglish,
  windowCoatingsTintsFrench,
  windowFillTypeEnglish,
  windowFillTypeFrench,
  windowSpacerTypeEnglish,
  windowSpacerTypeFrench,
  windowTypeEnglish,
  windowTypeFrench,
  windowFrameMaterialEnglish,
  windowFrameMaterialFrench,
  windowAreaMetres,
  windowAreaFeet,
  windowWidthMetres,
  windowWidthFeet,
  windowHeightMetres,
  windowHeightFeet,
  foundationFoundationTypeEnglish,
  foundationFoundationTypeFrench,
  foundationLabel,
  foundationConfigurationType,
  foundationMaterialEnglish,
  foundationMaterialFrench,
  foundationHeaderInsulationNominalRsi,
  foundationHeaderInsulationNominalR,
  foundationHeaderInsulationEffectiveRsi,
  foundationHeaderInsulationEffectiveR,
  foundationHeaderAreaMetres,
  foundationHeaderAreaFeet,
  foundationHeaderPerimeterMetres,
  foundationHeaderPerimeterFeet,
  foundationHeaderHeightMetres,
  foundationHeaderHeightFeet,
  foundationFloorFloorTypeEnglish,
  foundationFloorFloorTypeFrench,
  foundationFloorInsulationNominalRsi,
  foundationFloorInsulationNominalR,
  foundationFloorInsulationEffectiveRsi,
  foundationFloorInsulationEffectiveR,
  foundationFloorAreaMetres,
  foundationFloorAreaFeet,
  foundationFloorPerimeterMetres,
  foundationFloorPerimeterFeet,
  foundationFloorWidthMetres,
  foundationFloorWidthFeet,
  foundationFloorLengthMetres,
  foundationFloorLengthFeet,
  foundationWallWallTypeEnglish,
  foundationWallWallTypeFrench,
  foundationWallInsulationNominalRsi,
  foundationWallInsulationNominalR,
  foundationWallInsulationEffectiveRsi,
  foundationWallInsulationEffectiveR,
  foundationWallPercentage,
  foundationWallAreaMetres,
  foundationWallAreaFeet,
} from './enums'
/* eslint-enable import/named */

import { createI18NFloat } from './types/I18NFloat'
import { createI18NInt } from './types/I18NInt'
import { createI18NString } from './types/I18NString'
import { createI18NBoolean } from './types/I18NBoolean'
import { createI18NDate } from './types/I18NDate'

const Resolvers = i18n => {
  return {
    Int: createI18NInt(i18n),
    String: createI18NString(i18n),
    I18NFloat: createI18NFloat(i18n),
    Boolean: createI18NBoolean(i18n),
    Date: createI18NDate(i18n),
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
        const { filters, dateRange, limit, next, previous } = args

        if (next && previous) {
          throw new GraphQLError(
            i18n.t`
              Cannot submit values for both 'next' and 'previous'.
            `,
          )
        }

        let query = {
          $and: [{}],
        }

        if (dateRange) {
          // ISO string format looks like "2012-10-01T15:08:41.000Z"
          const startDateQuery = dateRange.startDate
            ? { $gte: dateRange.startDate.toISOString().split('T')[0] }
            : {}
          const endDateQuery = dateRange.endDate
            ? { $lte: dateRange.endDate.toISOString().split('T')[0] }
            : {}

          const dateQuery = Object.assign({}, startDateQuery, endDateQuery)

          if (Object.keys(dateQuery).length === 0) {
            throw new GraphQLError(
              i18n.t`
                A 'dateRange' must include a 'startDate' or an 'endDate'.
                `,
            )
          }

          if (
            dateQuery['$gte'] &&
            dateQuery['$lte'] &&
            dateQuery['$gte'] >= dateQuery['$lte']
          ) {
            throw new GraphQLError(
              i18n.t`
                The 'endDate' cannot be equal to or earlier than the 'startDate'.
                `,
            )
          }

          // eslint-disable-next-line security/detect-eval-with-expression
          let queryGenerator = eval(dateRange.field) // eslint-disable-line no-eval
          let attrQuery = queryGenerator(dateQuery)
          query['$and'].push(attrQuery)
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
          previous,
          limit,
        })

        return result
      },
    },
    DateField: {
      evaluationEntryDate: evaluationEntryDate.toString(),
      evaluationCreationDate: evaluationCreationDate.toString(),
      evaluationModificationDate: evaluationModificationDate.toString(),
    },
    Field: {
      dwellingHouseId: dwellingHouseId.toString(),
      dwellingYearBuilt: dwellingYearBuilt.toString(),
      dwellingCity: dwellingCity.toString(),
      dwellingRegion: dwellingRegion.toString(),
      dwellingForwardSortationArea: dwellingForwardSortationArea.toString(),
      evaluationEvaluationType: evaluationEvaluationType.toString(),
      evaluationFileId: evaluationFileId.toString(),
      evaluationErsRating: evaluationErsRating.toString(),
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
      waterHeatingEfficiencyEf: waterHeatingEfficiencyEf.toString(),
      waterHeatingEfficiencyPercentage: waterHeatingEfficiencyPercentage.toString(),
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
      doorTypeEnglish: doorTypeEnglish.toString(),
      doorTypeFrench: doorTypeFrench.toString(),
      doorInsulationRsi: doorInsulationRsi.toString(),
      doorInsulationR: doorInsulationR.toString(),
      doorUFactor: doorUFactor.toString(),
      doorUFactorImperial: doorUFactorImperial.toString(),
      doorAreaMetres: doorAreaMetres.toString(),
      doorAreaFeet: doorAreaFeet.toString(),
      windowLabel: windowLabel.toString(),
      windowInsulationRsi: windowInsulationRsi.toString(),
      windowInsulationR: windowInsulationR.toString(),
      windowGlazingTypesEnglish: windowGlazingTypesEnglish.toString(),
      windowGlazingTypesFrench: windowGlazingTypesFrench.toString(),
      windowCoatingsTintsEnglish: windowCoatingsTintsEnglish.toString(),
      windowCoatingsTintsFrench: windowCoatingsTintsFrench.toString(),
      windowFillTypeEnglish: windowFillTypeEnglish.toString(),
      windowFillTypeFrench: windowFillTypeFrench.toString(),
      windowSpacerTypeEnglish: windowSpacerTypeEnglish.toString(),
      windowSpacerTypeFrench: windowSpacerTypeFrench.toString(),
      windowTypeEnglish: windowTypeEnglish.toString(),
      windowTypeFrench: windowTypeFrench.toString(),
      windowFrameMaterialEnglish: windowFrameMaterialEnglish.toString(),
      windowFrameMaterialFrench: windowFrameMaterialFrench.toString(),
      windowAreaMetres: windowAreaMetres.toString(),
      windowAreaFeet: windowAreaFeet.toString(),
      windowWidthMetres: windowWidthMetres.toString(),
      windowWidthFeet: windowWidthFeet.toString(),
      windowHeightMetres: windowHeightMetres.toString(),
      windowHeightFeet: windowHeightFeet.toString(),
      foundationFoundationTypeEnglish: foundationFoundationTypeEnglish.toString(),
      foundationFoundationTypeFrench: foundationFoundationTypeFrench.toString(),
      foundationLabel: foundationLabel.toString(),
      foundationConfigurationType: foundationConfigurationType.toString(),
      foundationMaterialEnglish: foundationMaterialEnglish.toString(),
      foundationMaterialFrench: foundationMaterialFrench.toString(),
      foundationHeaderInsulationNominalRsi: foundationHeaderInsulationNominalRsi.toString(),
      foundationHeaderInsulationNominalR: foundationHeaderInsulationNominalR.toString(),
      foundationHeaderInsulationEffectiveRsi: foundationHeaderInsulationEffectiveRsi.toString(),
      foundationHeaderInsulationEffectiveR: foundationHeaderInsulationEffectiveR.toString(),
      foundationHeaderAreaMetres: foundationHeaderAreaMetres.toString(),
      foundationHeaderAreaFeet: foundationHeaderAreaFeet.toString(),
      foundationHeaderPerimeterMetres: foundationHeaderPerimeterMetres.toString(),
      foundationHeaderPerimeterFeet: foundationHeaderPerimeterFeet.toString(),
      foundationHeaderHeightMetres: foundationHeaderHeightMetres.toString(),
      foundationHeaderHeightFeet: foundationHeaderHeightFeet.toString(),
      foundationFloorFloorTypeEnglish: foundationFloorFloorTypeEnglish.toString(),
      foundationFloorFloorTypeFrench: foundationFloorFloorTypeFrench.toString(),
      foundationFloorInsulationNominalRsi: foundationFloorInsulationNominalRsi.toString(),
      foundationFloorInsulationNominalR: foundationFloorInsulationNominalR.toString(),
      foundationFloorInsulationEffectiveRsi: foundationFloorInsulationEffectiveRsi.toString(),
      foundationFloorInsulationEffectiveR: foundationFloorInsulationEffectiveR.toString(),
      foundationFloorAreaMetres: foundationFloorAreaMetres.toString(),
      foundationFloorAreaFeet: foundationFloorAreaFeet.toString(),
      foundationFloorPerimeterMetres: foundationFloorPerimeterMetres.toString(),
      foundationFloorPerimeterFeet: foundationFloorPerimeterFeet.toString(),
      foundationFloorWidthMetres: foundationFloorWidthMetres.toString(),
      foundationFloorWidthFeet: foundationFloorWidthFeet.toString(),
      foundationFloorLengthMetres: foundationFloorLengthMetres.toString(),
      foundationFloorLengthFeet: foundationFloorLengthFeet.toString(),
      foundationWallWallTypeEnglish: foundationWallWallTypeEnglish.toString(),
      foundationWallWallTypeFrench: foundationWallWallTypeFrench.toString(),
      foundationWallInsulationNominalRsi: foundationWallInsulationNominalRsi.toString(),
      foundationWallInsulationNominalR: foundationWallInsulationNominalR.toString(),
      foundationWallInsulationEffectiveRsi: foundationWallInsulationEffectiveRsi.toString(),
      foundationWallInsulationEffectiveR: foundationWallInsulationEffectiveR.toString(),
      foundationWallPercentage: foundationWallPercentage.toString(),
      foundationWallAreaMetres: foundationWallAreaMetres.toString(),
      foundationWallAreaFeet: foundationWallAreaFeet.toString(),
    },
    Comparator: {
      gt: '$gt',
      lt: '$lt',
      eq: '$eq',
    },
  }
}

export { Resolvers }

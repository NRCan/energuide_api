import resolvers from './resolvers'
import { makeExecutableSchema } from 'graphql-tools'

const Schema = i18n => {
  const typeDefs = `
    scalar ForwardSortationArea

    enum Comparator {
      gt
      lt
      eq
    }

    input Filter {
      field: Field!
      comparator: Comparator!
      value: String!
    }

    type Ventilation {
      typeEnglish: String
      typeFrench: String
      airFlowRateLps: Float
      airFlowRateCfm: Float
    }

    type Floor {
      label: String
      insulationNominalRsi: Float
      insulationNominalR: Float
      insulationEffectiveRsi: Float
      insulationEffectiveR: Float
      areaMetres: Float
      areaFeet: Float
      lengthMetres: Float
      lengthFeet: Float
    }

    type WaterHeater {
      typeEnglish: String
      typeFrench: String
      tankVolumeLitres: Float
      tankVolumeGallon: Float
      efficiency: Float
    }

    type PaginatedResultSet {
      hasNext: Boolean
      hasPrevious: Boolean
      next: String
      previous: String
      results: [Dwelling]
    }

    type HeatedFloorArea {
      areaAboveGradeMetres: Float
      areaAboveGradeFeet: Float
      areaBelowGradeMetres: Float
      areaBelowGradeFeet: Float
    }

    type Wall {
      label: String
      structureTypeEnglish: String
      structureTypeFrench: String
      componentTypeSizeEnglish: String
      componentTypeSizeFrench: String
      insulationNominalRsi: Float
      insulationNominalR: Float
      insulationEffectiveRsi: Float
      insulationEffectiveR: Float
      areaMetres: Float
      areaFeet: Float
      perimeterMetres: Float
      perimeterFeet: Float
      heightMetres: Float
      heightFeet: Float
    }

    type Door {
      typeEnglish: String
      typeFrench: String
      insulationRsi: Float
      insulationR: Float
      uFactor: Float
      uFactorImperial: Float
      areaMetres: Float
      areaFeet: Float
    }

    type Window {
      label: String
      insulationRsi: Float
      insulationR: Float
      glazingTypesEnglish: String
      glazingTypesFrench: String
      coatingsTintsEnglish: String
      coatingsTintsFrench: String
      fillTypeEnglish: String
      fillTypeFrench: String
      spacerTypeEnglish: String
      spacerTypeFrench: String
      typeEnglish: String
      typeFrench: String
      frameMaterialEnglish: String
      frameMaterialFrench: String
      areaMetres: Float
      areaFeet: Float
      widthMetres: Float
      widthFeet: Float
      heightMetres: Float
      heightFeet: Float
    }

    type Ceiling {
      label: String
      typeEnglish: String
      typeFrench: String
      insulationNominalRsi: Float
      insulationNominalR: Float
      insulationEffectiveRsi: Float
      insulationEffectiveR: Float
      areaMetres: Float
      areaFeet: Float
      lengthMetres: Float
      lengthFeet: Float
    }

    # ${i18n.t`This is a description of evaluations`}
    type Evaluation {
      evaluationType: String
      entryDate: String
      creationDate: String
      modificationDate: String
      ceilings: [Ceiling]
      walls: [Wall]
      floors: [Floor]
      doors: [Door]
      windows: [Window]
      heatedFloorArea: HeatedFloorArea
      ventilations: [Ventilation]
      waterHeatings: [WaterHeater]
    }


    # ${i18n.t`A residential building evaluted under the Energuide program`}
    type Dwelling {
      houseId: Int
      # ${i18n.t`Year of construction`}
      yearBuilt: Int
      city: String
      region: String
      forwardSortationArea: String
      evaluations: [Evaluation]
    }

    # ${i18n.t`The root query type`}
    type Query {
      # ${i18n.t`Details for a specific dwelling`}
      dwelling(houseId: Int!): Dwelling
      dwellingsInFSA(filters: [Filter!] forwardSortationArea: ForwardSortationArea! limit: Int, next: String): PaginatedResultSet
    }

    enum Field {
      dwellingHouseId
      dwellingYearBuilt
      dwellingCity
      dwellingRegion
      dwellingForwardSortationArea
      ventilationTypeEnglish
      ventilationTypeFrench
      ventilationAirFlowRateLps
      ventilationAirFlowRateCfm
      ventilationEfficiency
      floorLabel
      floorInsulationNominalRsi
      floorInsulationNominalR
      floorInsulationEffectiveRsi
      floorInsulationEffectiveR
      floorAreaMetres
      floorAreaFeet
      floorLengthMetres
      floorLengthFeet
    }
  `

  return makeExecutableSchema({ typeDefs, resolvers })
}

export default Schema

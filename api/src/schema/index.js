import resolvers from './resolvers'
import { makeExecutableSchema } from 'graphql-tools'

const Schema = i18n => {
  const typeDefs = `
    scalar ForwardSortationArea

    # ${i18n.t`An operator to describe how results will be filtered`}
    enum Comparator {
      # ${i18n.t`Greater than: returns true for results greater than the comparison value`}
      gt
      # ${i18n.t`Less than: returns true for results less than the comparison value`}
      lt
      # ${i18n.t`Equal to: returns true for results equal to the comparison value`}
      eq
    }

    # ${i18n.t`Filters will return results only if they satisfy a condition`}
    input Filter {
      # ${i18n.t`Name of field results will be filtered by`}
      field: Field!
      # ${i18n.t`An operator to describe how results will be filtered`}
      comparator: Comparator!
      # ${i18n.t`Results will be compared to this value`}
      value: String!
    }

    # ${i18n.t`Ventilation systems draw exterior air into the house, exhaust interior air to the exterior, or both`}
    type Ventilation {
      # ${i18n.t`Ventilation type installed (en)`}
      typeEnglish: String
      # ${i18n.t`Ventilation type installed (fr)`}
      typeFrench: String
      # ${i18n.t`Air flow rate in Litres per Second (LpS)`}
      airFlowRateLps: Float
      # ${i18n.t`Air flow rate in Cubic feet per Minute (CfM)`}
      airFlowRateCfm: Float
    }

    # ${i18n.t`Floors represents the usable area of the house`}
    type Floor {
      # ${i18n.t`Description of floor location`}
      label: String
      # ${i18n.t`Floor insulation nominal RSI (R-value Systeme International)`}
      insulationNominalRsi: Float
      # ${i18n.t`Floor insulation nominal R-value`}
      insulationNominalR: Float
      # ${i18n.t`Floor insulation effective RSI (R-value Systeme International)`}
      insulationEffectiveRsi: Float
      # ${i18n.t`Floor insulation effective R-value`}
      insulationEffectiveR: Float
      # ${i18n.t`Floor area of the house in square metres (m2)`}
      areaMetres: Float
      # ${i18n.t`Floor area of the house in square feet (ft2)`}
      areaFeet: Float
      # ${i18n.t`Floor length of the house in metres (m)`}
      lengthMetres: Float
      # ${i18n.t`Floor area of the house in feet (ft)`}
      lengthFeet: Float
    }

    # ${i18n.t`Water heaters heat the domestic hot water in a house`}
    type WaterHeater {
      # ${i18n.t`Type of tank being used to heat the domestic hot water in the house (en)`}
      typeEnglish: String
      # ${i18n.t`Type of tank being used to heat the domestic hot water in the house (fr)`}
      typeFrench: String
      # ${i18n.t`Volume of the tank capacity in Litres (L)`}
      tankVolumeLitres: Float
      # ${i18n.t`Volume of the tank capacity in Gallons (G)`}
      tankVolumeGallon: Float
      # ${i18n.t`Measures how effectively your water heater is burning fuel or turning fuel into heat`}
      efficiency: Float
    }

    # ${i18n.t`One page of results`}
    type PaginatedResultSet {
      # ${i18n.t`If true, a further page of results can be returned`}
      hasNext: Boolean
      # ${i18n.t`If true, a previous page of results can be returned`}
      hasPrevious: Boolean
      # ${i18n.t`Identifier used to return the next page of results`}
      next: String
      # ${i18n.t`Identifier cursor used to return the previous page of results`}
      previous: String
      # ${i18n.t`A list of dwellings`}
      results: [Dwelling]
    }

    # ${i18n.t`Heated floor areas represents the usable areas of a house that is conditioned to a specified temperature during the whole heating season`}
    type HeatedFloorArea {
      # ${i18n.t`Above-grade heated area of the house in square metres (m2), i.e. the ground floor`}
      areaAboveGradeMetres: Float
      # ${i18n.t`Above-grade heated area of the house in square feet (ft2), i.e. the ground floor`}
      areaAboveGradeFeet: Float
      # ${i18n.t`Below-grade heated area of the house in square metres (m2), i.e. the basement`}
      areaBelowGradeMetres: Float
      # ${i18n.t`Below-grade heated area of the house in square feet (ft2), i.e. the basement`}
      areaBelowGradeFeet: Float
    }

    # ${i18n.t`Walls separate the interior heated space from the outside (interior partition walls are not considered walls)`}
    type Wall {
      # ${i18n.t`Description of wall location`}
      label: String
      # ${i18n.t`Wall construction being used (en)`}
      structureTypeEnglish: String
      # ${i18n.t`Wall construction being used (fr)`}
      structureTypeFrench: String
      # ${i18n.t`Size of the component type (en)`}
      componentTypeSizeEnglish: String
      # ${i18n.t`Size of the component type (fr)`}
      componentTypeSizeFrench: String
      # ${i18n.t`Wall insulation nominal RSI (R-value Systeme International)`}
      insulationNominalRsi: Float
      # ${i18n.t`Wall insulation nominal R-value`}
      insulationNominalR: Float
      # ${i18n.t`Wall insulation effective RSI (R-value Systeme International)`}
      insulationEffectiveRsi: Float
      # ${i18n.t`Wall insulation nominal R-value`}
      insulationEffectiveR: Float
      # ${i18n.t`Wall area of the house in square metres (m2)`}
      areaMetres: Float
      # ${i18n.t`Wall area of the house in square feet (ft2)`}
      areaFeet: Float
      # ${i18n.t`Wall perimeter of the house in metres (m)`}
      perimeterMetres: Float
      # ${i18n.t`Wall perimeter of the house in feet (ft)`}
      perimeterFeet: Float
      # ${i18n.t`Wall height of the house in metres (m)`}
      heightMetres: Float
      # ${i18n.t`Wall height of the house in feet (ft)`}
      heightFeet: Float
    }

    # ${i18n.t`Doors are on outside walls, separating the interior heated space from the outside`}
    type Door {
      # ${i18n.t`Describes the construction of the door (en)`}
      typeEnglish: String
      # ${i18n.t`Describes the construction of the door (fr)`}
      typeFrench: String
      # ${i18n.t`Door RSI (R-value Systeme International)`}
      insulationRsi: Float
      # ${i18n.t`Door R-value`}
      insulationR: Float
      # ${i18n.t`Door U-factor in metric: Watts per square metre per degree Celcius (W/m2C)`}
      uFactor: Float
      # ${i18n.t`Door U-factor in imperial: British Thermal Units per square feet per degree Fahrenheit (BTU/ft2 F)`}
      uFactorImperial: Float
      # ${i18n.t`Door area in square metres (m2)`}
      areaMetres: Float
      # ${i18n.t`Door area in square feet (ft2)`}
      areaFeet: Float
    }

    # ${i18n.t`Windows separate the interior heated space from the outside`}
    type Window {
      # ${i18n.t`Used to identify the window component in the house`}
      label: String
      # ${i18n.t`Window RSI (R-value Systeme International)`}
      insulationRsi: Float
      # ${i18n.t`Window R-value`}
      insulationR: Float
      # ${i18n.t`Number of panes of transparent material in a window (en)`}
      glazingTypesEnglish: String
      # ${i18n.t`Number of panes of transparent material in a window (fr)`}
      glazingTypesFrench: String
      # ${i18n.t`Type of coating and tint on a window pane (en)`}
      coatingsTintsEnglish: String
      # ${i18n.t`Type of coating and tint on a window pane (fr)`}
      coatingsTintsFrench: String
      # ${i18n.t`Type of gas (air, argon or krypton) injected between the glass layers (en)`}
      fillTypeEnglish: String
      # ${i18n.t`Type of gas (air, argon or krypton) injected between the glass layers (fr)`}
      fillTypeFrench: String
      # ${i18n.t`Spacer systems used between the glass layers (en)`}
      spacerTypeEnglish: String
      # ${i18n.t`Spacer systems used between the glass layers (fr)`}
      spacerTypeFrench: String
      # ${i18n.t`Describes the construction of the window (en)`}
      typeEnglish: String
      # ${i18n.t`Describes the construction of the window (fr)`}
      typeFrench: String
      # ${i18n.t`Material type of the window frame (en)`}
      frameMaterialEnglish: String
      # ${i18n.t`Material type of the window frame (fr)`}
      frameMaterialFrench: String
      # ${i18n.t`Window area in square metres (m2)`}
      areaMetres: Float
      # ${i18n.t`Window area in square feet (ft2)`}
      areaFeet: Float
      # ${i18n.t`Window width in metres (m)`}
      widthMetres: Float
      # ${i18n.t`Window width in feet (ft)`}
      widthFeet: Float
      # ${i18n.t`Window height in metres (m)`}
      heightMetres: Float
      # ${i18n.t`Window height in feet (ft)`}
      heightFeet: Float
    }

    # ${i18n.t`Ceilings are the upper interior surface of a room`}
    type Ceiling {
      # ${i18n.t`Used to identify the ceiling in the house`}
      label: String
      # ${i18n.t`Describes the construction of the ceiling (en)`}
      typeEnglish: String
      # ${i18n.t`Describes the construction of the ceiling (fr)`}
      typeFrench: String
      # ${i18n.t`Ceiling insulation nominal RSI (R-value Systeme International)`}
      insulationNominalRsi: Float
      # ${i18n.t`Ceiling insulation nominal R-value`}
      insulationNominalR: Float
      # ${i18n.t`Ceiling insulation effective RSI (R-value Systeme International)`}
      insulationEffectiveRsi: Float
      # ${i18n.t`Ceiling insulation effective R-value`}
      insulationEffectiveR: Float
      # ${i18n.t`Ceiling area in square metres (m2)`}
      areaMetres: Float
      # ${i18n.t`Ceiling area in square feet (ft2)`}
      areaFeet: Float
      # ${i18n.t`Ceiling length in metres (m)`}
      lengthMetres: Float
      # ${i18n.t`Ceiling length in feet (ft)`}
      lengthFeet: Float
    }

    # ${i18n.t`Detailed information about specific features of a given dwelling`}
    type Evaluation {
      # ${i18n.t`Evaluation type codes are used to define the type of evaluation performed and to distinguish the house type (i.e. newly built or existing)`}
      evaluationType: String
      # ${i18n.t`Date the evaluation was made`}
      entryDate: String
      # ${i18n.t`Date the record was first created`}
      creationDate: String
      # ${i18n.t`Date the record was last modified`}
      modificationDate: String
      # ${i18n.t`A list of ceiling data entries for a dwelling`}
      ceilings: [Ceiling]
      # ${i18n.t`A list of wall data entries for a dwelling`}
      walls: [Wall]
      # ${i18n.t`A list of floor data entries for a dwelling`}
      floors: [Floor]
      # ${i18n.t`A list of door data entries for a dwelling`}
      doors: [Door]
      # ${i18n.t`A list of window data entries for a dwelling`}
      windows: [Window]
      # ${i18n.t`A heated floor area entry for a dwelling`}
      heatedFloorArea: HeatedFloorArea
      # ${i18n.t`A list of ventilation data entries for a dwelling`}
      ventilations: [Ventilation]
      # ${i18n.t`A list of water heater data entries for a dwelling`}
      waterHeatings: [WaterHeater]
    }


    # ${i18n.t`A residential building evaluted under the Energuide program`}
    type Dwelling {
      # ${i18n.t`Unique identification number for a dwelling`}
      houseId: Int
      # ${i18n.t`Year of construction`}
      yearBuilt: Int
      # ${i18n.t`Name of city where dwelling is located`}
      city: String
      # ${i18n.t`Region of country for dwelling (province/territory)`}
      region: String
      # ${i18n.t`The first three characters of a Canadian postal code, which correspond to a geographical area defined by Canada Post`}
      forwardSortationArea: String
      # ${i18n.t`A list of evaluations of specific features of the dwelling`}
      evaluations: [Evaluation]
    }

    # ${i18n.t`The root query type`}
    type Query {
      # ${i18n.t`Details for a specific dwelling`}
      dwelling(houseId: Int!): Dwelling
      # ${i18n.t`Details for all dwellings in a specfified forward sortation area, optionally filtered by one or more values`}
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

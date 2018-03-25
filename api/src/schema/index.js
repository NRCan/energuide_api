import { Resolvers } from './resolvers'
import { makeExecutableSchema } from 'graphql-tools'

import { createFoundation } from './types/Foundation'
import { createFoundationFloor } from './types/FoundationFloor'
import { createFoundationWall } from './types/FoundationWall'
import { createHeader } from './types/Header'

const Schema = i18n => {
  const typeDefs = [
    `
    scalar Int
    scalar Float
    scalar String
    scalar Boolean
    scalar Date

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

    # ${i18n.t`Filter by dwellings containing evaluations that were entered, created, or modified between a range of dates`}
    input DateRange {
      # ${i18n.t`Name of the date field results will be filtered by`}
      field: DateField!
      # ${i18n.t`Evaluation dates must be equal to or later than this value`}
      startDate: Date
      # ${i18n.t`Evaluation dates must be equal to or earlier than this value`}
      endDate: Date
    }

    # ${i18n.t`An improvement that could increase the energy efficiency of the dwelling`}
    type Upgrade @cacheControl(maxAge: 90) {
      # ${i18n.t`Part of the dwelling to be upgraded`}
      upgradeType: String
      # ${i18n.t`Estimated cost of upgrade`}
      cost: Int
      # ${i18n.t`Order of importance of upgrade recommendation (lower number means a higher priority)`}
      priority: Int
    }

    # ${i18n.t`One page of results`}
    type PaginatedResultSet @cacheControl(maxAge: 90) {
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
    type HeatedFloorArea @cacheControl(maxAge: 90) {
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
    type Wall @cacheControl(maxAge: 90) {
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

    # ${i18n.t`Ceilings are the upper interior surface of a room`}
    type Ceiling @cacheControl(maxAge: 90) {
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
    type Evaluation @cacheControl(maxAge: 90) {
      # ${i18n.t`Evaluation type codes are used to define the type of evaluation performed and to distinguish the house type (i.e. newly built or existing)`}
      evaluationType: String
      # ${i18n.t`Date the evaluation was made`}
      entryDate: String
      fileId: String
      # ${i18n.t`Date the record was first created`}
      creationDate: String
      # ${i18n.t`Date the record was last modified`}
      modificationDate: String
      # ${i18n.t`A list of ceiling data entries for a dwelling`}
      ceilings: [Ceiling]
      # ${i18n.t`A list of wall data entries for a dwelling`}
      walls: [Wall]
      # ${i18n.t`A heated floor area entry for a dwelling`}
      heatedFloorArea: HeatedFloorArea
      # ${i18n.t`A list of upgrades that would improve energy efficiency`}
      energyUpgrades: [Upgrade]
      # ${i18n.t`The details of the foundation`}
      foundations: [Foundation]
      # ${i18n.t`The EnerGuide Rating calculated for this evaluation`}
      ersRating: Int
    }

    # ${i18n.t`A residential building evaluted under the Energuide program`}
    type Dwelling @cacheControl(maxAge: 90) {
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
    type Query @cacheControl(maxAge: 90) {
      # ${i18n.t`Details for a specific dwelling`}
      dwelling(houseId: Int!): Dwelling
      # ${i18n.t`Details for all dwellings, optionally filtered by one or more values`}
      dwellings(filters: [Filter!] dateRange: DateRange limit: Int next: String previous: String): PaginatedResultSet
    }

    # ${i18n.t`An ISO date value, formatted 'YYYY-MM-DD'`}
    enum DateField {
      # ${i18n.t`Filter results by the dwellings containing at least one evaluation with a specific entry date`}
      evaluationEntryDate
      # ${i18n.t`Filter results by the dwellings containing at least one evaluation with a specific record creation date`}
      evaluationCreationDate
      # ${i18n.t`Filter results by the dwellings containing at least one evaluation with a specific record modification date`}
      evaluationModificationDate
    }

    enum Field {
      # ${i18n.t`Filter results by the house ID of a dwelling`}
      dwellingHouseId
      # ${i18n.t`Filter results by dwellings built in a specific year`}
      dwellingYearBuilt
      # ${i18n.t`Filter results by the dwellings in a specific city`}
      dwellingCity
      # ${i18n.t`Filter results by the dwellings in a specific region`}
      dwellingRegion
      # ${i18n.t`Filter results by the dwellings in a specific forward sortation area`}
      dwellingForwardSortationArea
      # ${i18n.t`Filter results by the dwellings containing at least one evaluation with a specific evaluation type code`}
      evaluationEvaluationType
      # ${i18n.t`Filter results by the dwellings containing at least one evaluation with a specific evaluation ID`}
      evaluationFileId
      # ${i18n.t`Filter results by the dwellings containing at least one evaluation with a specific ERS rating`}
      evaluationErsRating
      # ${i18n.t`Filter results by the dwellings containing an above-grade heated floor area with a specific area in square metres (m2)`}
      heatedFloorAreaAreaAboveGradeMetres
      # ${i18n.t`Filter results by the dwellings containing an above-grade heated floor area with a specific area in square feet (ft2)`}
      heatedFloorAreaAreaAboveGradeFeet
      # ${i18n.t`Filter results by the dwellings containing a below-grade heated floor area with a specific area in square metres (m2)`}
      heatedFloorAreaAreaBelowGradeMetres
      # ${i18n.t`Filter results by the dwellings containing a below-grade heated floor area with a specific area in square feet (ft2)`}
      heatedFloorAreaAreaBelowGradeFeet
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific location`}
      wallLabel
      # ${i18n.t`Filter results by the dwellings containing at least one wall of a specific type (en)`}
      wallStructureTypeEnglish
      # ${i18n.t`Filter results by the dwellings containing at least one wall of a specific type (fr)`}
      wallStructureTypeFrench
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a component of a specific size (en)`}
      wallComponentTypeSizeEnglish
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a component of a specific size (fr)`}
      wallComponentTypeSizeFrench
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific nominal RSI (R-value Systeme International)`}
      wallInsulationNominalRsi
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific nominal R-value`}
      wallInsulationNominalR
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific effective RSI (R-value Systeme International)`}
      wallInsulationEffectiveRsi
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific effective R-value`}
      wallInsulationEffectiveR
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific area in square metres (m2)`}
      wallAreaMetres
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific area in square feet (ft2)`}
      wallAreaFeet
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific perimeter in metres (m)`}
      wallPerimeterMetres
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific perimeter in feet (ft)`}
      wallPerimeterFeet
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific height in metres (m)`}
      wallHeightMetres
      # ${i18n.t`Filter results by the dwellings containing at least one wall with a specific height in feet (ft)`}
      wallHeightFeet
      # ${i18n.t`Filter results by the dwellings where at least one ceiling has a matching label`}
      ceilingLabel
      # ${i18n.t`Filter results by the dwellings where at least one ceiling has a matching type (en)`}
      ceilingTypeEnglish
      # ${i18n.t`Filter results by the dwellings where at least one ceiling has a matching type (fr)`}
      ceilingTypeFrench
      # ${i18n.t`Filter results by the dwellings where at least one ceiling has a specific nominal RSI (R-value Systeme International)`}
      ceilingInsulationNominalRsi
      # ${i18n.t`Filter results by the dwellings containing at least one ceiling with a specific nominal R-value`}
      ceilingInsulationNominalR
      # ${i18n.t`Filter results by the dwellings containing at least one ceiling with a specific effective RSI (R-value Systeme International)`}
      ceilingInsulationEffectiveRsi
      # ${i18n.t`Filter results by the dwellings containing at least one ceiling with a specific effective R-value`}
      ceilingInsulationEffectiveR
      # ${i18n.t`Filter results by the dwellings containing at least one ceiling with a specific area in square metres (m2)`}
      ceilingAreaMetres
      # ${i18n.t`Filter results by the dwellings containing at least one ceiling with a specific area in square feet (ft2)`}
      ceilingAreaFeet
      # ${i18n.t`Filter results by the dwellings containing at least one ceiling with a specific length in metres (m)`}
      ceilingLengthMetres
      # ${i18n.t`Filter results by the dwellings containing at least one ceiling with a specific length in feet (ft)`}
      ceilingLengthFeet
      # ${i18n.t`Filter results for dwellings with matching foundation type (en)`}
      foundationFoundationTypeEnglish
      # ${i18n.t`Filter results for dwellings with matching foundation type (fr)`}
      foundationFoundationTypeFrench
      # ${i18n.t`Filter results for dwellings with a specific foundation label`}
      foundationLabel
      # ${i18n.t`Filter results for dwellings with a specific foundation configuration`}
      foundationConfigurationType
      # ${i18n.t`Filter results for dwellings whose foundation was constructed with a specific material (en)`}
      foundationMaterialEnglish
      # ${i18n.t`Filter results for dwellings whose foundation was constructed with a specific material (en)`}
      foundationMaterialFrench
      # ${i18n.t`Filter results for dwellings with a specific foundation header insulation nominal RSI (R-value Systeme International)`}
      foundationHeaderInsulationNominalRsi
      # ${i18n.t`Filter results for dwellings with a specific foundation header insulation nominal R-value`}
      foundationHeaderInsulationNominalR
      # ${i18n.t`Filter results for dwellings with a specific foundation header insulation effective RSI (R-value Systeme International)`}
      foundationHeaderInsulationEffectiveRsi
      # ${i18n.t`Filter results for dwellings with a specific foundationn header insulation effective R-value`}
      foundationHeaderInsulationEffectiveR
      # ${i18n.t`Filter results for dwellings with a specific foundation header area in square metres (m2)`}
      foundationHeaderAreaMetres
      # ${i18n.t`Filter results for dwellings with a specific foundation header area in square feet (ft2)`}
      foundationHeaderAreaFeet
      # ${i18n.t`Filter results for dwellings with a specific foundation header perimeter in metres (m)`}
      foundationHeaderPerimeterMetres
      # ${i18n.t`Filter results for dwellings with a specific foundation header perimeter in feet (ft)`}
      foundationHeaderPerimeterFeet
      # ${i18n.t`Filter results for dwellings with a specific foundation header height in metres (m)`}
      foundationHeaderHeightMetres
      # ${i18n.t`Filter results for dwellings with a specific header height in feet (ft)`}
      foundationHeaderHeightFeet
      # ${i18n.t`Filter for dwellings with a specific type of foundation floor type (en)`}
      foundationFloorFloorTypeEnglish
      # ${i18n.t`Filter for dwellings with a specific type of foundation floor type (fr)`}
      foundationFloorFloorTypeFrench
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific insulation nominal RSI (R-value Systeme International)`}
      foundationFloorInsulationNominalRsi
      # ${i18n.t`Filter for dwellings with a specific insulation nominal R-value on the foundation floor`}
      foundationFloorInsulationNominalR
      # ${i18n.t`Filter for dwellings with a specific insulation effective RSI (R-value Systeme International) for the foundation floor`}
      foundationFloorInsulationEffectiveRsi
      # ${i18n.t`Filter for dwellings with a specific insulation effective R-value for the foundation floor`}
      foundationFloorInsulationEffectiveR
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific area in square metres (m2)`}
      foundationFloorAreaMetres
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific area in square feet (ft2)`}
      foundationFloorAreaFeet
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific perimeter in metres (m)`}
      foundationFloorPerimeterMetres
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific perimeter in feet (ft)`}
      foundationFloorPerimeterFeet
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific width in metres (m)`}
      foundationFloorWidthMetres
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific width in feet (ft)`}
      foundationFloorWidthFeet
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific length in metres (m)`}
      foundationFloorLengthMetres
      # ${i18n.t`Filter for dwellings where the foundation floor has a specific length in feet (ft)`}
      foundationFloorLengthFeet
      # ${i18n.t`Filter results for dwellings whose foundation wall has a specific type (en)`}
      foundationWallWallTypeEnglish
      # ${i18n.t`Filter results for dwellings whose foundation wall has a specific type (fr)`}
      foundationWallWallTypeFrench
      # ${i18n.t`Filter results for dwellings with a specific foundation wall insulation nominal RSI (R-value Systeme International)`}
      foundationWallInsulationNominalRsi
      # ${i18n.t`Filter results for dwellings with a specific foundation wall insulation nominal R-value`}
      foundationWallInsulationNominalR
      # ${i18n.t`Filter results for dwellings with a specific foundation wall insulation effective RSI (R-value Systeme International)`}
      foundationWallInsulationEffectiveRsi
      # ${i18n.t`Filter results for dwellings with a specific foundation wall insulation effective R-value`}
      foundationWallInsulationEffectiveR
      # ${i18n.t`Filter results for dwellings with a section of its foundation wall with a specific percentage of the overall amount`}
      foundationWallPercentage
      # ${i18n.t`Filter results for dwellings with a specific foundation wall area in square metres (m2)`}
      foundationWallAreaMetres
      # ${i18n.t`Filter results for dwellings with a specific foundation wall area in square feet (ft2)`}
      foundationWallAreaFeet
    }
  `,

    createFoundation(i18n),
    createFoundationFloor(i18n),
    createFoundationWall(i18n),
    createHeader(i18n),
  ]

  return makeExecutableSchema({ typeDefs, resolvers: new Resolvers(i18n) })
}

export default Schema

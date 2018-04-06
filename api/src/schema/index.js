import { Resolvers } from './resolvers'
import { makeExecutableSchema } from 'graphql-tools'

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

    # ${i18n.t`Walls separate the interior heated space from the outside (interior partition walls are not considered walls)`}
    type Wall @cacheControl(maxAge: 90) {
      # ${i18n.t`Wall measurements calculated for this evaluation`}
      measurement: WallMeasurement
      # ${i18n.t`Proposed upgrade wall measurements calculated for this evaluation`}
      upgrade: WallMeasurement
    }

    # ${i18n.t`Wall measurements calculated for this evaluation`}
    type WallMeasurement @cacheControl(maxAge: 90) {
      # ${i18n.t`Description of wall insulation`}
      insulation: [Insulation]
      # ${i18n.t`Heat loss through walls in MJ`}
      heatLost: Float
    }

    # ${i18n.t`Material used to insulate something`}
    type Insulation @cacheControl(maxAge: 90) {
      # ${i18n.t`The proportion of total element that insulation makes up`}
      percentage: Float
      # ${i18n.t`The insulation rValue of the element`}
      rValue: Float
    }

    # ${i18n.t`Detailed information about specific features of a given dwelling`}
    type Evaluation @cacheControl(maxAge: 90) {
      # ${i18n.t`Evaluation type codes are used to define the type of evaluation performed and to distinguish the house type (i.e. newly built or existing)`}
      evaluationType: String
      # ${i18n.t`Date the evaluation was made`}
      entryDate: String
      # ${i18n.t`Compound field with service organization, advisor and file sequence`}
      fileId: String
      # ${i18n.t`Type of house`}
      houseType: String
      # ${i18n.t`Date the record was first created`}
      creationDate: String
      # ${i18n.t`Date the record was last modified`}
      modificationDate: String
      # ${i18n.t`A list of upgrades that would improve energy efficiency`}
      energyUpgrades: [Upgrade]
      # ${i18n.t`Heated floor area in m2`}
      heatedFloorArea: Float
      # ${i18n.t`The EnerGuide Rating calculated for this evaluation, in GJ`}
      ersRating: Rating
      # ${i18n.t`[Deprecated] The EnerGuide Rating calculated for this evaluation`}
      eghRating: Rating
      # ${i18n.t`Rated greenhouse gas emissions in tonnes/year`}
      greenhouseGasEmissions: Rating
      # ${i18n.t`Calculated as Heated Floor Area/ERS Rating, units of GJ/m2`}
      energyIntensity: Rating
      # ${i18n.t`Wall data entry for a dwelling`}
      walls: Wall
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

    # ${i18n.t`A rating value for a given field`}
    type Rating @cacheControl(maxAge: 90) {
      # ${i18n.t`Value of rating calculated for this evaluation`}
      measurement: Float
      # ${i18n.t`Proposed upgrade value of rating calculated for this evaluation`}
      upgrade: Float
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
      # ${i18n.t`Filter results by the dwellings of a specific type`}
      evaluationHouseType
      # ${i18n.t`Filter results by the dwellings containing at least one evaluation with a specific ERS rating`}
      evaluationErsRating
    }
  `,
  ]

  return makeExecutableSchema({ typeDefs, resolvers: new Resolvers(i18n) })
}

export default Schema

import { Resolvers } from './resolvers'
import { makeExecutableSchema } from 'graphql-tools'

import { createFoundation } from './types/Foundation'
import { createFoundationFloor } from './types/FoundationFloor'
import { createFoundationWall } from './types/FoundationWall'
import { createHeader } from './types/Header'

const Schema = i18n => {
  const typeDefs = [
    `
    scalar I18NInt
    scalar I18NFloat
    scalar I18NString
    scalar I18NBoolean
    scalar I18NDate

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
      value: I18NString!
    }

    # ${i18n.t`Filter by dwellings containing evaluations that were entered, created, or modified between a range of dates`}
    input DateRange {
      # ${i18n.t`Name of the date field results will be filtered by`}
      field: DateField!
      # ${i18n.t`Evaluation dates must be equal to or later than this value`}
      startDate: I18NDate
      # ${i18n.t`Evaluation dates must be equal to or earlier than this value`}
      endDate: I18NDate
    }

    # ${i18n.t`An improvement that could increase the energy efficiency of the dwelling`}
    type Upgrade @cacheControl(maxAge: 90) {
      # ${i18n.t`Part of the dwelling to be upgraded`}
      upgradeType: I18NString
      # ${i18n.t`Estimated cost of upgrade`}
      cost: I18NInt
      # ${i18n.t`Order of importance of upgrade recommendation (lower number means a higher priority)`}
      priority: I18NInt
    }

    # ${i18n.t`Ventilation systems draw exterior air into the house, exhaust interior air to the exterior, or both`}
    type Ventilation @cacheControl(maxAge: 90) {
      # ${i18n.t`Ventilation type installed (en)`}
      typeEnglish: I18NString
      # ${i18n.t`Ventilation type installed (fr)`}
      typeFrench: I18NString
      # ${i18n.t`Air flow rate in litres per second (L/s)`}
      airFlowRateLps: I18NFloat
      # ${i18n.t`Air flow rate in cubic feet per minute (f3/m)`}
      airFlowRateCfm: I18NFloat
    }

    # ${i18n.t`Floors represents the usable area of the house`}
    type Floor @cacheControl(maxAge: 90) {
      # ${i18n.t`Description of floor location`}
      label: I18NString
      # ${i18n.t`Floor insulation nominal RSI (R-value Systeme International)`}
      insulationNominalRsi: I18NFloat
      # ${i18n.t`Floor insulation nominal R-value`}
      insulationNominalR: I18NFloat
      # ${i18n.t`Floor insulation effective RSI (R-value Systeme International)`}
      insulationEffectiveRsi: I18NFloat
      # ${i18n.t`Floor insulation effective R-value`}
      insulationEffectiveR: I18NFloat
      # ${i18n.t`Floor area of the house in square metres (m2)`}
      areaMetres: I18NFloat
      # ${i18n.t`Floor area of the house in square feet (ft2)`}
      areaFeet: I18NFloat
      # ${i18n.t`Floor length of the house in metres (m)`}
      lengthMetres: I18NFloat
      # ${i18n.t`Floor area of the house in square feet (ft2)`}
      lengthFeet: I18NFloat
    }

    # ${i18n.t`Water heaters heat the domestic water in a house`}
    type WaterHeater @cacheControl(maxAge: 90) {
      # ${i18n.t`Type of tank being used to heat the domestic water in the house (en)`}
      typeEnglish: I18NString
      # ${i18n.t`Type of tank being used to heat the domestic water in the house (fr)`}
      typeFrench: I18NString
      # ${i18n.t`Capacity of the tank in litres (L)`}
      tankVolumeLitres: I18NFloat
      # ${i18n.t`Capacity of the tank in gallons (Gal)`}
      tankVolumeGallon: I18NFloat
      # ${i18n.t`Measures how effectively your water heater is burning fuel or turning fuel into heat`}
      efficiencyEf: I18NString
      # ${i18n.t`A percentage representing the ratio of how effectively your water heater is turning fuel into heat`}
      efficiencyPercentage: I18NString
    }

    # ${i18n.t`A principal heating system is either the only source of heat for the house, or is used for at least 70% of the heating load`}
    type Heating @cacheControl(maxAge: 90) {
      # ${i18n.t`Description of heating system`}
      label: I18NString
      # ${i18n.t`Type of heating system (en)`}
      heatingTypeEnglish: I18NString
      # ${i18n.t`Type of heating system (fr)`}
      heatingTypeFrench: I18NString
      # ${i18n.t`The source of fuel for the heating system (en)`}
      energySourceEnglish: I18NString
      # ${i18n.t`The source of fuel for the heating system (fr)`}
      energySourceFrench: I18NString
      # ${i18n.t`Equipment type of heating system (en)`}
      equipmentTypeEnglish: I18NString
      # ${i18n.t`Equipment type of heating system (fr)`}
      equipmentTypeFrench: I18NString
      # ${i18n.t`Output capacity of the heating system in kilowatt hours (kWh)`}
      outputSizeKW: I18NFloat
      # ${i18n.t`Output capacity of the heating system in British Thermal Units per hour (BTU/h)`}
      outputSizeBtu: I18NFloat
      # ${i18n.t`Measures how effectively your heating system is burning fuel or turning fuel into heat`}
      efficiency: I18NFloat
      # ${i18n.t`Steady-state efficiency is the combustion efficiency of the equipment at peak performance.
        The Annual Fuel Utilization Efficiency (AFUE) is a measure of efficiency based on average usage, accounting for the fact that most heating systems rarely run long enough to reach peak performance.`}
      steadyState: I18NString
    }

    # ${i18n.t`One page of results`}
    type PaginatedResultSet @cacheControl(maxAge: 90) {
      # ${i18n.t`If true, a further page of results can be returned`}
      hasNext: I18NBoolean
      # ${i18n.t`If true, a previous page of results can be returned`}
      hasPrevious: I18NBoolean
      # ${i18n.t`Identifier used to return the next page of results`}
      next: I18NString
      # ${i18n.t`Identifier cursor used to return the previous page of results`}
      previous: I18NString
      # ${i18n.t`A list of dwellings`}
      results: [Dwelling]
    }

    # ${i18n.t`Heated floor areas represents the usable areas of a house that is conditioned to a specified temperature during the whole heating season`}
    type HeatedFloorArea @cacheControl(maxAge: 90) {
      # ${i18n.t`Above-grade heated area of the house in square metres (m2), i.e. the ground floor`}
      areaAboveGradeMetres: I18NFloat
      # ${i18n.t`Above-grade heated area of the house in square feet (ft2), i.e. the ground floor`}
      areaAboveGradeFeet: I18NFloat
      # ${i18n.t`Below-grade heated area of the house in square metres (m2), i.e. the basement`}
      areaBelowGradeMetres: I18NFloat
      # ${i18n.t`Below-grade heated area of the house in square feet (ft2), i.e. the basement`}
      areaBelowGradeFeet: I18NFloat
    }

    # ${i18n.t`Walls separate the interior heated space from the outside (interior partition walls are not considered walls)`}
    type Wall @cacheControl(maxAge: 90) {
      # ${i18n.t`Description of wall location`}
      label: I18NString
      # ${i18n.t`Wall construction being used (en)`}
      structureTypeEnglish: I18NString
      # ${i18n.t`Wall construction being used (fr)`}
      structureTypeFrench: I18NString
      # ${i18n.t`Size of the component type (en)`}
      componentTypeSizeEnglish: I18NString
      # ${i18n.t`Size of the component type (fr)`}
      componentTypeSizeFrench: I18NString
      # ${i18n.t`Wall insulation nominal RSI (R-value Systeme International)`}
      insulationNominalRsi: I18NFloat
      # ${i18n.t`Wall insulation nominal R-value`}
      insulationNominalR: I18NFloat
      # ${i18n.t`Wall insulation effective RSI (R-value Systeme International)`}
      insulationEffectiveRsi: I18NFloat
      # ${i18n.t`Wall insulation nominal R-value`}
      insulationEffectiveR: I18NFloat
      # ${i18n.t`Wall area of the house in square metres (m2)`}
      areaMetres: I18NFloat
      # ${i18n.t`Wall area of the house in square feet (ft2)`}
      areaFeet: I18NFloat
      # ${i18n.t`Wall perimeter of the house in metres (m)`}
      perimeterMetres: I18NFloat
      # ${i18n.t`Wall perimeter of the house in feet (ft)`}
      perimeterFeet: I18NFloat
      # ${i18n.t`Wall height of the house in metres (m)`}
      heightMetres: I18NFloat
      # ${i18n.t`Wall height of the house in feet (ft)`}
      heightFeet: I18NFloat
    }

    # ${i18n.t`Doors are on outside walls, separating the interior heated space from the outside`}
    type Door @cacheControl(maxAge: 90) {
      # ${i18n.t`Describes the construction of the door (en)`}
      typeEnglish: I18NString
      # ${i18n.t`Describes the construction of the door (fr)`}
      typeFrench: I18NString
      # ${i18n.t`Door RSI (R-value Systeme International)`}
      insulationRsi: I18NFloat
      # ${i18n.t`Door R-value`}
      insulationR: I18NFloat
      # ${i18n.t`Door U-factor in metric: watts per square metre per degree Celcius (W/m2C)`}
      uFactor: I18NFloat
      # ${i18n.t`Door U-factor in imperial: British Thermal Units per square feet per degree Fahrenheit (BTU/ft2F)`}
      uFactorImperial: I18NFloat
      # ${i18n.t`Door area in square metres (m2)`}
      areaMetres: I18NFloat
      # ${i18n.t`Door area in square feet (ft2)`}
      areaFeet: I18NFloat
    }

    # ${i18n.t`Windows separate the interior heated space from the outside`}
    type Window @cacheControl(maxAge: 90) {
      # ${i18n.t`Used to identify the window component in the house`}
      label: I18NString
      # ${i18n.t`Window RSI (R-value Systeme International)`}
      insulationRsi: I18NFloat
      # ${i18n.t`Window R-value`}
      insulationR: I18NFloat
      # ${i18n.t`Number of panes of transparent material in a window (en)`}
      glazingTypesEnglish: I18NString
      # ${i18n.t`Number of panes of transparent material in a window (fr)`}
      glazingTypesFrench: I18NString
      # ${i18n.t`Type of coating and tint on a window pane (en)`}
      coatingsTintsEnglish: I18NString
      # ${i18n.t`Type of coating and tint on a window pane (fr)`}
      coatingsTintsFrench: I18NString
      # ${i18n.t`Type of gas injected between the glass layers (en)`}
      fillTypeEnglish: I18NString
      # ${i18n.t`Type of gas injected between the glass layers (fr)`}
      fillTypeFrench: I18NString
      # ${i18n.t`Spacer systems used between the glass layers (en)`}
      spacerTypeEnglish: I18NString
      # ${i18n.t`Spacer systems used between the glass layers (fr)`}
      spacerTypeFrench: I18NString
      # ${i18n.t`Describes the construction of the window (en)`}
      typeEnglish: I18NString
      # ${i18n.t`Describes the construction of the window (fr)`}
      typeFrench: I18NString
      # ${i18n.t`Material type of the window frame (en)`}
      frameMaterialEnglish: I18NString
      # ${i18n.t`Material type of the window frame (fr)`}
      frameMaterialFrench: I18NString
      # ${i18n.t`Window area in square metres (m2)`}
      areaMetres: I18NFloat
      # ${i18n.t`Window area in square feet (ft2)`}
      areaFeet: I18NFloat
      # ${i18n.t`Window width in metres (m)`}
      widthMetres: I18NFloat
      # ${i18n.t`Window width in feet (ft)`}
      widthFeet: I18NFloat
      # ${i18n.t`Window height in metres (m)`}
      heightMetres: I18NFloat
      # ${i18n.t`Window height in feet (ft)`}
      heightFeet: I18NFloat
    }

    # ${i18n.t`Ceilings are the upper interior surface of a room`}
    type Ceiling @cacheControl(maxAge: 90) {
      # ${i18n.t`Used to identify the ceiling in the house`}
      label: I18NString
      # ${i18n.t`Describes the construction of the ceiling (en)`}
      typeEnglish: I18NString
      # ${i18n.t`Describes the construction of the ceiling (fr)`}
      typeFrench: I18NString
      # ${i18n.t`Ceiling insulation nominal RSI (R-value Systeme International)`}
      insulationNominalRsi: I18NFloat
      # ${i18n.t`Ceiling insulation nominal R-value`}
      insulationNominalR: I18NFloat
      # ${i18n.t`Ceiling insulation effective RSI (R-value Systeme International)`}
      insulationEffectiveRsi: I18NFloat
      # ${i18n.t`Ceiling insulation effective R-value`}
      insulationEffectiveR: I18NFloat
      # ${i18n.t`Ceiling area in square metres (m2)`}
      areaMetres: I18NFloat
      # ${i18n.t`Ceiling area in square feet (ft2)`}
      areaFeet: I18NFloat
      # ${i18n.t`Ceiling length in metres (m)`}
      lengthMetres: I18NFloat
      # ${i18n.t`Ceiling length in feet (ft)`}
      lengthFeet: I18NFloat
    }

    # ${i18n.t`Detailed information about specific features of a given dwelling`}
    type Evaluation @cacheControl(maxAge: 90) {
      # ${i18n.t`Evaluation type codes are used to define the type of evaluation performed and to distinguish the house type (i.e. newly built or existing)`}
      evaluationType: I18NString
      # ${i18n.t`Date the evaluation was made`}
      entryDate: I18NString
      fileId: I18NString
      # ${i18n.t`Date the record was first created`}
      creationDate: I18NString
      # ${i18n.t`Date the record was last modified`}
      modificationDate: I18NString
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
      # ${i18n.t`A principal heating system for a dwelling`}
      heating: Heating
      # ${i18n.t`A list of upgrades that would improve energy efficiency`}
      energyUpgrades: [Upgrade]
      # ${i18n.t`The details of the foundation`}
      foundations: [Foundation]
      # ${i18n.t`The EnerGuide Rating calculated for this evaluation`}
      ersRating: I18NString
    }

    # ${i18n.t`A residential building evaluted under the Energuide program`}
    type Dwelling @cacheControl(maxAge: 90) {
      # ${i18n.t`Unique identification number for a dwelling`}
      houseId: I18NInt
      # ${i18n.t`Year of construction`}
      yearBuilt: I18NInt
      # ${i18n.t`Name of city where dwelling is located`}
      city: I18NString
      # ${i18n.t`Region of country for dwelling (province/territory)`}
      region: I18NString
      # ${i18n.t`The first three characters of a Canadian postal code, which correspond to a geographical area defined by Canada Post`}
      forwardSortationArea: I18NString
      # ${i18n.t`A list of evaluations of specific features of the dwelling`}
      evaluations: [Evaluation]
    }

    # ${i18n.t`The root query type`}
    type Query @cacheControl(maxAge: 90) {
      # ${i18n.t`Details for a specific dwelling`}
      dwelling(houseId: I18NInt!): Dwelling
      # ${i18n.t`Details for all dwellings, optionally filtered by one or more values`}
      dwellings(filters: [Filter!] dateRange: DateRange limit: I18NInt next: I18NString previous: I18NString): PaginatedResultSet
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
      # ${i18n.t`Filter results by the dwellings containing at least one ventilation system with a specific type (en)`}
      ventilationTypeEnglish
      # ${i18n.t`Filter results by the dwellings containing at least one ventilation system with a specific type (fr)`}
      ventilationTypeFrench
      # ${i18n.t`Filter results by the dwellings containing at least one ventilation system with a specific air flow rate in litres per second (L/s)`}
      ventilationAirFlowRateLps
      # ${i18n.t`Filter results by the dwellings containing at least one ventilation system with a specific air flow rate in cubic feet per minute (f3/m)`}
      ventilationAirFlowRateCfm
      # ${i18n.t`Filter results by the dwellings containing at least one ventilation system with a specific efficiency rating`}
      ventilationEfficiency
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific location`}
      floorLabel
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific nominal RSI (R-value Systeme International)`}
      floorInsulationNominalRsi
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific nominal R-value`}
      floorInsulationNominalR
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific effective R-value`}
      floorInsulationEffectiveRsi
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific effective R-value`}
      floorInsulationEffectiveR
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific area in square metres (m2)`}
      floorAreaMetres
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific area in square feet (ft2)`}
      floorAreaFeet
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific length in metres (m)`}
      floorLengthMetres
      # ${i18n.t`Filter results by the dwellings containing at least one floor with a specific length in feet (ft)`}
      floorLengthFeet
      # ${i18n.t`Filter results by the dwellings containing at least one water heating system of a specific type (en)`}
      waterHeatingTypeEnglish
      # ${i18n.t`Filter results by the dwellings containing at least one water heating system of a specific type (fr)`}
      waterHeatingTypeFrench
      # ${i18n.t`Filter results by the dwellings containing at least one water heating system with a specific capacity in litres (L)`}
      waterHeatingTankVolumeLitres
      # ${i18n.t`Filter results by the dwellings containing at least one water heating system with a specific capacity in gallons (Gal)`}
      waterHeatingTankVolumeGallon
      # ${i18n.t`Filter results by the dwellings containing at least one water heating system with a specific efficiency percentage`}
      waterHeatingEfficiencyPercentage
      # ${i18n.t`Filter results by the dwellings containing at least one water heating system with a specific efficiency rating`}
      waterHeatingEfficiencyEf
      # ${i18n.t`Filter results by the dwellings containing a heating system with a specific description`}
      heatingLabel
      # ${i18n.t`Filter results by the dwellings containing a heating system of a specific type (en)`}
      heatingHeatingTypeEnglish
      # ${i18n.t`Filter results by the dwellings containing a heating system of a specific type (fr)`}
      heatingHeatingTypeFrench
      # ${i18n.t`Filter results by the dwellings containing a heating system with a specific fuel source (en)`}
      heatingEnergySourceEnglish
      # ${i18n.t`Filter results by the dwellings containing a heating system with a specific fuel source (fr)`}
      heatingEnergySourceFrench
      # ${i18n.t`Filter results by the dwellings containing a heating system with a specific type of equipment (en)`}
      heatingEquipmentTypeEnglish
      # ${i18n.t`Filter results by the dwellings containing a heating system with a specific type of equipment (fr)`}
      heatingEquipmentTypeFrench
      # ${i18n.t`Filter results by the dwellings containing a heating system with a specific output capacity in kilowatt hours (kWh)`}
      heatingOutputSizeKW
      # ${i18n.t`Filter results by the dwellings containing a heating system with a specific output capacity in British Thermal Units per hour (BTU/h)`}
      heatingOutputSizeBtu
      # ${i18n.t`Filter results by the dwellings containing a heating system with a specific efficiency rating`}
      heatingEfficiency
      # ${i18n.t`Filter results by the dwellings containing a heating system efficiency measurement that is either 'Steady State' or 'AFUE'`}
      heatingSteadyState
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
      # ${i18n.t`Filter results by the dwellings containing at least one door with a specific type (en)`}
      doorTypeEnglish
      # ${i18n.t`Filter results by the dwellings containing at least one door with a specific type (fr)`}
      doorTypeFrench
      # ${i18n.t`Filter results by the dwellings where at least one door has a specific RSI (R-value Systeme International) value`}
      doorInsulationRsi
      # ${i18n.t`Filter results by the dwellings containing at least one door with a specific effective R-value`}
      doorInsulationR
      # ${i18n.t`Filter results for dwellings which have at least one door with a matching U-factor in metric: watts per square metre per degree Celcius (W/m2C)`}
      doorUFactor
      # ${i18n.t`Filter results for dwellings which have at least one door with a matching U-factor in imperial: British Thermal Units per square feet per degree Fahrenheit (BTU/ft2F)`}
      doorUFactorImperial
      # ${i18n.t`Filter results by dwellings where the area of the doors have certain value in square metres (m2)`}
      doorAreaMetres
      # ${i18n.t`Filter results by dwellings where the area of the doors have certain value in square feet (ft2)`}
      doorAreaFeet
      # ${i18n.t`Filter results by dwellings have window with a matching label`}
      windowLabel
      # ${i18n.t`Filter results by dwellings with a specific window RSI (R-value Systeme International)`}
      windowInsulationRsi
      # ${i18n.t`Filter results by dwellings with a specific window R-value`}
      windowInsulationR
      # ${i18n.t`Filter results by dwellings with a matching number of panes of transparent material in a window (en)`}
      windowGlazingTypesEnglish
      # ${i18n.t`Filter results by dwellings with a matching number of panes of transparent material in a window (fr)`}
      windowGlazingTypesFrench
      # ${i18n.t`Filter results for dwellings with a specific type of coating and tint on a window pane (en)`}
      windowCoatingsTintsEnglish
      # ${i18n.t`Filter results for dwellings with a specific type of coating and tint on a window pane (fr)`}
      windowCoatingsTintsFrench
      # ${i18n.t`Filter results for dwellings with windows containing a specific type of gas injected between the glass layers (en)`}
      windowFillTypeEnglish
      # ${i18n.t`Filter results for dwellings with windows containing a specific type of gas injected between the glass layers (fr)`}
      windowFillTypeFrench
      # ${i18n.t`Filter results for dwellings with a specific spacer system used between the glass layers (en)`}
      windowSpacerTypeEnglish
      # ${i18n.t`Filter results for dwellings with a specific spacer system used between the glass layers (fr)`}
      windowSpacerTypeFrench
      # ${i18n.t`Filter results for dwellings with a particular type of window construction (en)`}
      windowTypeEnglish
      # ${i18n.t`Filter results for dwellings with a particular type of window construction (fr)`}
      windowTypeFrench
      # ${i18n.t`Filter results for dwellings with window frames matching a specific material (en)`}
      windowFrameMaterialEnglish
      # ${i18n.t`Filter results for dwellings with window frames matching a specific material (fr)`}
      windowFrameMaterialFrench
      # ${i18n.t`Filter results for dwellings with a window matching a specific area in square metres (m2)`}
      windowAreaMetres
      # ${i18n.t`Filter results for dwellings with a window matching a specific area in square feet (ft2)`}
      windowAreaFeet
      # ${i18n.t`Filter results for dwellings with a window matching a specific width in metres (m)`}
      windowWidthMetres
      # ${i18n.t`Filter results for dwellings with a window matching a specific width in feet (ft)`}
      windowWidthFeet
      # ${i18n.t`Filter results for dwellings with a window matching a specific height in metres (m)`}
      windowHeightMetres
      # ${i18n.t`Filter results for dwellings with a window matching a specific height in feet (ft)`}
      windowHeightFeet
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
      # ${i18n.t`Filter results for dwellings wiht a specific foundation header insulation nominal RSI (R-value Systeme International)`}
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
      # ${i18n.t`Filter results for dwellings with a foundation wall has specific area in square metres (m2)`}
      foundationWallAreaMetres
      # ${i18n.t`Filter results for dwellings with a foundation wall has specific area in square feet (ft)`}
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

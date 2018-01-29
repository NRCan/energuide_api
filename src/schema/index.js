import resolvers from './resolvers'
import { makeExecutableSchema } from 'graphql-tools'

const Schema = i18n => {
  const typeDefs = `
    scalar Longitude
    scalar Latitude
    scalar PostalCode

    input GeoPoint {
      lat: Latitude!
      lng: Longitude!
    }

    input Filter {
      field: Field!
      gt: String
      lt: String
      eq: String
    }

    type Query {
      evaluationsFor(account: Int! postalCode: PostalCode!): Evaluation
      evaluations(filter: Filter withinPolygon: [GeoPoint]!): [Evaluation]
    }
    
    # ${i18n.t`This is a description of evaluations`}
    type Evaluation {
      yearBuilt: String
      # ${i18n.t`Square footage of home`}
      evalId: String
      idNumber: String
      partner: String
      evaluator: String
      previousFileId: String
      status: String
      creationDate: String
      modificationDate: String
      builder: String
      houseRegion: String
      weatherLocation: String
      entryBy: String
      clientCity: String
      clientAddress: String
      clientPostalCode: String
      clientName: String
      telephoneNumber: String
      mailingAddress: String
      mailingAddressCity: String
      mailingAddressRegion: String
      mailingAddressPostalCode: String
      taxNumber: String
      info1: String
      info2: String
      info3: String
      info4: String
      info5: String
      info6: String
      info7: String
      info8: String
      info9: String
      info10: String
      floorArea: String
      # ${i18n.t`Footprint`}
      footPrint: String
      # ${i18n.t`Type of furnace in home`}
      furnaceType: String
      furnaceSteadyStateEfficiency: String
      # ${i18n.t`Primary heating equipment fuel type`}
      furnaceFuel: String
      # ${i18n.t`Heat pump source of supply`}
      heatPumpSupplySource: String
      # ${i18n.t`Heat pump co-efficient of performance`}
      heatPumpCoeffiecientOfPerformance: String
      # ${i18n.t`Primary domestic hot water equipment type`}
      hotWaterEquipmentType: String
      # ${i18n.t`Domestic hot water equipment efficiency`}
      hotWaterEquipmentEfficiency: String
      # ${i18n.t`Primary domestic hot water equipment fuel type`}
      hotWaterEquipmentFuelType: String
      # ${i18n.t`Domestic hot water heat pump system type`}
      hotWaterHeatPumpSystemType: String
      # ${i18n.t`Domestic hot water heat pump system co-efficient of performance`}
      hotWaterHeatPumpSystemCoefficienctOfPerformance: String
      # ${i18n.t`Canadian Solar Industry Association rating for solar DHW system (MJ/y)`}
      csiaRating: String
      # ${i18n.t`Type of house (detached, semi-detached, or row housing)`}
      typeOfHouse: String
      # ${i18n.t`Ceiling insulation RSI value`}
      ceilingInsulationRSIvalue: String
      # ${i18n.t`Foundation insulation RSI value`}
      foundationWallInsulationRSIvalue: String
      # ${i18n.t`Main walls insulation RSI value`}
      mainWallInsulationRSI: String
      # ${i18n.t`Number of floors above grade`}
      storeys: String
      # ${i18n.t`Total number of occupants`}
      totalOccupants: String
      # ${i18n.t`House shape`}
      planShape: String
      # ${i18n.t`Temperature of the basement in Celsius`}
      basementTemperature: String
      # ${i18n.t`Temperature of the main floor in Celsius`}
      mainFloorTemperature: String
      # ${i18n.t`House volume in m3`}
      houseVolume: String
      # ${i18n.t`Air leakage at 50 pascals`}
      airLeakageAt50Pascals: String
      # ${i18n.t`Equivalent leakage area at 10 pascals`}
      leakageAreaAt10Pascals: String
      # ${i18n.t`Ventilation type installed`}
      centralVentilationSystemType: String
      # ${i18n.t`Indicates which version of hot2000 was used: General Mode or Expert Version (EA version)`}
      registration: String
      # ${i18n.t`Name of program used (indicates which build of hot2000 was used….9.34c, 10.50, etc.)`}
      programName: String 
      # ${i18n.t`Consumption of electricity in kWh`}
      eghfElectricityConsumption: String
      # ${i18n.t`Consumption of gas in m3`}
      eghfGasConsumption: String
      # ${i18n.t`Consumption of oil in L`}
      eghfOilConsumption: String
      # ${i18n.t`Consumption of propane in L`}
      eghfPropaneConsumption: String
      # ${i18n.t`Total energy consumption in MJ`}
      eghfTotalEnergyConsumption: String
      # ${i18n.t`Estimated annual space heating energy consumption + ventilator electrical consumption (heating hour) heating energy in MJ`}
      eghEstimatedAnnualSpaceHeatingEnergyConsumption: String
      eghfcostelec: String
      eghfcostngas: String
      eghfcostoil: String
      eghfcostprop: String
      eghfcosttotal: String
      eghcritnatach: String
      eghcrittotach: String
      eghhlair: String
      eghhlfound: String
      eghhlceiling: String
      eghhlwalls: String
      eghhlwindoor: String
      eghrating: String
      ugrfurnacetyp: String
      ugrfurnaceeff: String
      ugrfurnacefuel: String
      ugrhptype: String
      ugrhpcop: String
      ugrdhwsystype: String
      ugrdhwsysef: String
      ugrdhwsysfuel: String
      ugrdhwhptype: String
      ugrdhwhpcop: String
      ugrdhwcsia: String
      ugrceilins: String
      ugrfndins: String
      ugrwallins: String
      ugrfconelec: String
      ugrfconngas: String
      ugrfconoil: String
      ugrfconprop: String
      ugrfcontotal: String
      ugrfcostelec: String
      ugrfcostngas: String
      ugrfcostoil: String
      ugrfcostprop: String
      ugrfcosttotal: String
      ugrair50pa: String
      ugrhlair: String
      ugrhlfound: String
      ugrhlceiling: String
      ugrhlwalls: String
      ugrhlwindoor: String
      ugrrating: String
      province: String
      decadebuilt: String
      location_id: String
      eghfurnaceaec: String
      ugrfurnaceaec: String
      eghdeshtloss: String
      ugrdeshtloss: String
      eghfurseaeff: String
      ugrfurseaeff: String
      uceventsystype: String
      ugrcritnatach: String
      eghhlexposedflr: String
      eghinexposedflr: String
      ugrinexposedflr: String
      ugrhlexposedflr: String
      ugrcrittotach: String
      ugrfurseaseff: String
      eghfurseaseff: String
      batch_number: String
      payable: String
      eghfconwood: String
      eghfcostwood: String
      ugrfconwood: String
      ugrfcostwood: String
      otc: String
      vermiculite: String
      ponywallexists: String
      basementfloorar: String
      walkoutfloorar: String
      crawlspfloorar: String
      slabfloorar: String
      blowerdoortest: String
      fireplacedamp1: String
      fireplacedamp2: String
      heatsyssizeop: String
      totalventsupply: String
      totalventexh: String
      ugrtotalventsup: String
      ugrtotalventexh: String
      credit_pv: String
      credit_wind: String
      ugrcredit_pv: String
      ugrcredit_wind: String
      credit_thermst: String
      credit_vent: String
      credit_garage: String
      credit_lighting: String
      credit_egh: String
      credit_oth1oth2: String
      windowcode: String
      ugrwindowcode: String
      hrveff0c: String
      unitsmurbs: String
      visitedunits: String
      baseloadsmurb: String
      murbhtsystemdis: String
      indfurnacetype: String
      indfursseff: String
      indfurnacefuel: String
      ugrindfurnacetp: String
      ugrindfursseff: String
      ugrindfurnacefu: String
      sharedata: String
      estar: String
      depressexhaust: String
      entrydate: String
      furnacemodel: String
      buildername: String
      ownership: String
      eghheatfconse: String
      eghheatfconsg: String
      eghheatfconso: String
      eghheatfconsp: String
      eghheatfconsw: String
      ugrheatfconse: String
      ugrheatfconsg: String
      ugrheatfconso: String
      ugrheatfconsp: String
      ugrheatfconsw: String
      furdcmotor: String
      ugrfurdcmotor: String
      hpestar: String
      ugrhpestar: String
      nelecthermos: String
      ugrnelecthermos: String
      epacsa: String
      ugrepacsa: String
      supphtgtype1: String
      supphtgtype2: String
      supphtgfuel1: String
      supphtgfuel2: String
      ugrsupphtgtype1: String
      ugrsupphtgtype2: String
      ugrsupphtgfuel1: String
      ugrsupphtgfuel2: String
      epacsasupphtg1: String
      epacsasupphtg2: String
      uepacsasupphtg1: String
      uepacsasupphtg2: String
      hviequip: String
      ugrhviequip: String
      aircondtype: String
      ugraircondtype: String
      aircop: String
      ugraircop: String
      accentestar: String
      ugraccentestar: String
      acwindestar: String
      ugracwindestar: String
      fndhdr: String
      ugrfndhdr: String
      numwindows: String
      numwinestar: String
      numdoors: String
      ugrnumwinestar: String
      numdoorestar: String
      ugrnumdoorestar: String
      acwindnum: String
      ugracwindnum: String
      heatafue: String
      ugrheatafue: String
      ceilingtype: String
      ugrceilingtype: String
      atticceilingdef: String
      uattceilingdef: String
      caflaceilingdef: String
      ucaflceilingdef: String
      fndtype: String
      ugrfndtype: String
      fnddef: String
      ugrfnddef: String
      walldef: String
      ugrwalldef: String
      eincentive: String
      lftoilets: String
      ulftoilets: String
      dwhrl1m: String
      udwhrl1m: String
      dwhrm1m: String
      udwhrm1m: String
      wthdata: String
      sdhwtype: String
      sdhwef: String
      sdhwfuel: String
      sdhwhptype: String
      sdhwhpcop: String
      ugrsdhwsystype: String
      ugrsdhwsysef: String
      ugrsdhwsysfuel: String
      ugrsdhwhptype: String
      ugrsdhwhpcop: String
      exposedfloor: String
      ugexposedfloor: String
      murbhsestar: String
      murbwoodepa: String
      murbashpestar: String
      murbdwhrl1m: String
      murbdwhrm1m: String
      murbhrvhvi: String
      murbdhwins: String
      murbdhwcond: String
      murbwoodheat: String
      type1capacity: String
      pdhwestar: String
      ugrpdhwestar: String
      sdhwestar: String
      ugrsdhwestar: String
      murbdhwinses: String
      umurbdhwinses: String
      murbdhwcondinses: String
      umurbdhwcondines: String
      hpcap: String
      acmodelnumber: String
      mixuse: String
      windowcodenum: String
      uwindowcodenum: String
      cid: String
      numsolsys: String
      totcsia: String
      largestcsia: String
      sndheatsys: String
      sndheatsysfuel: String
      sndheatsystype: String
      sndheatafue: String
      sndheatdcmotor: String
      sndheatmanufacturer: String
      sndheatmodel: String
      sndheatestar: String
      ugrsndheatsys: String
      ugrsndheatsysfuel: String
      ugrsndheatsystype: String
      ugrsndheatafue: String
      ugrsndheatdcmotor: String
      ugrsndheatmanufacturer: String
      ugrsndheatmodel: String
      ugrsndheatestar: String
      numwinzoned: String
      numdoorzoned: String
      ugrnumwinzoned: String
      ugrnumdoorzoned: String
      washermanufacturer: String
      washermodel: String
      washerestar: String
      ugrwashermanufacturer: String
      ugrwashermodel: String
      ugrwasherestar: String
      dryerfuel: String
      dryermanufacturer: String
      dryermodel: String
      ugrdryerfuel: String
      ugrdryermanufacturer: String
      ugrdryermodel: String
      estarlights: String
      ugrestarlights: String
      hviestar: String
      estarmurbhrvhvi: String
      ugrhviestar: String
      ugrmurbhrvhvi: String
      ugrestarmurbhrvhvi: String
      murbdhwstes: String
      ugrmurbdhwstes: String
      eval_type: String
      eid: String
      house_id: String
      justify: String
      # ${i18n.t`The actual EnerGuide rating for house`}
      energuideRating: String
      ugrersrating: String
      ersenergyintensity: String
      ugrersenergyintensity: String
      ersghg: String
      ugrersghg: String
      ersrenewableprod: String
      hocersrating: String
      hocugrersrating: String
      ersrefhouserating: String
      rulesetver: String
      rulesettype: String
      heatedfloorarea: String
      ersrenewableelec: String
      ersspacecoolenergy: String
      ersrenewablesolar: String
      erswaterheatingenergy: String
      ersventilationenergy: String
      erslightapplianceenergy: String
      ersotherelecenergy: String
      ugrersspacecoolenergy: String
      ugrerswaterheatingenergy: String
      ugrersventilationenergy: String
      ugrerslightapplianceenergy: String
      ugrersotherelecenergy: String
      erselecghg: String
      ersngasghg: String
      ersoilghg: String
      erspropghg: String
      erswoodghg: String
      ersrenewableelecghg: String
      ersrenewablesolarghg: String
      ershlwindow: String
      ershldoor: String
      ugrershlwindow: String
      ugrershldoor: String
      ugrspaceenergy: String
      qwarn: String
      qtot: String
      dataset: String
      eidef: String
      ugreidef: String
      buildingtype: String
      eghfconwoodgj: String
    }

    enum Field {
      yearBuilt
      evalId
      idNumber
      partner
      evaluator
      previousFileId
      status
      creationDate
      modificationDate
      builder
      houseRegion
      weatherLocation
      entryBy
      clientCity
      clientAddress
      clientPostalCode
      clientName
      telephoneNumber
      mailingAddress
      mailingAddressCity
      mailingAddressRegion
      mailingAddressPostalCode
      taxNumber
      info1
      info2
      info3
      info4
      info5
      info6
      info7
      info8
      info9
      info10
      floorArea
      footPrint
      furnaceType
      furnaceSteadyStateEfficiency
      furnaceFuel
      heatPumpSupplySource
      heatPumpCoeffiecientOfPerformance
      hotWaterEquipmentType
      hotWaterEquipmentEfficiency
      hotWaterEquipmentFuelType
      hotWaterHeatPumpSystemType
      hotWaterHeatPumpSystemCoefficienctOfPerformance
      csiaRating
      typeOfHouse
      ceilingInsulationRSIvalue
      foundationWallInsulationRSIvalue
      mainWallInsulationRSI
      storeys
      totalOccupants
      planShape
      basementTemperature
      mainFloorTemperature
      houseVolume
      airLeakageAt50Pascals
      leakageAreaAt10Pascals
      centralVentilationSystemType
      registration
      programName 
      eghfElectricityConsumption
      eghfGasConsumption
      eghfOilConsumption
      eghfPropaneConsumption
      eghfTotalEnergyConsumption
      eghEstimatedAnnualSpaceHeatingEnergyConsumption
      eghfcostelec
      eghfcostngas
      eghfcostoil
      eghfcostprop
      eghfcosttotal
      eghcritnatach
      eghcrittotach
      eghhlair
      eghhlfound
      eghhlceiling
      eghhlwalls
      eghhlwindoor
      eghrating
      ugrfurnacetyp
      ugrfurnaceeff
      ugrfurnacefuel
      ugrhptype
      ugrhpcop
      ugrdhwsystype
      ugrdhwsysef
      ugrdhwsysfuel
      ugrdhwhptype
      ugrdhwhpcop
      ugrdhwcsia
      ugrceilins
      ugrfndins
      ugrwallins
      ugrfconelec
      ugrfconngas
      ugrfconoil
      ugrfconprop
      ugrfcontotal
      ugrfcostelec
      ugrfcostngas
      ugrfcostoil
      ugrfcostprop
      ugrfcosttotal
      ugrair50pa
      ugrhlair
      ugrhlfound
      ugrhlceiling
      ugrhlwalls
      ugrhlwindoor
      ugrrating
      province
      decadebuilt
      location_id
      eghfurnaceaec
      ugrfurnaceaec
      eghdeshtloss
      ugrdeshtloss
      eghfurseaeff
      ugrfurseaeff
      uceventsystype
      ugrcritnatach
      eghhlexposedflr
      eghinexposedflr
      ugrinexposedflr
      ugrhlexposedflr
      ugrcrittotach
      ugrfurseaseff
      eghfurseaseff
      batch_number
      payable
      eghfconwood
      eghfcostwood
      ugrfconwood
      ugrfcostwood
      otc
      vermiculite
      ponywallexists
      basementfloorar
      walkoutfloorar
      crawlspfloorar
      slabfloorar
      blowerdoortest
      fireplacedamp1
      fireplacedamp2
      heatsyssizeop
      totalventsupply
      totalventexh
      ugrtotalventsup
      ugrtotalventexh
      credit_pv
      credit_wind
      ugrcredit_pv
      ugrcredit_wind
      credit_thermst
      credit_vent
      credit_garage
      credit_lighting
      credit_egh
      credit_oth1oth2
      windowcode
      ugrwindowcode
      hrveff0c
      unitsmurbs
      visitedunits
      baseloadsmurb
      murbhtsystemdis
      indfurnacetype
      indfursseff
      indfurnacefuel
      ugrindfurnacetp
      ugrindfursseff
      ugrindfurnacefu
      sharedata
      estar
      depressexhaust
      entrydate
      furnacemodel
      buildername
      ownership
      eghheatfconse
      eghheatfconsg
      eghheatfconso
      eghheatfconsp
      eghheatfconsw
      ugrheatfconse
      ugrheatfconsg
      ugrheatfconso
      ugrheatfconsp
      ugrheatfconsw
      furdcmotor
      ugrfurdcmotor
      hpestar
      ugrhpestar
      nelecthermos
      ugrnelecthermos
      epacsa
      ugrepacsa
      supphtgtype1
      supphtgtype2
      supphtgfuel1
      supphtgfuel2
      ugrsupphtgtype1
      ugrsupphtgtype2
      ugrsupphtgfuel1
      ugrsupphtgfuel2
      epacsasupphtg1
      epacsasupphtg2
      uepacsasupphtg1
      uepacsasupphtg2
      hviequip
      ugrhviequip
      aircondtype
      ugraircondtype
      aircop
      ugraircop
      accentestar
      ugraccentestar
      acwindestar
      ugracwindestar
      fndhdr
      ugrfndhdr
      numwindows
      numwinestar
      numdoors
      ugrnumwinestar
      numdoorestar
      ugrnumdoorestar
      acwindnum
      ugracwindnum
      heatafue
      ugrheatafue
      ceilingtype
      ugrceilingtype
      atticceilingdef
      uattceilingdef
      caflaceilingdef
      ucaflceilingdef
      fndtype
      ugrfndtype
      fnddef
      ugrfnddef
      walldef
      ugrwalldef
      eincentive
      lftoilets
      ulftoilets
      dwhrl1m
      udwhrl1m
      dwhrm1m
      udwhrm1m
      wthdata
      sdhwtype
      sdhwef
      sdhwfuel
      sdhwhptype
      sdhwhpcop
      ugrsdhwsystype
      ugrsdhwsysef
      ugrsdhwsysfuel
      ugrsdhwhptype
      ugrsdhwhpcop
      exposedfloor
      ugexposedfloor
      murbhsestar
      murbwoodepa
      murbashpestar
      murbdwhrl1m
      murbdwhrm1m
      murbhrvhvi
      murbdhwins
      murbdhwcond
      murbwoodheat
      type1capacity
      pdhwestar
      ugrpdhwestar
      sdhwestar
      ugrsdhwestar
      murbdhwinses
      umurbdhwinses
      murbdhwcondinses
      umurbdhwcondines
      hpcap
      acmodelnumber
      mixuse
      windowcodenum
      uwindowcodenum
      cid
      numsolsys
      totcsia
      largestcsia
      sndheatsys
      sndheatsysfuel
      sndheatsystype
      sndheatafue
      sndheatdcmotor
      sndheatmanufacturer
      sndheatmodel
      sndheatestar
      ugrsndheatsys
      ugrsndheatsysfuel
      ugrsndheatsystype
      ugrsndheatafue
      ugrsndheatdcmotor
      ugrsndheatmanufacturer
      ugrsndheatmodel
      ugrsndheatestar
      numwinzoned
      numdoorzoned
      ugrnumwinzoned
      ugrnumdoorzoned
      washermanufacturer
      washermodel
      washerestar
      ugrwashermanufacturer
      ugrwashermodel
      ugrwasherestar
      dryerfuel
      dryermanufacturer
      dryermodel
      ugrdryerfuel
      ugrdryermanufacturer
      ugrdryermodel
      estarlights
      ugrestarlights
      hviestar
      estarmurbhrvhvi
      ugrhviestar
      ugrmurbhrvhvi
      ugrestarmurbhrvhvi
      murbdhwstes
      ugrmurbdhwstes
      eval_type
      eid
      house_id
      justify
      energuideRating
      ugrersrating
      ersenergyintensity
      ugrersenergyintensity
      ersghg
      ugrersghg
      ersrenewableprod
      hocersrating
      hocugrersrating
      ersrefhouserating
      rulesetver
      rulesettype
      heatedfloorarea
      ersrenewableelec
      ersspacecoolenergy
      ersrenewablesolar
      erswaterheatingenergy
      ersventilationenergy
      erslightapplianceenergy
      ersotherelecenergy
      ugrersspacecoolenergy
      ugrerswaterheatingenergy
      ugrersventilationenergy
      ugrerslightapplianceenergy
      ugrersotherelecenergy
      erselecghg
      ersngasghg
      ersoilghg
      erspropghg
      erswoodghg
      ersrenewableelecghg
      ersrenewablesolarghg
      ershlwindow
      ershldoor
      ugrershlwindow
      ugrershldoor
      ugrspaceenergy
      qwarn
      qtot
      dataset
      eidef
      ugreidef
      buildingtype
      eghfconwoodgj
    }
  `

  return makeExecutableSchema({ typeDefs, resolvers })
}

export default Schema

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

    type Query {
      evaluationsFor(account: Int! postalCode: PostalCode!): Evaluation
      evaluations(withinPolygon: [GeoPoint]!): [Evaluation]
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
      mainwallins: String
      storeys: String
      totalOccupants: String
      planshape: String
      tbsmnt: String
      tmain: String
      hsevol: String
      # ${i18n.t`Air leakage at 50 pascals`}
      airLeakageAt50Pascals: String
      leakar: String
      cenventsystype: String
      registration: String
      programname: String
      eghfconelec: String
      eghfconngas: String
      eghfconoil: String
      eghfconprop: String
      eghfcontotal: String
      eghspaceenergy: String
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
  `

  return makeExecutableSchema({ typeDefs, resolvers })
}

export default Schema

export const createFoundationWall = i18n => {
  const FoundationWall = `
    # ${i18n.t`Foundation Walls are below-ground walls separating the interior heated space from the outside (interior partition walls are not considered walls)`}
    type FoundationWall @cacheControl(maxAge: 90) {
      # ${i18n.t`Wall construction being used (en)`}
      wallTypeEnglish: String
      # ${i18n.t`Wall construction being used (fr)`}
      wallTypeFrench: String
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
      # ${i18n.t`The percentage of the total wall area this section accounts for`}
      percentage: Float
    }
  `
  return FoundationWall
}

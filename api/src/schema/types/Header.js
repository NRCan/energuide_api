export const createHeader = i18n => {
  const Header = `
    type Header @cacheControl(maxAge: 90) {
      # ${i18n.t`Header insulation nominal RSI (R-value Systeme International)`}
      insulationNominalRsi: Float
      # ${i18n.t`Header insulation nominal R-value`}
      insulationNominalR: Float
      # ${i18n.t`Header insulation effective RSI (R-value Systeme International)`}
      insulationEffectiveRsi: Float
      # ${i18n.t`Header insulation effective R-value`}
      insulationEffectiveR: Float
      # ${i18n.t`Header area in square metres (m2)`}
      areaMetres: Float
      # ${i18n.t`Header area in square feet (ft2)`}
      areaFeet: Float
      # ${i18n.t`Header perimeter of the house in metres (m)`}
      perimeterMetres: Float
      # ${i18n.t`Header perimeter of the house in feet (ft)`}
      perimeterFeet: Float
      # ${i18n.t`Header height in metres (m)`}
      heightMetres: Float
      # ${i18n.t`Header height in feet (ft)`}
      heightFeet: Float
    }
  `
  return Header
}

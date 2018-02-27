export const createHeader = i18n => {
  const Header = `
    type Header {
      # ${i18n.t`Header insulation nominal RSI (R-value Systeme International)`}
      insulationNominalRsi: I18NFloat
      # ${i18n.t`Header insulation nominal R-value`}
      insulationNominalR: I18NFloat
      # ${i18n.t`Header insulation effective RSI (R-value Systeme International)`}
      insulationEffectiveRsi: I18NFloat
      # ${i18n.t`Header insulation effective R-value`}
      insulationEffectiveR: I18NFloat
      # ${i18n.t`Header area in square metres (m2)`}
      areaMetres: I18NFloat
      # ${i18n.t`Header area in square feet (ft2)`}
      areaFeet: I18NFloat
      # ${i18n.t`Header perimeter of the house in metres (m)`}
      perimeterMetres: I18NFloat
      # ${i18n.t`Header perimeter of the house in feet (ft)`}
      perimeterFeet: I18NFloat
      # ${i18n.t`Header height in metres (m)`}
      heightMetres: I18NFloat
      # ${i18n.t`Header height in feet (ft)`}
      heightFeet: I18NFloat
    }
  `
  return Header
}

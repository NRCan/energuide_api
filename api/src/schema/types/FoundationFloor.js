export const createFoundationFloor = i18n => {
  const FoundationFloor = `
    # ${i18n.t`A floor below ground that represents the usable area of the house`}
    type FoundationFloor @cacheControl(maxAge: 90) {
      # ${i18n.t`Type of foundation floor (en)`}
      floorTypeEnglish: I18NString
      # ${i18n.t`Type of foundation floor (fr)`}
      floorTypeFrench: I18NString
      # ${i18n.t`The insulation nominal RSI (R-value Systeme International) of the foundation floor`}
      insulationNominalRsi: I18NFloat
      # ${i18n.t`The insulation nominal R-value of the foundation floor`}
      insulationNominalR: I18NFloat
      # ${i18n.t`The insulation effective RSI (R-value Systeme International) of the foundation floor`}
      insulationEffectiveRsi: I18NFloat
      # ${i18n.t`The insulation effective R-value of the foundation floor`}
      insulationEffectiveR: I18NFloat
      # ${i18n.t`The area in square metres (m2) of the foundation floor`}
      areaMetres: I18NFloat
      # ${i18n.t`The area in square feet (ft2) of the foundation floor`}
      areaFeet: I18NFloat
      # ${i18n.t`The perimeter of the foundation floor in metres (m)`}
      perimeterMetres: I18NFloat
      # ${i18n.t`The perimeter of the foundation floor in feet (ft)`}
      perimeterFeet: I18NFloat
      # ${i18n.t`The width in metres (m) of the foundation floor`}
      heightMetres: I18NFloat
      # ${i18n.t`The width in feet (ft) of the foundation floor`}
      heightFeet: I18NFloat
      # ${i18n.t`The length in metres (m) of the foundation floor`}
      lengthMetres: I18NFloat
      # ${i18n.t`The length in feet (ft) of the foundation floor`}
      lengthFeet: I18NFloat
    }
  `
  return FoundationFloor
}

export const createFoundationFloor = i18n => {
  const FoundationFloor = `
    # ${i18n.t`A floor below ground that represents the usable area of the house`}
    type FoundationFloor @cacheControl(maxAge: 90) {
      # ${i18n.t`Type of foundation floor (en)`}
      floorTypeEnglish: String
      # ${i18n.t`Type of foundation floor (fr)`}
      floorTypeFrench: String
      # ${i18n.t`The insulation nominal RSI (R-value Systeme International) of the foundation floor`}
      insulationNominalRsi: Float
      # ${i18n.t`The insulation nominal R-value of the foundation floor`}
      insulationNominalR: Float
      # ${i18n.t`The insulation effective RSI (R-value Systeme International) of the foundation floor`}
      insulationEffectiveRsi: Float
      # ${i18n.t`The insulation effective R-value of the foundation floor`}
      insulationEffectiveR: Float
      # ${i18n.t`The area of the foundation floor in square metres (m2)`}
      areaMetres: Float
      # ${i18n.t`The area of the foundation floor in square feet (ft2)`}
      areaFeet: Float
      # ${i18n.t`The perimeter of the foundation floor in metres (m)`}
      perimeterMetres: Float
      # ${i18n.t`The perimeter of the foundation floor in feet (ft)`}
      perimeterFeet: Float
      # ${i18n.t`The width of the foundation floor in metres (m)`}
      heightMetres: Float
      # ${i18n.t`The width of the foundation floor in feet (ft)`}
      heightFeet: Float
      # ${i18n.t`The length of the foundation floor in metres (m)`}
      lengthMetres: Float
      # ${i18n.t`The length of the foundation floor in feet (ft)`}
      lengthFeet: Float
    }
  `
  return FoundationFloor
}

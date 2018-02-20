function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

export function generateName(type, attr) {
  let capitalized = capitalizeFirstLetter(attr)
  return `${type}${capitalized}`
}

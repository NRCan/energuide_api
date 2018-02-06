module.exports = {
  parser: "babel-eslint",
  extends: ["standard", "prettier", "plugin:import/recommended", "plugin:security/recommended"],
  plugins: ["jest", "security"],
  env: {
    "jest/globals": true,
  },
  rules: {
    "comma-dangle": ["error", "always-multiline"],
  },
}

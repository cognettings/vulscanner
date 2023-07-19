module.exports = {
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  parser: "@typescript-eslint/parser",
  parserOptions: {
    sourceType: "module",
    ecmaFeatures: {
      jsx: true,
    },
    project: "./tsconfig.json",
    tsconfigRootDir: __dirname,
  },
  plugins: [
    "@typescript-eslint",
    "fp",
    "import",
    "jsx-a11y",
    "prettier",
    "react",
    "react-hooks",
  ],
  extends: [
    "eslint:all",
    "plugin:@typescript-eslint/all",
    "plugin:fp/recommended",
    "plugin:import/recommended",
    "plugin:import/typescript",
    "plugin:jsx-a11y/strict",
    "plugin:prettier/recommended",
    "plugin:react/all",
    "plugin:storybook/recommended",
    "prettier",
  ],
  settings: {
    "import/parsers": {
      "@typescript-eslint/parser": [".ts", ".tsx"],
    },
    "import/resolver": {
      typescript: {},
    },
  },
  ignorePatterns: [".eslintrc.js"],
  rules: {
    "capitalized-comments": [
      "error",
      "always",
      { ignoreConsecutiveComments: true },
    ],
    eqeqeq: ["error", "smart"],
    "func-style": ["error", "declaration", { allowArrowFunctions: true }],
    /*
     * Given exceptions for lodash, jquery and translation wildcard "t"
     */
    "id-length": [
      "error",
      { exceptions: ["_", "$", "t"], properties: "never" },
    ],
    "line-comment-position": ["error", "above"],
    /*
     * "Max" retrictions are not suitable for the present codebase due to the
     * size of certain files and components
     */
    "max-lines": "off",
    "max-lines-per-function": "off",
    "max-params": "off",
    "max-statements": "off",
    "multiline-comment-style": ["error", "starred-block"],
    /*
     * Replaced by @typescript-eslint/no-duplicate-imports to avoid
     * conflicts with type imports
     * https://github.com/typescript-eslint/typescript-eslint/issues/2315
     */
    "no-duplicate-imports": "off",
    /*
     * Replaced by @typescript-eslint/no-magic-numbers
     */
    "no-magic-numbers": "off",
    /*
     * Rules regarding the ternary op are disabled, as it is common its usage in React
     */
    "no-nested-ternary": "off",
    "no-ternary": "off",
    /*
     * This rule is deactivated as the codebase uses extensivelly "undefined"
     * It was established by a previous TSLint rule:
     * https://palantir.github.io/tslint/rules/no-null-keyword/
     * For consistency, we will prefer "undefined" over "null"
     */
    "no-undefined": "off",
    /*
     * Exception to the next rule: The variable "__typename" is required by Apollo Library
     */
    "no-underscore-dangle": ["error", { allow: ["__typename"] }],
    "no-void": ["error", { allowAsStatement: true }],
    "one-var": ["error", "never"],
    "padding-line-between-statements": [
      "error",
      { blankLine: "always", prev: "*", next: "return" },
    ],
    "sort-imports": ["error", { ignoreDeclarationSort: true }],
    "prettier/prettier": [
      "error",
      {},
      {
        usePrettierrc: true,
      },
    ],
    "@typescript-eslint/ban-ts-comment": [
      "error",
      { "ts-expect-error": "allow-with-description" },
    ],
    /*
     * Useful when migrating from TSLint to ESLint
     */
    "@typescript-eslint/ban-tslint-comment": "error",
    "@typescript-eslint/explicit-function-return-type": [
      "error",
      {
        allowConciseArrowFunctionExpressionsStartingWithVoid: false,
        allowTypedFunctionExpressions: false,
        allowHigherOrderFunctions: false,
      },
    ],
    "@typescript-eslint/naming-convention": [
      "error",
      {
        selector: "variable",
        format: ["camelCase", "UPPER_CASE", "PascalCase"],
        leadingUnderscore: "allow",
      },
      {
        selector: "interface",
        format: ["PascalCase"],
        prefix: ["I"],
      },
    ],
    "@typescript-eslint/no-duplicate-imports": ["error"],
    /*
     * Disabling this rule is necessary to avoid a conflict with
     * @typescript-eslint/typedef that checks for all variables to be typed
     */
    "@typescript-eslint/no-inferrable-types": "off",
    /*
     * Disabled until the migration to newer versions of eslint is done
     */
    "@typescript-eslint/no-magic-numbers": [
      "off",
      {
        ignore: [-1, 0, 1, 2, 4],
        /*
         * We need type indexes to retrieve specific objects in interface lists
         */
        ignoreTypeIndexes: true,
      },
    ],
    /*
     * Disabled until the migration to newer versions of eslint is done
     */
    "@typescript-eslint/no-misused-promises": "off",
    /*
     * Using non-null assertions cancels the benefits of the strict null-checking mode
     */
    "@typescript-eslint/no-non-null-assertion": "error",
    /*
     * This rule is incompatible with "@typescript-eslint/no-non-null-assertion" and it
     * is not a problem to have verbose type casts
     */
    "@typescript-eslint/non-nullable-type-assertion-style": "off",
    /*
     * Disabled until the migration to newer versions of eslint is done
     */
    "@typescript-eslint/no-type-alias": [
      "off",
      {
        allowAliases: "always",
        allowGenerics: "always",
      },
    ],
    /*
     * Since we are working with external libraries that use any in there type
     * definitions. We need to disable the NEXT couple of rules, until they
     * update to the new unknown type
     */
    "@typescript-eslint/no-unsafe-argument": "off",
    "@typescript-eslint/no-unsafe-assignment": "off",
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
    /*
     * This rule must be disabled as it can report incorrect errors in conflict
     * with with rule eslint/object-curly-spacing. Official plugin doc
     */
    "@typescript-eslint/object-curly-spacing": "off",
    /*
     * We prefer interfaces over type aliases, the reason is no more than
     * consistency
     */
    "@typescript-eslint/prefer-function-type": "off",
    /*
     * This is a good rule in theory, but in practice we found:
     * 1. We tried to use a DeepReadonly utility type to solve types nesting
     * problems; but it conflicts with wrapper components, since you cannot
     * modify the types of the component being wrapped, if it is from a third
     * party library.
     * 2. We are using the fp eslint plugin that is already in charge of
     * avoiding side effects as much as posible
     */
    "@typescript-eslint/prefer-readonly-parameter-types": "off",
    "@typescript-eslint/sort-type-union-intersection-members": "error",
    /*
     * In the functional react world, you likely will never have a function that
     * actually cares about the this context. Refer to:
     * https://github.com/typescript-eslint/typescript-eslint/issues/2245#issuecomment-648712540
     */
    "@typescript-eslint/unbound-method": "off",
    "fp/no-mutation": [
      "error",
      {
        commonjs: true,
      },
    ],
    /*
     * Since we need side effects to make our program meaningful, for instace:
     * callbacks, DOM mutations, Node processes, etc. We need to disable the
     * next TWO rules, the result is: from now on it should be inferred that
     * any method call without an assignment, produce some kind of side effect
     */
    "fp/no-unused-expression": "off",
    "fp/no-nil": "off",
    "import/default": "error",
    "import/export": "error",
    "import/exports-last": "error",
    "import/first": "error",
    "import/group-exports": "error",
    "import/newline-after-import": "error",
    "import/no-absolute-path": ["error", { commonjs: false }],
    "import/no-cycle": ["error", { ignoreExternal: true }],
    "import/no-default-export": "error",
    "import/no-deprecated": "error",
    /*
     * This rule conflicts with the rule eslint/consistent-type-imports when
     * trying to import types and default modules in the same import
     * https://github.com/benmosher/eslint-plugin-import/pull/334
     */
    "import/no-duplicates": "off",
    "import/no-extraneous-dependencies": [
      "error",
      { optionalDependencies: false },
    ],
    "import/no-named-as-default": "error",
    "import/no-named-as-default-member": "error",
    "import/no-named-default": "error",
    "import/no-namespace": "error",
    "import/no-self-import": "error",
    "import/no-unresolved": "error",
    "import/no-useless-path-segments": ["error", { noUselessIndex: true }],
    "import/no-webpack-loader-syntax": "error",
    "import/order": [
      "error",
      {
        alphabetize: { order: "asc", caseInsensitive: true },
        groups: ["builtin", "external", "sibling"],
        "newlines-between": "always",
      },
    ],
    "jsx-a11y/label-has-for": "off",
    /*
     * This rule has been deprecated
     * because browsers fixed it.
     * https://github.com/jsx-eslint/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-onchange.md
     */
    "jsx-a11y/no-onchange": "off",
    /*
     * This rule requires the type attribute to be a string literal, because of
     * that it has a conflic with react/jsx-curly-brace-presence
     */
    "react/button-has-type": "off",
    "react/jsx-boolean-value": ["error", "always"],
    "react/jsx-curly-brace-presence": ["error", "always"],
    "react/jsx-filename-extension": [
      "error",
      {
        extensions: [".tsx"],
      },
    ],
    "react/jsx-fragments": ["error", "element"],
    "react/jsx-max-depth": "off",
    "react/jsx-no-bind": [
      "error",
      {
        allowFunctions: true,
      },
    ],
    /*
     * Turned off until an easy way to exclude context provider values in
     * tests is found
     */
    "react/jsx-no-constructed-context-values": "off",
    /*
     * "allowedStrings" is not working once the @typescript-eslint@4.15.2
     * plugin is updated. Affected string changed by its Unicode equivalent
     */
    "react/jsx-no-literals": ["error"],
    "react/function-component-definition": [
      "error",
      {
        namedComponents: "arrow-function",
      },
    ],
    "react-hooks/exhaustive-deps": "error",
    "react-hooks/rules-of-hooks": "error",
  },
};

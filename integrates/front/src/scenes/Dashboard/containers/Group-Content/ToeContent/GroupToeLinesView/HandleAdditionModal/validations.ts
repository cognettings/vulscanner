import _ from "lodash";
import type { TestContext, ValidationError } from "yup";
import { number, object, string } from "yup";

import { translate } from "utils/translations/translate";

const validations = object().shape({
  filename: string()
    .required(translate.t("validations.required"))
    .test({
      exclusive: false,
      name: "invalidTextBeginning",
      params: {},
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
          return false;
        }
        const beginTextMatch: RegExpMatchArray | null =
          /^=|^-|^\+|^@|^\t|^\r/u.exec(value);

        return _.isNull(beginTextMatch)
          ? true
          : thisContext.createError({
              message: translate.t("validations.invalidTextBeginning", {
                chars: `'${beginTextMatch[0]}'`,
              }),
            });
      },
    })
    .test({
      exclusive: false,
      name: "invalidTextPattern",
      params: {},
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
          return false;
        }
        const contentTextMatch: RegExpMatchArray | null =
          /["',;](?:[-=+@\t\r])/u.exec(value);

        return _.isNull(contentTextMatch)
          ? true
          : thisContext.createError({
              message: translate.t("validations.invalidTextPattern", {
                chars: `'${contentTextMatch[0]}'`,
              }),
            });
      },
    })
    .test({
      exclusive: false,
      name: "invalidTextField",
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
          return false;
        }
        const textMatch: RegExpMatchArray | null =
          /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s(){}[\],./:;@&_$%'#*=¿?¡!+-]/u.exec(
            value
          );

        return _.isNull(textMatch)
          ? true
          : thisContext.createError({
              message: translate.t("validations.invalidTextField", {
                chars: `'${textMatch[0]}'`,
              }),
            });
      },
    }),
  lastAuthor: string()
    .required(translate.t("validations.required"))
    .matches(
      /^[a-zA-Z0-9.!#$%&’*/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/u,
      translate.t("validations.email")
    )
    .test({
      exclusive: false,
      name: "invalidTextBeginning",
      params: {},
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
          return false;
        }
        const beginTextMatch: RegExpMatchArray | null =
          /^=|^-|^\+|^@|^\t|^\r/u.exec(value);

        return _.isNull(beginTextMatch)
          ? true
          : thisContext.createError({
              message: translate.t("validations.invalidTextBeginning", {
                chars: `'${beginTextMatch[0]}'`,
              }),
            });
      },
    })
    .test({
      exclusive: false,
      name: "invalidTextPattern",
      params: {},
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
          return false;
        }
        const contentTextMatch: RegExpMatchArray | null =
          /["',;](?:[-=+@\t\r])/u.exec(value);

        return _.isNull(contentTextMatch)
          ? true
          : thisContext.createError({
              message: translate.t("validations.invalidTextPattern", {
                chars: `'${contentTextMatch[0]}'`,
              }),
            });
      },
    }),
  lastCommit: string()
    .required(translate.t("validations.required"))
    .matches(
      /^[A-Fa-f0-9]{40}$|^[A-Fa-f0-9]{64}$/u,
      translate.t("validations.commitHash")
    ),
  loc: number()
    .required(translate.t("validations.required"))
    .test(
      "isZeroOrPositive",
      translate.t("validations.zeroOrPositive"),
      (value: number | undefined): boolean => {
        if (value === undefined) {
          return false;
        }

        return value >= 0;
      }
    )
    .test(
      "isOptionalInteger",
      translate.t("validations.integer"),
      (value: number | undefined): boolean => {
        return _.isInteger(value) || (_.isString(value) && _.isEmpty(value));
      }
    ),
});

export { validations };

import _ from "lodash";
import type { TestContext, ValidationError } from "yup";
import { object, string } from "yup";

import { translate } from "utils/translations/translate";

const MAX_BUSINESS_INFO_LENGTH: number = 60;
const MAX_DESCRIPTION_LENGTH: number = 200;
const min: number = 1;
const max: number = 10;

const validations = object().shape({
  businessId: string()
    .nullable()
    .max(
      MAX_BUSINESS_INFO_LENGTH,
      translate.t("validations.maxLength", { count: MAX_BUSINESS_INFO_LENGTH })
    )
    .test({
      exclusive: false,
      name: "invalidTextBeginning",
      params: {},
      test: (
        value: string | null | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined || _.isNull(value)) {
          return true;
        }
        const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);

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
      name: "invalidTextField",
      params: {},
      test: (
        value: string | null | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined || _.isNull(value)) {
          return true;
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
  businessName: string()
    .nullable()
    .max(
      MAX_BUSINESS_INFO_LENGTH,
      translate.t("validations.maxLength", { count: MAX_BUSINESS_INFO_LENGTH })
    )
    .test({
      exclusive: false,
      name: "invalidTextBeginning",
      params: {},
      test: (
        value: string | null | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined || _.isNull(value)) {
          return true;
        }
        const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);

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
      name: "invalidTextField",
      params: {},
      test: (
        value: string | null | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined || _.isNull(value)) {
          return true;
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
  description: string()
    .nullable()
    .required(translate.t("validations.required"))
    .max(
      MAX_DESCRIPTION_LENGTH,
      translate.t("validations.maxLength", { count: MAX_DESCRIPTION_LENGTH })
    )
    .test({
      exclusive: false,
      name: "invalidTextBeginning",
      params: {},
      test: (
        value: string | null | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined || _.isNull(value)) {
          return true;
        }
        const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);

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
      name: "invalidTextField",
      params: {},
      test: (
        value: string | null | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined || _.isNull(value)) {
          return true;
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
  sprintDuration: string()
    .matches(/^\d+$/u, translate.t("validations.numeric"))
    .test(
      "numberBetween",
      translate.t("validations.between", { max, min }),
      (value): boolean => {
        if (value === undefined) {
          return false;
        }

        return Number(value) > min && Number(value) < max;
      }
    ),
  sprintStartDate: string()
    .required(translate.t("validations.required"))
    .test(
      "greaterDate",
      translate.t("validations.greaterDate"),
      (value?: string): boolean => {
        if (value === undefined) {
          return false;
        }
        const date: Date = new Date(value);
        const today: Date = new Date();

        return date <= today;
      }
    ),
});

export { validations };

import _ from "lodash";
import type { TestContext, ValidationError } from "yup";
import { array, date, number, object, string } from "yup";

import { translate } from "utils/translations/translate";

const MAX_LENGTH: number = 100;
const today: Date = new Date();

const validations = object().shape({
  closingDate: date().max(today, translate.t("validations.greaterDate")),
  location: string()
    .max(
      MAX_LENGTH,
      translate.t("validations.maxLength", { count: MAX_LENGTH })
    )
    .test({
      exclusive: false,
      name: "invalidTextBeginning",
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
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
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
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
  maxReleaseDate: date()
    .max(new Date(), translate.t("validations.greaterDate"))
    .test({
      exclusive: false,
      message: "Must be greater than or equal to Min release date",
      name: "min",
      params: {},
      test: (value: Date | undefined, thisContext: TestContext): boolean => {
        const { minReleaseDate } = thisContext.parent;

        return value === undefined || minReleaseDate === undefined
          ? true
          : value >= minReleaseDate;
      },
    }),
  maxSeverity: number()
    .max(10)
    .test({
      exclusive: false,
      message: "Must be greater than or equal to Min severity",
      name: "min",
      params: {},
      test: (value: number | undefined, thisContext: TestContext): boolean => {
        const { minSeverity } = thisContext.parent;

        return value === undefined || minSeverity === undefined
          ? true
          : value >= (minSeverity ?? 0);
      },
    }),
  minReleaseDate: date()
    .max(new Date(), translate.t("validations.greaterDate"))
    .test({
      exclusive: false,
      message: "Must be less than or equal to Max release date",
      name: "max",
      params: {},
      test: (value: Date | undefined, thisContext: TestContext): boolean => {
        const { maxReleaseDate } = thisContext.parent;

        return value === undefined || maxReleaseDate === undefined
          ? true
          : value <= maxReleaseDate;
      },
    }),
  minSeverity: number()
    .min(0)
    .test({
      exclusive: false,
      message: "Must be less than or equal to Max severity",
      name: "max",
      params: {},
      test: (value: number | undefined, thisContext: TestContext): boolean => {
        const { maxSeverity } = thisContext.parent;

        return value === undefined || maxSeverity === undefined
          ? true
          : value <= (maxSeverity ?? 10);
      },
    }),
  states: array().min(1, translate.t("validations.someRequired")),
  treatments: array().when("closingDate", {
    is: (closingDate: string): boolean => _.isEmpty(closingDate),
    otherwise: array().notRequired(),
    then: array().min(1, translate.t("validations.someRequired")),
  }),
});

export { validations };

import _ from "lodash";
import type { TestContext, ValidationError } from "yup";
import { mixed, object, string } from "yup";

import { translate } from "utils/translations/translate";

const MAX_DESCRIPTION_LENGTH: number = 200;
const MAX_GROUP_NAME_LENGTH: number = 20;
const MIN_GROUP_NAME_LENGTH: number = 4;
const MAX_ORGANIZATION_LENGTH: number = 50;

const validations = object().shape({
  description: string()
    .required(translate.t("validations.required"))
    .max(
      MAX_DESCRIPTION_LENGTH,
      translate.t("validations.maxLength", { count: MAX_DESCRIPTION_LENGTH })
    )
    .test({
      exclusive: false,
      name: "invalidTextBeginning",
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
          return false;
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
  name: string()
    .required(translate.t("validations.required"))
    .matches(/^[a-zA-Z0-9]+$/u, translate.t("validations.alphanumeric"))
    .max(
      MAX_GROUP_NAME_LENGTH,
      translate.t("validations.maxLength", { count: MAX_GROUP_NAME_LENGTH })
    )
    .min(
      MIN_GROUP_NAME_LENGTH,
      translate.t("validations.minLength", { count: MIN_GROUP_NAME_LENGTH })
    ),
  organization: string()
    .required(translate.t("validations.required"))
    .max(
      MAX_ORGANIZATION_LENGTH,
      translate.t("validations.maxLength", { count: MAX_ORGANIZATION_LENGTH })
    )
    .test({
      exclusive: false,
      name: "invalidTextBeginning",
      test: (
        value: string | undefined,
        thisContext: TestContext
      ): ValidationError | boolean => {
        if (value === undefined) {
          return false;
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
  type: mixed().required(translate.t("validations.required")),
});

export { validations };

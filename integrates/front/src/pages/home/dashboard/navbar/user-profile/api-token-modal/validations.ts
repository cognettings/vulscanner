import _ from "lodash";
import type { BaseSchema, InferType, TestContext, ValidationError } from "yup";
import { lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import { translate } from "utils/translations/translate";

const MAX_NAME_LENGTH = 20;
const validateSchema = (): InferType<TypedSchema> =>
  lazy(
    (): BaseSchema =>
      object().shape({
        expirationTime: string()
          .required(translate.t("validations.required"))
          .test(
            "isLowerDate",
            translate.t("validations.lowerDate"),
            (value?: string): boolean => {
              if (value === undefined || _.isEmpty(value)) {
                return false;
              }
              const date: Date = new Date(value);
              const today: Date = new Date();

              return date > today;
            }
          )
          .test(
            "isValidDateAccessToken",
            translate.t("validations.validDateToken"),
            (value?: string): boolean => {
              if (value === undefined || _.isEmpty(value)) {
                return false;
              }
              const today = new Date();
              const date = new Date(value);
              const sixMonths = new Date(today.setMonth(today.getMonth() + 6));

              return date < sixMonths;
            }
          ),
        name: string()
          .required(translate.t("validations.required"))
          .max(
            MAX_NAME_LENGTH,
            translate.t("validations.maxLength", { count: MAX_NAME_LENGTH })
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
      })
  );

export { validateSchema };

import _ from "lodash";
import type { TestContext, ValidationError } from "yup";
import { mixed, object, string } from "yup";

import { translate } from "utils/translations/translate";

const MAX_LENGTH: number = 200;
const MAX_FILE_SIZE: number = 5000;

const addFilesModalSchema = object().shape({
  description: string()
    .matches(/^(?!=).+/u, translate.t("validations.invalidValueInField"))
    .max(
      MAX_LENGTH,
      translate.t("validations.maxLength", { count: MAX_LENGTH - 1 })
    )
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
  file: mixed()
    .required(translate.t("validations.required"))
    .test(
      "isValidFileName",
      translate.t("searchFindings.tabResources.invalidChars"),
      (value?: FileList): boolean => {
        if (value === undefined || _.isEmpty(value)) {
          return false;
        }
        const fileName: string = value[0].name;
        const name: string[] = fileName.split(".");
        const validCharacters: RegExp = /^[A-Za-z0-9!\-_.*'()&$@=;:+,?\s]*$/u;

        return name.length <= 2 && validCharacters.test(fileName);
      }
    )
    .test(
      "isValidFileSize",
      translate.t("validations.fileSize", { count: MAX_FILE_SIZE }),
      (value?: FileList): boolean => {
        if (value === undefined || _.isEmpty(value)) {
          return false;
        }
        const MIB: number = 1048576;

        return [...Array(value.length).keys()].every(
          (index: number): boolean => value[index].size < MIB * MAX_FILE_SIZE
        );
      }
    ),
});

export { addFilesModalSchema };

import { object, string } from "yup";

import { translate } from "utils/translations/translate";

const MAX_RESPONSIBILITY_LENGTH: number = 50;

const validations = object().shape({
  email: string()
    .email(translate.t("validations.email"))
    .required(translate.t("validations.required")),
  responsibility: string()
    .when("type", {
      is: "group",
      otherwise: string().nullable(),
      then: string()
        .required(translate.t("validations.required"))
        .matches(
          /^[a-zA-Z0-9\s]+$|^-$/u,
          translate.t("validations.alphanumeric")
        )
        .nullable(),
    })
    .max(
      MAX_RESPONSIBILITY_LENGTH,
      translate.t("validations.maxLength", {
        count: MAX_RESPONSIBILITY_LENGTH,
      })
    ),
  /*
   * The forbidden characters (e.g. =,'',"") check
   * will still be performed by the old custom
   * method via field-level validation
   */
  role: string().required(translate.t("validations.required")),
});

export { validations };

import type { BaseSchema, InferType } from "yup";
import { lazy, number, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import { translate } from "utils/translations/translate";

const minInactivityPeriod: number = 21;
const maxInactivityPeriod: number = 999;
const minSeverity: number = 0.0;
const maxSeverity: number = 10.0;

const numberBetweenInactivity = (
  isInactivityPeriodHide: boolean
): ((value: string | undefined) => boolean) => {
  return (value: string | undefined): boolean => {
    if (isInactivityPeriodHide) {
      return true;
    }
    if (value === undefined) {
      return false;
    }

    return (
      Number(value) >= minInactivityPeriod &&
      Number(value) <= maxInactivityPeriod
    );
  };
};

const numberBetweenSeverity = (value: string | undefined): boolean => {
  if (value === undefined) {
    return false;
  }

  return Number(value) >= minSeverity && Number(value) <= maxSeverity;
};

const isZeroOrPositive = (value: number | undefined): boolean => {
  if (value === undefined) {
    return false;
  }

  return value >= 0;
};

const isFloatOrInteger = (value: string | undefined): boolean => {
  function checkNumeric(valueToValidate: never): boolean {
    return !isNaN(valueToValidate - parseFloat(valueToValidate));
  }
  if (value === undefined || (value !== "" && !checkNumeric(value as never))) {
    return false;
  }

  return true;
};

const validateSchema = (
  isInactivityPeriodHide: boolean
): InferType<TypedSchema> =>
  lazy(
    (): BaseSchema =>
      object().shape({
        inactivityPeriod: string()
          .matches(/^\d+$/u, translate.t("validations.numeric"))
          .test(
            "numberBetween",
            translate.t("validations.between", {
              max: maxInactivityPeriod,
              min: minInactivityPeriod,
            }),
            numberBetweenInactivity(isInactivityPeriodHide)
          ),
        maxAcceptanceDays: number().test(
          "isZeroOrPositive",
          translate.t("validations.zeroOrPositive"),
          isZeroOrPositive
        ),
        maxAcceptanceSeverity: string()
          .test(
            "numberBetween",
            translate.t("validations.between", {
              max: maxSeverity,
              min: minSeverity,
            }),
            numberBetweenSeverity
          )
          .test(
            "floatOrInteger",
            translate.t("validations.numeric"),
            isFloatOrInteger
          ),
        maxNumberAcceptances: number().test(
          "isZeroOrPositive",
          translate.t("validations.zeroOrPositive"),
          isZeroOrPositive
        ),
        minAcceptanceSeverity: string()
          .test(
            "numberBetween",
            translate.t("validations.between", {
              max: maxSeverity,
              min: minSeverity,
            }),
            numberBetweenSeverity
          )
          .test(
            "floatOrInteger",
            translate.t("validations.numeric"),
            isFloatOrInteger
          ),
        minBreakingSeverity: string()
          .test(
            "numberBetween",
            translate.t("validations.between", {
              max: maxSeverity,
              min: minSeverity,
            }),
            numberBetweenSeverity
          )
          .test(
            "floatOrInteger",
            translate.t("validations.numeric"),
            isFloatOrInteger
          ),
        vulnerabilityGracePeriod: number().test(
          "isZeroOrPositive",
          translate.t("validations.zeroOrPositive"),
          isZeroOrPositive
        ),
      })
  );

export { validateSchema };

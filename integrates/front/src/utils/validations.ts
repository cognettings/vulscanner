import type { Dayjs } from "dayjs";
import dayjs, { extend, isDayjs } from "dayjs";
import isSameOrBefore from "dayjs/plugin/isSameOrBefore";
import _ from "lodash";
import {
  hasLengthLessThan,
  isNumeric,
  isRequired,
  matchesPattern,
} from "revalidate";

import type { IPhoneData } from "components/Input/utils";
import { translate } from "utils/translations/translate";

/**
 *Validations.ts is legacy code or used for complex validations,
 *Use Yup validations schema instead.
 */

/**
 * Groups single or multiple field-level validations and returns the first error
 *
 * Example: composeValidators([val1, val2, val3])
 */

// Needed for compatibility with all kind of validators
// eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-type-alias
type Validator = (value: any, allValues?: any, props?: any, name?: any) => any;

const composeValidators =
  (
    // Needed for compatibility with ConfigurableValidator parameters
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    args: ((value: any) => string | undefined)[]
  ): ((value: unknown) => string | undefined) =>
  (value: unknown): string | undefined => {
    const errors = args
      .map((validator): string | undefined => validator(value))
      .filter((error): boolean => error !== undefined);

    return errors[0];
  };

const required: Validator = isRequired({
  message: translate.t("validations.required"),
});

function checkIfValid(
  hasDescription: boolean,
  hasUrl: boolean,
  hasFileSelected: boolean
): string | undefined {
  if (hasDescription) {
    if (hasUrl) {
      return undefined;
    }

    return hasFileSelected
      ? undefined
      : translate.t("groupAlerts.noFileSelected");
  }

  return hasFileSelected ? translate.t("validations.required") : undefined;
}

const isValidEvidenceDescription: (
  url: string | undefined,
  file: object | undefined
) => Validator =
  (url: string | undefined, file: object | undefined): Validator =>
  (value: string | undefined): string | undefined => {
    const hasUrl: boolean = url !== "";
    const hasDescription: boolean = value !== "";
    const hasFileSelected: boolean = file !== undefined;

    return checkIfValid(hasDescription, hasUrl, hasFileSelected);
  };

const validTextField: Validator = (value: string): string | undefined => {
  if (!_.isNil(value)) {
    const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);
    if (!_.isNull(beginTextMatch)) {
      return translate.t("validations.invalidTextBeginning", {
        chars: `'${beginTextMatch[0]}'`,
      });
    }

    const textMatch: RegExpMatchArray | null =
      // We use them for control character pattern matching.
      // eslint-disable-next-line no-control-regex
      /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s(){}[\],./:;@&_$%'#*=¿?¡!+-]/u.exec(
        value
      );
    if (!_.isNull(textMatch)) {
      return translate.t("validations.invalidTextField", {
        chars: `'${textMatch[0]}'`,
      });
    }

    return undefined;
  }

  return undefined;
};

const validUrlField: (value: string) => string | undefined = (
  value: string
): string | undefined => {
  if (_.isNil(value)) {
    return undefined;
  }

  const encodedCharWhitelist: string[] = ["%20"];

  const cleanValue: string = encodedCharWhitelist.reduce(
    (valueBeingCleaned: string, encodedChar: string): string =>
      valueBeingCleaned.replace(new RegExp(encodedChar, "gu"), ""),
    value
  );
  if (!_.isNil(cleanValue)) {
    const textMatch: RegExpMatchArray | null = /^=/u.exec(value);
    if (!_.isNull(textMatch)) {
      return translate.t("validations.invalidTextBeginning", {
        chars: `'${textMatch[0]}'`,
      });
    }

    const urlMatch: RegExpMatchArray | null =
      /[^a-zA-Z0-9(),./:;@_$#=?-]/u.exec(cleanValue);
    if (!_.isNull(urlMatch)) {
      return translate.t("validations.invalidUrlField", {
        chars: `'${urlMatch[0]}'`,
      });
    }

    return undefined;
  }

  return undefined;
};

const numberBetween: (min: number, max: number) => Validator =
  (min: number, max: number): Validator =>
  (value: number): string | undefined =>
    value < min || value > max
      ? translate.t("validations.between", { max, min })
      : undefined;

const optionalNumberBetween: (min: number, max: number) => Validator =
  (min: number, max: number): Validator =>
  (value: number | string): string | undefined =>
    _.isNumber(value) && (value < min || value > max)
      ? translate.t("validations.between", { max, min })
      : undefined;

const maxLength: (max: number) => Validator = (max: number): Validator =>
  hasLengthLessThan(max)({
    message: translate.t("validations.maxLength", { count: max - 1 }),
  }) as Validator;

const numeric: Validator = isNumeric({
  message: translate.t("validations.numeric"),
});

const validEmail: Validator = matchesPattern(
  /^[a-zA-Z0-9.!#$%&’*/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/u
)({
  message: translate.t("validations.email"),
});

const validCommitHash: Validator = matchesPattern(
  /^[A-Fa-f0-9]{40}$|^[A-Fa-f0-9]{64}$/u
)({
  message: translate.t("validations.commitHash"),
});

const validDraftTitle: (title: string) => string | undefined = (
  title: string
): string | undefined => {
  if (/^\d{3}\. .+/gu.test(title)) {
    return undefined;
  }

  return translate.t("validations.draftTitle");
};

const validFindingTypology: (titleSuggestions: string[]) => Validator =
  (titleSuggestions: string[]): Validator =>
  (title: string): string | undefined => {
    if (titleSuggestions.includes(title)) {
      return undefined;
    }

    return translate.t("validations.draftTypology");
  };

const isValidVulnSeverity: Validator = (value: string): string | undefined => {
  const min: number = 0;
  const max: number = 1000000000;
  if (
    _.isUndefined(
      isNumeric({ message: translate.t("validations.numeric") }, value)
    )
  ) {
    const severityBetween: (input: number) => string | undefined =
      numberBetween(min, max);

    return severityBetween(Number(value));
  }

  return translate.t("validations.between", { max, min });
};

const validDatetime: Validator = (value?: Dayjs | string): string | undefined =>
  isDayjs(value) ? undefined : translate.t("validations.datetime");

const isValidPhoneNumber: Validator = (
  value: IPhoneData | undefined
): string | undefined => {
  if (
    !_.isUndefined(value) &&
    /^(?:\d ?){6,11}\d$/u.test(value.nationalNumber)
  ) {
    return undefined;
  }

  return translate.t("validations.invalidPhoneNumber");
};

const getFileExtension: (file: File) => string = (file: File): string => {
  const splittedName: string[] = file.name.split(".");
  const extension: string =
    splittedName.length > 1 ? (_.last(splittedName) as string) : "";

  return extension.toLowerCase();
};

const hasExtension: (
  allowedExtensions: string[] | string,
  file?: File
) => boolean = (allowedExtensions: string[] | string, file?: File): boolean => {
  if (!_.isUndefined(file)) {
    return _.includes(allowedExtensions, getFileExtension(file));
  }

  return false;
};

const validEventFile: Validator = (value: FileList): string | undefined =>
  _.isEmpty(value) || hasExtension(["pdf", "zip", "csv", "txt"], _.first(value))
    ? undefined
    : translate.t("group.events.form.wrongFileType");

const validEvidenceImage: Validator = (
  value: FileList | undefined
): string | undefined =>
  _.isUndefined(value) ||
  (!_.isUndefined(value) &&
    [...Array(value.length).keys()].every((index: number): boolean =>
      hasExtension(["png", "webm"], value[index])
    ))
    ? undefined
    : translate.t("group.events.form.wrongImageType");

const isValidEvidenceName: (
  organizationName: string,
  groupName: string
) => Validator =
  (organizationName: string, groupName: string): Validator =>
  (file: FileList | undefined): string | undefined => {
    return _.isUndefined(file) ||
      (!_.isUndefined(file) &&
        [...Array(file.length).keys()].every((index: number): boolean => {
          const filename = file[index].name.toLocaleLowerCase();
          const extensions = getFileExtension(file[index]);
          const starts = `${organizationName.toLocaleLowerCase()}-${groupName.toLocaleLowerCase()}-`;
          const [ends] = filename.split(starts).slice(-1);
          const regex = /^[a-zA-Z0-9]{10}$/u;

          return (
            filename.startsWith(starts) &&
            regex.test(ends.replace(`.${extensions}`, ""))
          );
        }))
      ? undefined
      : translate.t("group.events.form.wrongImageName");
  };

const validRecordsFile: Validator = (value: FileList): string | undefined =>
  hasExtension("csv", _.first(value))
    ? undefined
    : translate.t("groupAlerts.fileTypeCsv");

const dateTimeBeforeToday: Validator = (date: Dayjs): string | undefined => {
  const today: Dayjs = dayjs();

  // Formik validation needs this seemingly unnecessary undefined check
  // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
  if (!(date instanceof dayjs)) {
    return undefined;
  }

  extend(isSameOrBefore);

  return date.isSameOrBefore(today)
    ? undefined
    : translate.t("validations.greaterDate");
};

const validPath: (host: string | undefined) => Validator =
  (host: string | undefined): Validator =>
  (path: string): string | undefined => {
    const formmattedHost = host
      ?.replace("https://", "")
      .replace("http://", "")
      .slice(0, -1);
    if (
      (!_.isUndefined(formmattedHost) && path.includes(formmattedHost)) ||
      path.includes("https://") ||
      path.includes("http://")
    ) {
      return translate.t("validations.excludePathHost");
    }

    if (!_.isEmpty(path) && path.startsWith("/")) {
      return translate.t("validations.invalidTextBeginning", {
        chars: "/",
      });
    }

    return undefined;
  };

const isValidFileSize: (maxSize: number) => Validator =
  (maxSize: number): Validator =>
  (file: FileList | undefined): string | undefined => {
    const MIB: number = 1048576;

    return _.isUndefined(file) ||
      (!_.isUndefined(file) &&
        [...Array(file.length).keys()].every(
          (index: number): boolean => file[index].size < MIB * maxSize
        ))
      ? undefined
      : translate.t("validations.fileSize", { count: maxSize });
  };

const isValidAmountOfFiles: (maxFiles: number) => Validator =
  (maxFiles: number): Validator =>
  (file: FileList | undefined): string | undefined => {
    return _.isUndefined(file) ||
      (!_.isUndefined(file) && file.length <= maxFiles)
      ? undefined
      : translate.t("validations.amountOfFiles", { count: maxFiles });
  };

const isLowerDate: Validator = (value: string): string | undefined => {
  const date: Date = new Date(value);
  const today: Date = new Date();

  if (date <= today) {
    return translate.t("validations.lowerDate");
  }

  return undefined;
};

export {
  composeValidators,
  required,
  isValidEvidenceDescription,
  validTextField,
  validUrlField,
  numberBetween,
  optionalNumberBetween,
  maxLength,
  numeric,
  validEmail,
  validDraftTitle,
  validPath,
  isValidAmountOfFiles,
  isValidPhoneNumber,
  isValidVulnSeverity,
  validCommitHash,
  validDatetime,
  validEventFile,
  validEvidenceImage,
  validFindingTypology,
  validRecordsFile,
  dateTimeBeforeToday,
  isValidEvidenceName,
  isValidFileSize,
  isLowerDate,
};

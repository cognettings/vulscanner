/* eslint-disable react/forbid-prop-types */
import type { FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import type { BaseSchema, InferType } from "yup";
import { array, lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import type { IFormValues, IGitRootAttr } from "../types";
import {
  formatBooleanHealthCheck,
  getAddGitRootCredentials,
  getUpdateGitRootCredentials,
} from "../utils";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

// GitModal helpers

type modalMessages = React.Dispatch<
  React.SetStateAction<{
    message: string;
    type: string;
  }>
>;

const validateValue = (regex: RegExp, value: string | undefined): boolean => {
  if (value === undefined) {
    return true;
  }

  return regex.test(value);
};
const validateSshFormat = (
  regex: RegExp,
  value: string | undefined,
  values: IFormValues
): boolean => {
  if (value === undefined || values.credentials.type !== "SSH") {
    return true;
  }

  return regex.test(value);
};

const validCredentialType = (
  value: string | undefined,
  values: IFormValues
): boolean => {
  if (
    _.isUndefined(value) ||
    _.isUndefined(values.url) ||
    !_.includes(["OAUTH"], value) ||
    _.isEmpty(values.url)
  ) {
    return true;
  }
  try {
    const { protocol } = new URL(values.url);

    return _.includes(["OAUTH"], value) && protocol.toLowerCase() === "https:";
  } catch {
    return true;
  }
};

const validateExcludeFormat = (
  repoUrl: string,
  value: string | undefined
): boolean => {
  if (!_.isUndefined(repoUrl) && !_.isUndefined(value)) {
    const [urlBasename] = repoUrl.split("/").slice(-1);
    const repoName: string = urlBasename.endsWith(".git")
      ? urlBasename.replace(".git", "")
      : urlBasename;

    return value.toLowerCase().split("/").indexOf(repoName.toLowerCase()) !== 0;
  }

  return false;
};

const validateHealthCheck = (
  gitRootsPermissions: {
    canAddExclusions: boolean;
    hasSquad: boolean;
  },
  isCheckedHealthCheck: boolean,
  values: IFormValues
): boolean => {
  const { healthCheckConfirm, includesHealthCheck } = values;
  if (!gitRootsPermissions.hasSquad || isCheckedHealthCheck) {
    return true;
  }
  if (
    formatBooleanHealthCheck(includesHealthCheck) !== null &&
    formatBooleanHealthCheck(includesHealthCheck) === false &&
    healthCheckConfirm === undefined
  ) {
    return true;
  }
  if (healthCheckConfirm === undefined) {
    return false;
  }

  return (
    ((formatBooleanHealthCheck(includesHealthCheck) ?? false) &&
      healthCheckConfirm.includes("includeA")) ||
    (!(formatBooleanHealthCheck(includesHealthCheck) ?? true) &&
      healthCheckConfirm.includes("rejectA") &&
      healthCheckConfirm.includes("rejectB") &&
      healthCheckConfirm.includes("rejectC"))
  );
};

const gitModalSchema = (
  isEditing: boolean,
  credExists: boolean,
  gitRootsPermissions: {
    canAddExclusions: boolean;
    hasSquad: boolean;
  },
  isCheckedHealthCheck: boolean,
  isGitAccessible: boolean
  // Exception: FP(parameters are necessary)
  // eslint-disable-next-line
): InferType<TypedSchema> => // NOSONAR
  lazy(
    (values: IFormValues): BaseSchema =>
      object().shape({
        branch: string().required(translate.t("validations.required")),
        credentials: object({
          azureOrganization: string().when(["type", "isPat"], {
            is: (type: string, isPat: boolean): boolean =>
              !credExists &&
              type ===
                (values.credentials.typeCredential === "TOKEN"
                  ? "HTTPS"
                  : "") &&
              isPat,
            otherwise: string(),
            then: string()
              .required(translate.t("validations.required"))
              .test(
                "hasValidValue",
                translate.t("validations.invalidSpaceField"),
                (value): boolean => {
                  const regex = /\S/u;

                  return validateValue(regex, value);
                }
              )
              .test(
                "invalidSpaceInField",
                translate.t("validations.invalidSpaceInField"),
                (value): boolean => {
                  if (value === undefined) {
                    return true;
                  }

                  return !value.includes(" ");
                }
              ),
          }),
          id: string(),
          key: string()
            .when("type", {
              is: credExists ? "" : "SSH",
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (): boolean => {
                return isGitAccessible;
              }
            )
            .test(
              "hasSshFormat",
              translate.t("validations.invalidSshFormat"),
              (value): boolean => {
                const regex =
                  /^-{5}BEGIN OPENSSH PRIVATE KEY-{5}\n(?:[a-zA-Z0-9+/=]+\n)+-{5}END OPENSSH PRIVATE KEY-{5}\n?$/u;

                return validateSshFormat(regex, value, values);
              }
            ),
          name: isEditing
            ? string().when("type", {
                is: undefined,
                otherwise: string().required(
                  translate.t("validations.required")
                ),
                then: string(),
              })
            : string()
                .required(translate.t("validations.required"))
                .test(
                  "hasValidValue",
                  translate.t("validations.invalidSpaceField"),
                  (value): boolean => {
                    const regex = /\S/u;

                    return validateValue(regex, value);
                  }
                ),
          password: string()
            .when("type", {
              is:
                !credExists && values.credentials.typeCredential === "USER"
                  ? "HTTPS"
                  : "",
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (): boolean => {
                return isGitAccessible;
              }
            )
            .test(
              "hasValidValue",
              translate.t("validations.invalidSpaceField"),
              (value): boolean => {
                const regex = /\S/u;

                return validateValue(regex, value);
              }
            ),
          token: string()
            .when("type", {
              is:
                !credExists && values.credentials.typeCredential === "TOKEN"
                  ? "HTTPS"
                  : "",
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (): boolean => {
                return isGitAccessible;
              }
            )
            .test(
              "hasValidValue",
              translate.t("validations.invalidSpaceField"),
              (value): boolean => {
                const regex = /\S/u;

                return validateValue(regex, value);
              }
            ),
          type: isEditing
            ? string()
            : string().required(translate.t("validations.required")),
          typeCredential: isEditing
            ? string()
            : string()
                .required(translate.t("validations.required"))
                .test(
                  "hasInvalidCredentialType",
                  translate.t("validations.invalidCredentialType"),
                  (value): boolean => {
                    return validCredentialType(value, values);
                  }
                ),
          user: string()
            .when("type", {
              is:
                !credExists && values.credentials.typeCredential === "USER"
                  ? "HTTPS"
                  : "",
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (): boolean => {
                return isGitAccessible;
              }
            )
            .test(
              "hasValidValue",
              translate.t("validations.invalidSpaceField"),
              (value): boolean => {
                const regex = /\S/u;

                return validateValue(regex, value);
              }
            ),
        }),
        environment: string().required(translate.t("validations.required")),
        gitignore: array().of(
          string()
            .required(translate.t("validations.required"))
            .test(
              "excludeFormat",
              translate.t("validations.excludeFormat"),
              (value): boolean => {
                const repoUrl = values.url;

                return validateExcludeFormat(repoUrl, value);
              }
            )
        ),
        hasExclusions: string().when("$canAddExclusions", {
          is: (): boolean => gitRootsPermissions.canAddExclusions,
          otherwise: string(),
          then: string().required(translate.t("validations.required")),
        }),
        healthCheckConfirm: array()
          .of(string())
          .test(
            "isChecked",
            translate.t("validations.required"),
            (): boolean => {
              return validateHealthCheck(
                gitRootsPermissions,
                isCheckedHealthCheck,
                values
              );
            }
          ),
        includesHealthCheck: string().when("$hasSquad", {
          is: (): boolean => gitRootsPermissions.hasSquad,
          otherwise: string(),
          then: string().required(translate.t("validations.required")),
        }),
        url: string().required(translate.t("validations.required")),
      })
  );

// Index helpers

const handleCreationError = (
  graphQLErrors: readonly GraphQLError[],
  setModalMessages: modalMessages
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        setModalMessages({
          message: translate.t("group.scope.git.errors.invalid"),
          type: "error",
        });
        break;
      case "Exception - Root with the same nickname already exists":
        setModalMessages({
          message: translate.t("group.scope.common.errors.duplicateNickname"),
          type: "error",
        });
        break;
      case "Exception - Root with the same URL/branch already exists":
        setModalMessages({
          message: translate.t("group.scope.common.errors.duplicateUrl"),
          type: "error",
        });
        break;
      case "Exception - Root name should not be included in the exception pattern":
        setModalMessages({
          message: translate.t("group.scope.git.errors.rootInGitignore"),
          type: "error",
        });
        break;
      case "Exception - Invalid characters":
        setModalMessages({
          message: translate.t("validations.invalidChar"),
          type: "error",
        });
        break;
      case "Exception - Unsanitized input found":
        setModalMessages({
          message: translate.t("validations.unsanitizedInputFound"),
          type: "error",
        });
        break;
      case "Exception - A credential exists with the same name":
        setModalMessages({
          message: translate.t("validations.invalidCredentialName"),
          type: "error",
        });
        break;
      case "Exception - Git repository was not accessible with given credentials":
        setModalMessages({
          message: translate.t("group.scope.git.errors.invalidGitCredentials"),
          type: "error",
        });
        break;
      case "Exception - Branch not found":
        setModalMessages({
          message: translate.t("group.scope.git.errors.invalidBranch"),
          type: "error",
        });
        break;
      case "Exception - Field cannot fill with blank characters":
        setModalMessages({
          message: translate.t("validations.invalidSpaceField"),
          type: "error",
        });
        break;
      case "Exception - The action is not allowed during the free trial":
        msgError(translate.t("group.scope.git.errors.trial"));
        break;
      default:
        setModalMessages({
          message: translate.t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.error("Couldn't add git roots", error);
    }
  });
};

const handleUpdateError = (
  graphQLErrors: readonly GraphQLError[],
  setModalMessages: modalMessages,
  scope: "envs" | "root" | "tours"
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    const showMessage = (translation: string): void => {
      if (scope === "root" || scope === "envs") {
        setModalMessages({
          message: translate.t(translation),
          type: "error",
        });
      } else {
        msgError(translate.t(translation));
      }
    };
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        showMessage("group.scope.git.errors.invalid");
        break;
      case "Exception - A root with reported vulns can't be updated":
        showMessage("group.scope.common.errors.hasVulns");
        break;
      case "Exception - Root with the same URL/branch already exists":
        showMessage("group.scope.common.errors.duplicateUrl");
        break;
      case "Exception - Root with the same nickname already exists":
        showMessage("group.scope.common.errors.duplicateNickname");
        break;
      case "Exception - Invalid characters":
        showMessage("validations.invalidChar");
        break;
      case "Exception - Git repository was not accessible with given credentials":
        showMessage("group.scope.git.errors.invalidGitCredentials");
        break;
      case "Exception - A credential exists with the same name":
        showMessage("validations.invalidCredentialName");
        break;
      case "Exception - Unsanitized input found":
        setModalMessages({
          message: translate.t("validations.unsanitizedInputFound"),
          type: "error",
        });
        break;
      default:
        showMessage("groupAlerts.errorTextsad");
        Logger.error(`Couldn't update git ${scope}`, error);
    }
  });
};

const handleActivationError = (
  graphQLErrors: readonly GraphQLError[]
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    if (
      error.message ===
      "Exception - Root with the same URL/branch already exists"
    ) {
      msgError(translate.t("group.scope.common.errors.duplicateUrl"));
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.error("Couldn't activate root", error);
    }
  });
};

const handleSyncError = (graphQLErrors: readonly GraphQLError[]): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Access denied or credential not found":
        msgError(translate.t("group.scope.git.sync.noCredentials"));
        break;
      case "Exception - The root already has an active cloning process":
        msgError(translate.t("group.scope.git.sync.alreadyCloning"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't queue root cloning", error);
    }
  });
};

const hasCheckedItem = (
  checkedItems: Record<string, boolean>,
  columnName: string
): boolean => {
  return (
    Object.values(checkedItems).filter((val: boolean): boolean => val)
      .length === 1 && checkedItems[columnName]
  );
};

function useGitSubmit(
  addGitRoot: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  groupName: string,
  isManagingRoot: false | { mode: "ADD" | "EDIT" },
  setModalMessages: modalMessages,
  updateGitRoot: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>
): ({
  branch,
  credentials,
  environment,
  gitignore,
  id,
  includesHealthCheck,
  nickname,
  url,
  useVpn,
}: IFormValues) => Promise<void> {
  return useCallback(
    async ({
      branch,
      credentials,
      environment,
      gitignore,
      id,
      includesHealthCheck,
      nickname,
      url,
      useVpn,
    }: IFormValues): Promise<void> => {
      setModalMessages({ message: "", type: "success" });
      if (isManagingRoot !== false) {
        if (isManagingRoot.mode === "ADD") {
          mixpanel.track("AddGitRoot");
          await addGitRoot({
            variables: {
              branch: branch.trim(),
              credentials: getAddGitRootCredentials(credentials),
              environment,
              gitignore,
              groupName,
              includesHealthCheck:
                formatBooleanHealthCheck(includesHealthCheck) ?? false,
              nickname,
              url: url.trim(),
              useVpn,
            },
          });
        } else {
          mixpanel.track("EditGitRoot");
          await updateGitRoot({
            variables: {
              branch,
              credentials: getUpdateGitRootCredentials(credentials),
              environment,
              gitignore,
              groupName,
              id,
              includesHealthCheck:
                formatBooleanHealthCheck(includesHealthCheck) ?? false,
              nickname: "",
              url,
              useVpn,
            },
          });
        }
      }
    },
    [addGitRoot, groupName, isManagingRoot, setModalMessages, updateGitRoot]
  );
}

function filterSelectStatus(
  rows: IGitRootAttr[],
  currentValue: string
): IGitRootAttr[] {
  return rows.filter((row: IGitRootAttr): boolean =>
    _.isEmpty(currentValue) ? true : row.cloningStatus.status === currentValue
  );
}

function filterSelectIncludesHealthCheck(
  rows: IGitRootAttr[],
  currentValue: string
): IGitRootAttr[] {
  const isHealthCheckIncluded = currentValue === "true";

  return rows.filter((row: IGitRootAttr): boolean =>
    _.isEmpty(currentValue)
      ? true
      : row.includesHealthCheck === isHealthCheckIncluded
  );
}

const getRepositoryTourStepsText = (
  values: IFormValues
): JSX.Element | undefined => {
  if (values.credentials.id === "") {
    if (
      values.credentials.typeCredential === "USER" &&
      (values.credentials.user === "" || values.credentials.password === "")
    ) {
      return <li>{translate.t("tours.addGitRoot.rootCredentials.user")}</li>;
    }
    if (
      values.credentials.typeCredential === "TOKEN" &&
      (values.credentials.token === "" ||
        values.credentials.azureOrganization === "")
    ) {
      return <li>{translate.t("tours.addGitRoot.rootCredentials.token")}</li>;
    }
    if (
      values.credentials.typeCredential === "SSH" &&
      values.credentials.key === ""
    ) {
      return <li>{translate.t("tours.addGitRoot.rootCredentials.key")}</li>;
    }
    if (values.credentials.typeCredential === "") {
      return <li>{translate.t("tours.addGitRoot.rootCredentials.type")}</li>;
    }
  }

  return undefined;
};

const shouldHideRepositoryTourFooter = (values: IFormValues): boolean => {
  if (values.credentials.id === "") {
    if (
      values.credentials.typeCredential === "" ||
      values.credentials.name.length === 0
    ) {
      return true;
    }
    if (
      values.credentials.typeCredential === "SSH" &&
      values.credentials.key.length === 0
    ) {
      return true;
    }
    if (
      values.credentials.typeCredential === "TOKEN" &&
      (values.credentials.token.length === 0 ||
        values.credentials.azureOrganization.length === 0)
    ) {
      return true;
    }
    if (
      values.credentials.typeCredential === "USER" &&
      (values.credentials.user.length === 0 ||
        values.credentials.password.length === 0)
    ) {
      return true;
    }
  }

  return false;
};

export {
  filterSelectStatus,
  filterSelectIncludesHealthCheck,
  getRepositoryTourStepsText,
  gitModalSchema,
  handleCreationError,
  handleUpdateError,
  handleActivationError,
  handleSyncError,
  hasCheckedItem,
  shouldHideRepositoryTourFooter,
  useGitSubmit,
};

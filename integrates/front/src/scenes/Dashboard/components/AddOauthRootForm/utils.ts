/* eslint-disable react/forbid-prop-types */
import { useMutation } from "@apollo/client";
import _ from "lodash";
import { useCallback } from "react";
import type { BaseSchema, InferType } from "yup";
import { array, boolean, lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import { ADD_GIT_ROOT } from "./queries";
import type { IFormValues, IIntegrationRepository } from "./types";

import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

const validateValue = (regex: RegExp, value: string | undefined): boolean => {
  if (value === undefined) {
    return true;
  }

  return regex.test(value);
};

const validateStep = (values: IFormValues): boolean => {
  const filledEnvValues = values.branches.filter(
    (branch): boolean => !_.isEmpty(branch)
  );

  const filledBranchesValues = values.environments.filter((env): boolean => {
    const regex = /\S/u;

    return validateValue(regex, env);
  });

  if (
    filledEnvValues.length === values.urls.length &&
    filledBranchesValues.length === values.urls.length
  ) {
    return false;
  }

  return true;
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

  return true;
};

const validateHealthCheck = (values: IFormValues): boolean => {
  const { healthCheckConfirm, includesHealthCheck } = values;
  if (healthCheckConfirm === undefined) {
    return false;
  }

  return (
    (includesHealthCheck === "yes" &&
      healthCheckConfirm.includes("includeA")) ||
    (includesHealthCheck === "no" &&
      healthCheckConfirm.includes("rejectA") &&
      healthCheckConfirm.includes("rejectB") &&
      healthCheckConfirm.includes("rejectC"))
  );
};

const validateOauthFormSchema = (
  hasSquad: boolean,
  provider?: string
): InferType<TypedSchema> =>
  lazy(
    (values: IFormValues): BaseSchema =>
      object().shape({
        branches: array().of(
          string().required(translate.t("validations.required"))
        ),
        credentials: object({
          id: string().required(translate.t("validations.required")),
          isPat: boolean(),
          isToken: boolean(),
          name: string(),
          oauthType: string(),
          type: string(),
        }),
        environments: array().of(string()),
        gitignore: array().of(
          object({
            paths: array().of(
              string()
                .test(
                  "isRequired",
                  translate.t("validations.required"),
                  (value, options): boolean => {
                    const parent = options.path;
                    const index = parseInt(
                      parent.split("[")[1].split("]")[0],
                      10
                    );

                    return (
                      values.gitignore[index].paths.length === 1 ||
                      (values.gitignore[index].paths.length > 1 &&
                        !_.isNil(value))
                    );
                  }
                )
                .test(
                  "excludeFormat",
                  translate.t("validations.excludeFormat"),
                  (value, options): boolean => {
                    const parent = options.path;
                    const index = parseInt(
                      parent.split("[")[1].split("]")[0],
                      10
                    );
                    const repoUrl = values.urls[index];

                    return validateExcludeFormat(repoUrl, value);
                  }
                )
            ),
          })
        ),
        hasExclusions: string().required(translate.t("validations.required")),
        healthCheckConfirm: array()
          .of(string())
          .when("validateHealthCheck", {
            is: (): boolean => _.isUndefined(provider) || !hasSquad,
            otherwise: array()
              .of(string())
              .test(
                "isCheckedHealthCheck",
                translate.t("validations.required"),
                (): boolean => {
                  return validateHealthCheck(values);
                }
              ),
            then: array(),
          }),
        includesHealthCheck: string(),
      })
  );

const formatGitIgnore = (paths: string[]): string[] => {
  if (paths.length === 1 && _.isEmpty(paths[0])) {
    return [];
  }

  return paths;
};

function useRootSubmit(
  groupName: string,
  repositories: Record<string, IIntegrationRepository>,
  onUpdate?: () => void,
  closeModal?: () => void
): ({
  branches,
  credentials,
  environments,
  gitignore,
  includesHealthCheck,
  urls,
}: IFormValues) => void {
  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("Couldn't add root", error);
      });
    },
  });

  return useCallback(
    async ({
      branches,
      credentials,
      environments,
      gitignore,
      includesHealthCheck,
      urls,
    }: IFormValues): Promise<void> => {
      await Promise.all(
        urls.map(async (url, index): Promise<void> => {
          const repository = repositories[url];

          await addGitRoot({
            variables: {
              branch: branches[index].trim(),
              credentials: {
                id: credentials.id,
              },
              environment: environments[index],
              gitignore: formatGitIgnore(gitignore[index].paths),
              groupName,
              includesHealthCheck: includesHealthCheck === "yes",
              nickname: repository.name,
              url: url.trim(),
              useVpn: false,
            },
          });
        })
      );
      onUpdate?.();
      closeModal?.();
    },
    [addGitRoot, closeModal, groupName, onUpdate, repositories]
  );
}

export { useRootSubmit, validateOauthFormSchema, validateStep };

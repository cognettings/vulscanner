import { useLazyQuery, useMutation } from "@apollo/client";
import { useAbility } from "@casl/react";
import { Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { StringSchema } from "yup";
import { object, string } from "yup";

import { CloudName } from "./CloudName";
import { EnvironmentType } from "./EnvironmentType";
import { EnvironmentUrl } from "./EnvironmentUrl";
import type { IAddEnvironmentProps } from "./types";

import { Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";
import { authzPermissionsContext } from "context/authz/config";
import {
  ADD_ENVIRONMENT_SECRET,
  ADD_ENVIRONMENT_URL,
  GET_ROOT_ENVIRONMENT_URLS,
  VERIFY_AWS_CREDENTIALS,
  VERIFY_URL_STATUS,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IAddEnvironmentURL {
  addGitEnvironmentUrl: { urlId: string; success: boolean };
}

interface IVerifyAwsCredentials {
  verifyAwsCredentials: boolean;
}
interface IVerifyUrlStatus {
  verifyUrlStatus: boolean;
}

const AddEnvironment: React.FC<IAddEnvironmentProps> = ({
  groupName,
  rootId,
  closeFunction,
}: IAddEnvironmentProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions = useAbility(authzPermissionsContext);
  const canAddSecret: boolean = permissions.can(
    "api_mutations_add_git_environment_secret_mutate"
  );
  const forbiddenLinks =
    /^(?!.*(?:https:\/\/play\.google\.com\/store\/apps|https:\/\/apps\.apple\.com\/co\/app\/)).*$/u;
  const validations = object().shape({
    accessKeyId: string().when("cloudName", {
      is: "AWS",
      then: string().matches(/^[A-Z0-9]{20}$/u),
    }),
    cloudName: string().oneOf(["AZURE", "AWS", "GCP"]).nullable(),
    secretAccessKey: string().when("cloudName", {
      is: "AWS",
      then: string().matches(/^.{40}$/u),
    }),
    url: string()
      .when("urlType", {
        is: "URL",
        then: (schema): StringSchema => schema.url(t("validations.invalidUrl")),
      })
      .when("cloudName", {
        is: "AWS",
        then: string().matches(/^\d{12}$/u),
      })
      .when("urlType", {
        is: "URL",
        then: string().matches(
          forbiddenLinks,
          t("validations.invalidAppStoreUrl")
        ),
      })
      .required(t("validations.required")),
    urlType: string()
      .oneOf(["URL", "APK", "CLOUD"])
      .defined(t("validations.invalidUrlType")),
  });

  const [addEnvironmentUrl] = useMutation<IAddEnvironmentURL>(
    ADD_ENVIRONMENT_URL,
    {
      onCompleted: (): void => {
        msgSuccess(
          t("group.scope.git.addEnvironment.success"),
          t("group.scope.git.addEnvironment.successTittle")
        );
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't add environment url", error);
        });
      },
      refetchQueries: [
        { query: GET_ROOT_ENVIRONMENT_URLS, variables: { groupName, rootId } },
      ],
    }
  );

  const [addSecret] = useMutation(ADD_ENVIRONMENT_SECRET, {
    onCompleted: (): void => {
      msgSuccess(
        t("group.scope.git.repo.credentials.secrets.success"),
        t("group.scope.git.repo.credentials.secrets.successTitle")
      );
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't add secret", error);
      });
    },
  });

  const [verifyAwsCredentials] = useLazyQuery<IVerifyAwsCredentials>(
    VERIFY_AWS_CREDENTIALS,
    {
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Failed to complete credential validation", error);
        });
      },
    }
  );

  const [verifyUrlStatus] = useLazyQuery<IVerifyUrlStatus>(VERIFY_URL_STATUS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorUrlStatus"));
        Logger.error("Failed to get URL status", error);
      });
    },
  });

  const handleFormSubmit = useCallback(
    async ({
      accessKeyId,
      cloudName,
      secretAccessKey,
      url,
      urlType,
    }: {
      accessKeyId: string;
      cloudName: string | undefined;
      secretAccessKey: string;
      url: string;
      urlType: string;
    }): Promise<void> => {
      if (urlType === "URL") {
        const urlStatus = await verifyUrlStatus({
          variables: { url },
        });

        if (
          urlStatus.data?.verifyUrlStatus // eslint-disable-line @typescript-eslint/strict-boolean-expressions
        ) {
          await addEnvironmentUrl({
            variables: { cloudName, groupName, rootId, url, urlType },
          });
          closeFunction();
        } else {
          msgError(t("groupAlerts.errorUrlStatus"));
          await addEnvironmentUrl({
            variables: { cloudName, groupName, rootId, url, urlType },
          });
          closeFunction();
        }
      } else {
        const { data } = await addEnvironmentUrl({
          variables: { cloudName, groupName, rootId, url, urlType },
        });

        if (data) {
          const { urlId } = data.addGitEnvironmentUrl;
          const isCloud =
            cloudName === "AWS" && urlType === "CLOUD" && accessKeyId !== "";
          if (isCloud) {
            const verification = await verifyAwsCredentials({
              variables: { accessKeyId, secretAccessKey },
            });
            const keySecretName = "AWS_SECRET_ACCESS_KEY";
            const keyAccessIdName = "AWS_ACCESS_KEY_ID";
            const description = "";
            const addAwsCredentials = async (): Promise<void> => {
              await Promise.all([
                addSecret({
                  variables: {
                    description,
                    groupName,
                    key: keySecretName,
                    urlId,
                    value: secretAccessKey,
                  },
                }),
                addSecret({
                  variables: {
                    description,
                    groupName,
                    key: keyAccessIdName,
                    urlId,
                    value: accessKeyId,
                  },
                }),
              ]);
            };
            const addCloudSecrets = async (): Promise<void> => {
              if (
                verification.data &&
                !verification.data.verifyAwsCredentials
              ) {
                msgError(t("groupAlerts.errorAwsCredentials"));
                closeFunction();
              } else {
                await addAwsCredentials();
                closeFunction();
              }
            };
            await addCloudSecrets();
          }
        }
        closeFunction();
      }
    },
    [
      addEnvironmentUrl,
      groupName,
      rootId,
      addSecret,
      closeFunction,
      t,
      verifyAwsCredentials,
      verifyUrlStatus,
    ]
  );

  return (
    <Formik
      initialValues={{
        accessKeyId: "",
        cloudName: undefined,
        groupName,
        rootId,
        secretAccessKey: "",
        type: "",
        url: "",
        urlType: "",
      }}
      name={"addGitEnv"}
      onSubmit={handleFormSubmit}
      validationSchema={validations}
    >
      {({ isValid, dirty, isSubmitting }): JSX.Element => {
        return (
          <Form>
            <Row>
              <EnvironmentType />
              <CloudName />
            </Row>
            <Row>
              <EnvironmentUrl />
            </Row>
            <ModalConfirm
              disabled={!dirty || isSubmitting || !isValid || !canAddSecret}
              id={"add-env-url-confirm"}
              onCancel={closeFunction}
            />
          </Form>
        );
      }}
    </Formik>
  );
};

export { AddEnvironment };

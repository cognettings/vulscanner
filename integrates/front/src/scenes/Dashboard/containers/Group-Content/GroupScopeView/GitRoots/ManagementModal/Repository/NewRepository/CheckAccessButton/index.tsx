import { Buffer } from "buffer";

import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { useFormikContext } from "formik";
import type { GraphQLError } from "graphql";
import type { FC } from "react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { ICheckAccessProps } from "./types";

import { VALIDATE_GIT_ACCESS } from "../../../../../queries";
import type { IFormValues } from "../../../../../types";
import { submittableCredentials } from "../utils";
import { Button } from "components/Button";
import { Col } from "components/Layout";
import { Logger } from "utils/logger";

const CheckAccessButton: FC<ICheckAccessProps> = ({
  credExists,
  setIsGitAccessible,
  setShowGitAlert,
  setValidateGitMsg,
}): JSX.Element => {
  const { t } = useTranslation();
  const { validateField, values } = useFormikContext<IFormValues>();

  const [validateGitAccess] = useMutation(VALIDATE_GIT_ACCESS, {
    onCompleted: (): void => {
      setShowGitAlert(false);
      setIsGitAccessible(true);
      setValidateGitMsg({
        message: t("group.scope.git.repo.credentials.checkAccess.success"),
        type: "success",
      });
      validateField("credentials.token");
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      setShowGitAlert(false);
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Git repository was not accessible with given credentials":
            setValidateGitMsg({
              message: t("group.scope.git.errors.invalidGitCredentials"),
              type: "error",
            });
            break;
          case "Exception - Branch not found":
            setValidateGitMsg({
              message: t("group.scope.git.errors.invalidBranch"),
              type: "error",
            });
            break;
          default:
            setValidateGitMsg({
              message: t("groupAlerts.errorTextsad"),
              type: "error",
            });
            Logger.error("Couldn't activate root", error);
        }
      });
      setIsGitAccessible(false);
    },
  });

  const handleCheckAccessClick = useCallback((): void => {
    void validateGitAccess({
      variables: {
        branch: values.branch,
        credentials: {
          key: values.credentials.key
            ? Buffer.from(values.credentials.key).toString("base64")
            : undefined,
          name: values.credentials.name,
          password: values.credentials.password,
          token: values.credentials.token,
          type: values.credentials.type,
          user: values.credentials.user,
        },
        url: values.url,
      },
    });
  }, [validateGitAccess, values]);

  if (!submittableCredentials(credExists, values)) {
    return (
      <Col lg={100} md={100} sm={100}>
        <Button
          disp={"inline"}
          id={"checkAccessBtn"}
          onClick={handleCheckAccessClick}
          variant={"secondary"}
        >
          {t("group.scope.git.repo.credentials.checkAccess.text")}
        </Button>
      </Col>
    );
  }

  return <div />;
};

export { CheckAccessButton };

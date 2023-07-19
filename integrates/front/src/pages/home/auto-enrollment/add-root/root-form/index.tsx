import { Buffer } from "buffer";

import { useMutation } from "@apollo/client";
import { Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { CredentialsSection } from "./credentials-section";
import { Exclusions } from "./exclusions";
import { UrlSection } from "./url-section";

import { handleValidationError } from "../../helpers";
import type { IRootAttr, TEnrollPages } from "../../types";
import { submittableCredentials } from "../utils";
import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Container } from "components/Container";
import { Input } from "components/Input";
import { Hr, Row } from "components/Layout";
import { VALIDATE_GIT_ACCESS } from "pages/home/auto-enrollment/queries";
import type { ICheckGitAccessResult } from "pages/home/auto-enrollment/types";
import { msgSuccess } from "utils/notifications";

interface IAddRootFormProps {
  isSubmitting: boolean;
  rootMessages: {
    message: string;
    type: string;
  };
  setPage: React.Dispatch<React.SetStateAction<TEnrollPages>>;
  setProgress: React.Dispatch<React.SetStateAction<number>>;
  setRootMessages: React.Dispatch<
    React.SetStateAction<{
      message: string;
      type: string;
    }>
  >;
  setShowSubmitAlert: React.Dispatch<React.SetStateAction<boolean>>;
  showSubmitAlert: boolean;
}

export const RootForm: React.FC<IAddRootFormProps> = ({
  isSubmitting,
  rootMessages,
  setRootMessages,
  setPage,
  setProgress,
  setShowSubmitAlert,
  showSubmitAlert,
}: IAddRootFormProps): JSX.Element => {
  const { t } = useTranslation();
  const { dirty, values } = useFormikContext<IRootAttr>();

  const [validateGitAccess, { loading }] =
    useMutation<ICheckGitAccessResult>(VALIDATE_GIT_ACCESS);

  const [repoUrl, setRepoUrl] = useState("");
  const [accessChecked, setAccessChecked] = useState(false);

  const handleCheckAccessClick = useCallback((): void => {
    void validateGitAccess({
      onCompleted: (result): void => {
        if (result.validateGitAccess.success) {
          setProgress(100);
          setAccessChecked(true);
          msgSuccess(
            t("autoenrollment.messages.accessChecked.body"),
            t("autoenrollment.messages.accessChecked.title")
          );
        }
      },
      onError: (error): void => {
        setShowSubmitAlert(false);
        const { graphQLErrors } = error;
        handleValidationError(graphQLErrors, setRootMessages);
      },
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
  }, [
    setProgress,
    setRootMessages,
    setShowSubmitAlert,
    t,
    validateGitAccess,
    values,
  ]);

  const goBack = useCallback((): void => {
    setPage("fastTrack");
  }, [setPage]);

  return (
    <Form>
      <Row>
        <UrlSection accessChecked={accessChecked} setRepoUrl={setRepoUrl} />
      </Row>
      <Hr mv={16} />
      <Row>
        <CredentialsSection accessChecked={accessChecked} repoUrl={repoUrl} />
        <Input
          fw={"bold"}
          id={"env"}
          label={t("autoenrollment.environment.label")}
          name={"env"}
          placeholder={t("autoenrollment.environment.placeholder")}
          required={true}
          tooltip={t("Description of the application environment")}
        />
      </Row>
      <Row>
        <Exclusions />
      </Row>
      {!showSubmitAlert && rootMessages.message !== "" && (
        <Alert
          onTimeOut={setShowSubmitAlert}
          variant={rootMessages.type as IAlertProps["variant"]}
        >
          {rootMessages.message}
        </Alert>
      )}
      <Container margin={"8px 0 0 0"}>
        {accessChecked ? (
          <Button disabled={isSubmitting} type={"submit"} variant={"primary"}>
            {t("autoenrollment.submit")}
          </Button>
        ) : (
          <Container display={"flex"}>
            <Container margin={"0 8px 0 0"}>
              <Button onClick={goBack} variant={"primary"}>
                {t("autoenrollment.goBack")}
              </Button>
            </Container>
            <Button
              disabled={
                loading ||
                submittableCredentials(values) ||
                !dirty ||
                _.isEmpty(values.url)
              }
              onClick={handleCheckAccessClick}
              variant={"secondary"}
            >
              {t("autoenrollment.checkAccess")}
            </Button>
          </Container>
        )}
      </Container>
    </Form>
  );
};

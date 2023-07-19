/* eslint-disable complexity, react/forbid-component-props */

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { useAbility } from "@casl/react";
import type { FormikProps } from "formik";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { FC } from "react";
import React, { Fragment, useContext, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { CheckAccessButton } from "./CheckAccessButton";
import { CredentialsSection } from "./CredentialsSection";
import { Exclusions } from "./Exclusions";
import { HealthCheckSection } from "./HealthCheckSection";
import { RepositoryTour } from "./RepositoryTour";
import { UrlSection } from "./UrlSection";

import { GET_ORGANIZATION_CREDENTIALS } from "../../../../queries";
import type { ICredentialsAttr, IFormValues } from "../../../../types";
import { gitModalSchema } from "../../../helpers";
import type { IAlertProps } from "components/Alert";
import { Alert } from "components/Alert";
import { Input } from "components/Input";
import { Hr, Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { groupContext } from "scenes/Dashboard/group/context";
import type { IGroupContext } from "scenes/Dashboard/group/types";
import { Logger } from "utils/logger";

interface IRepositoryProps {
  initialValues: IFormValues;
  isEditing: boolean;
  manyRows: boolean | undefined;
  modalMessages: { message: string; type: string };
  onClose: () => void;
  onSubmit: (values: IFormValues) => Promise<void>;
  runTour: boolean;
  finishTour: () => void;
}

const NewRepository: FC<IRepositoryProps> = ({
  initialValues,
  isEditing,
  manyRows = false,
  modalMessages,
  onClose,
  onSubmit,
  runTour,
  finishTour,
}: IRepositoryProps): JSX.Element => {
  const { t } = useTranslation();
  const { organizationId }: IGroupContext = useContext(groupContext);
  const formRef = useRef<FormikProps<IFormValues>>(null);

  // GraphQL operations
  const { data: organizationCredentialsData } = useQuery<{
    organization: { credentials: ICredentialsAttr[] };
  }>(GET_ORGANIZATION_CREDENTIALS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load organization credentials", error);
      });
    },
    variables: {
      organizationId,
    },
  });

  const [isGitAccessible, setIsGitAccessible] = useState(true);
  const [repoUrl, setRepoUrl] = useState(initialValues.url);
  const [credExists, setCredExists] = useState(
    (!_.isNull(initialValues.credentials) &&
      initialValues.credentials.id !== "") ||
      manyRows
  );
  const [disabledCredsEdit, setDisabledCredsEdit] = useState(
    (!_.isNull(initialValues.credentials) &&
      initialValues.credentials.id !== "") ||
      manyRows
  );

  const attributes = useContext(authzGroupContext);
  const hasSquad = attributes.can("has_squad");

  const permissions = useAbility(authzPermissionsContext);
  const canAddExclusions = permissions.can("update_git_root_filter");

  const gitRootsPermissions = {
    canAddExclusions,
    hasSquad,
  };

  const [isCheckedHealthCheck, setIsCheckedHealthCheck] = useState(isEditing);

  const [showGitAlert, setShowGitAlert] = useState(false);
  const [showSubmitAlert, setShowSubmitAlert] = useState(false);

  const [validateGitMsg, setValidateGitMsg] = useState({
    message: "",
    type: "success",
  });

  const organizationCredentials = _.isUndefined(organizationCredentialsData)
    ? []
    : organizationCredentialsData.organization.credentials;

  const groupedExistingCreds =
    organizationCredentials.length > 0
      ? Object.fromEntries(
          organizationCredentials
            .filter((cred): boolean => {
              if (
                (cred.type === "SSH" && repoUrl.startsWith("ssh://")) ||
                (["HTTPS", "OAUTH"].includes(cred.type) &&
                  (repoUrl.startsWith("https://") ||
                    repoUrl.startsWith("http://")))
              )
                return true;

              return false;
            })
            .map((cred): [string, ICredentialsAttr] => [cred.id, cred])
        )
      : {};

  return (
    <Formik
      initialValues={initialValues}
      innerRef={formRef}
      name={"gitRoot"}
      onSubmit={onSubmit}
      validationSchema={gitModalSchema(
        isEditing,
        credExists,
        gitRootsPermissions,
        isCheckedHealthCheck,
        isGitAccessible
      )}
    >
      {({
        dirty,
        errors,
        isSubmitting,
        values,
      }): // eslint-disable-next-line
      JSX.Element => {
        if (isSubmitting) {
          setShowSubmitAlert(false);
        }

        return (
          <Fragment>
            <Form>
              <Row>
                <UrlSection
                  credExists={credExists}
                  form={formRef}
                  isEditing={isEditing}
                  manyRows={manyRows}
                  setCredExists={setCredExists}
                  setIsSameHealthCheck={setIsCheckedHealthCheck}
                  setRepoUrl={setRepoUrl}
                />
              </Row>
              <Hr mv={16} />
              <Row id={"git-root-add-credentials"}>
                <CredentialsSection
                  credExists={credExists}
                  disabledCredsEdit={disabledCredsEdit}
                  groupedExistingCreds={groupedExistingCreds}
                  isEditing={isEditing}
                  manyRows={manyRows}
                  repoUrl={repoUrl}
                  setCredExists={setCredExists}
                  setDisabledCredsEdit={setDisabledCredsEdit}
                  setShowGitAlert={setShowGitAlert}
                  showGitAlert={showGitAlert}
                  validateGitMsg={validateGitMsg}
                />
                <CheckAccessButton
                  credExists={credExists}
                  setIsGitAccessible={setIsGitAccessible}
                  setShowGitAlert={setShowGitAlert}
                  setValidateGitMsg={setValidateGitMsg}
                />
                <Input
                  fw={"bold"}
                  id={"git-root-add-env"}
                  label={t("group.scope.git.repo.environment.text")}
                  name={"environment"}
                  placeholder={t("group.scope.git.repo.environment.hint")}
                  required={true}
                  tooltip={t("group.scope.git.repo.environment.toolTip")}
                />
              </Row>
              <Exclusions isEditing={isEditing} manyRows={manyRows} />
              <HealthCheckSection
                form={formRef}
                isEditing={isEditing}
                isSameHealthCheck={isCheckedHealthCheck}
                setIsSameHealthCheck={setIsCheckedHealthCheck}
              />
              {!showSubmitAlert && modalMessages.message !== "" ? (
                <Alert
                  onTimeOut={setShowSubmitAlert}
                  variant={modalMessages.type as IAlertProps["variant"]}
                >
                  {modalMessages.message}
                </Alert>
              ) : undefined}
              <ModalConfirm
                disabled={
                  (!isGitAccessible && !values.useVpn) || !dirty || isSubmitting
                }
                id={"git-root-add-confirm"}
                onCancel={onClose}
              />
            </Form>
            {runTour ? (
              <RepositoryTour
                dirty={dirty}
                errors={errors}
                finishTour={finishTour}
                isGitAccessible={isGitAccessible}
                runTour={runTour}
                values={values}
              />
            ) : undefined}
          </Fragment>
        );
      }}
    </Formik>
  );
};

export { NewRepository };

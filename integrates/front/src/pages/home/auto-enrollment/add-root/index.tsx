import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { RootForm } from "./root-form";

import {
  handleEnrollmentCreateError,
  handleGroupCreateError,
  handleRootCreateError,
  handleValidationError,
  isRepeatedNickname,
  rootSchema,
} from "pages/home/auto-enrollment/helpers";
import {
  ADD_ENROLLMENT,
  ADD_GIT_ROOT,
  ADD_GROUP,
  ADD_ORGANIZATION,
} from "pages/home/auto-enrollment/queries";
import type {
  IAddGitRootResult,
  IAddGroupResult,
  IAddOrganizationResult,
  IAddRootProps,
  IRootAttr,
} from "pages/home/auto-enrollment/types";
import { getAddGitRootCredentials } from "pages/home/auto-enrollment/utils";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { generateWord } from "utils/wordGenerator";

const AddRoot: React.FC<IAddRootProps> = ({
  initialValues,
  mutationsState,
  organizationValues,
  rootMessages,
  setPage,
  setProgress,
  setRepositoryValues,
  setRootMessages,
}: IAddRootProps): JSX.Element => {
  const { t } = useTranslation();

  const [showSubmitAlert, setShowSubmitAlert] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMutation, setSuccessMutation] = useState(mutationsState);

  const [addOrganization] = useMutation<IAddOrganizationResult>(
    ADD_ORGANIZATION,
    {
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          if (message === "Access denied") {
            msgError(t("sidebar.newOrganization.modal.invalidName"));
          } else {
            Logger.error(
              "An error occurred creating new organization",
              message
            );
          }
        });
      },
    }
  );

  const [addGroup] = useMutation<IAddGroupResult>(ADD_GROUP, {
    onCompleted: (result): void => {
      if (result.addGroup.success) {
        msgSuccess(
          t("organization.tabs.groups.newGroup.success"),
          t("organization.tabs.groups.newGroup.titleSuccess")
        );
      }
    },
    onError: (error): void => {
      handleGroupCreateError(error.graphQLErrors, setRootMessages);
    },
  });

  const [addGitRoot] = useMutation<IAddGitRootResult>(ADD_GIT_ROOT, {
    onCompleted: (result): void => {
      if (result.addGitRoot.success) {
        msgSuccess(
          t("autoenrollment.messages.success.body"),
          t("autoenrollment.messages.success.title")
        );
      }
    },
    onError: (error): void => {
      handleRootCreateError(error.graphQLErrors, setRootMessages);
      setShowSubmitAlert(false);
    },
  });

  const [addEnrollment] = useMutation(ADD_ENROLLMENT, {
    onError: (error): void => {
      handleEnrollmentCreateError(error.graphQLErrors, setRootMessages);
    },
  });

  const validateAndSubmit = useCallback(
    // eslint-disable-next-line
    async (values: IRootAttr): Promise<void> => {
      // NOSONAR
      setIsSubmitting(true);
      const orgName = successMutation.organization
        ? organizationValues.organizationName
        : generateWord(Math.floor(Math.random() * 3) + 4);
      const groupName = successMutation.group
        ? organizationValues.groupName
        : orgName;
      async function addNewOrganization(): Promise<boolean> {
        try {
          mixpanel.track("AddOrganization");
          const response = await addOrganization({
            variables: {
              country: "TRIAL",
              name: orgName.toUpperCase(),
            },
          });
          const orgResult = response.data;

          return orgResult ? orgResult.addOrganization.success : false;
        } catch {
          return false;
        }
      }

      async function addNewGroup(): Promise<boolean> {
        try {
          mixpanel.track("AddGroup");
          const response = await addGroup({
            variables: {
              description: "Free trial group",
              groupName: groupName.toUpperCase(),
              hasMachine: true,
              hasSquad: false,
              language: "EN",
              organizationName: orgName.toUpperCase(),
              service: "WHITE",
              subscription: "CONTINUOUS",
            },
          });
          const groupResult = response.data;

          return groupResult ? groupResult.addGroup.success : false;
        } catch {
          return false;
        }
      }

      async function addNewRoot(): Promise<boolean> {
        try {
          mixpanel.track("AddGitRoot");
          const response = await addGitRoot({
            variables: {
              branch: values.branch.trim(),
              credentials: getAddGitRootCredentials(values.credentials),
              environment: values.env,
              gitignore: values.exclusions,
              groupName: groupName.toUpperCase(),
              includesHealthCheck: false,
              nickname: "",
              url: values.url.trim(),
              useVpn: false,
            },
          });
          const rootResult = response.data;
          const rootErrors = response.errors;
          const repeatedNickname = rootErrors
            ? isRepeatedNickname(rootErrors.toString())
            : false;

          return (
            (rootResult ? rootResult.addGitRoot.success : false) ||
            repeatedNickname
          );
        } catch {
          return false;
        }
      }

      async function createRoot(): Promise<void> {
        if (await addNewRoot()) {
          localStorage.clear();
          sessionStorage.clear();
          await addEnrollment();
          location.replace(
            `/orgs/${orgName.toLowerCase()}/groups/${groupName.toLowerCase()}/vulns`
          );
          setPage("standBy");
        } else {
          setPage("repository");
          setRootMessages({
            message: t("ainitialValuesutoenrollment.messages.error.repository"),
            type: "error",
          });
        }
      }

      async function createGroup(): Promise<void> {
        if (successMutation.group ? true : await addNewGroup()) {
          setSuccessMutation({ ...successMutation, group: true });
          await createRoot();
        } else {
          setRootMessages({
            message: t("autoenrollment.messages.error.group"),
            type: "error",
          });
        }
      }

      try {
        setRepositoryValues(values);
        if (successMutation.organization ? true : await addNewOrganization()) {
          setSuccessMutation({ ...successMutation, organization: true });
          await createGroup();
        } else {
          setRootMessages({
            message: t("autoenrollment.messages.error.organization"),
            type: "error",
          });
          mixpanel.track("AutoenrollSubmit", {
            addGroup: false,
            addOrg: false,
            addRoot: false,
            group: groupName.toLowerCase(),
            organization: orgName.toLowerCase(),
            url: values.url.trim(),
          });
        }
      } catch (error) {
        setIsSubmitting(false);
        setShowSubmitAlert(false);
        const { graphQLErrors } = error as ApolloError;
        handleValidationError(graphQLErrors, setRootMessages);
      }
    },
    [
      addEnrollment,
      addGitRoot,
      addGroup,
      addOrganization,
      organizationValues,
      setPage,
      setRootMessages,
      setRepositoryValues,
      successMutation,
      t,
    ]
  );

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={initialValues}
        name={"newRoot"}
        onSubmit={validateAndSubmit}
        validationSchema={rootSchema}
      >
        {(): JSX.Element => {
          return (
            <RootForm
              isSubmitting={isSubmitting}
              rootMessages={rootMessages}
              setPage={setPage}
              setProgress={setProgress}
              setRootMessages={setRootMessages}
              setShowSubmitAlert={setShowSubmitAlert}
              showSubmitAlert={showSubmitAlert}
            />
          );
        }}
      </Formik>
    </div>
  );
};

export { AddRoot };

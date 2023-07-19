import { Formik } from "formik";
import _ from "lodash";
import type { FC } from "react";
import React, { useContext, useState } from "react";
import { useParams } from "react-router-dom";

import { OauthForm } from "./OauthForm";
import type { IIntegrationRepository, IOauthRootFormProps } from "./types";
import { useRootSubmit, validateOauthFormSchema } from "./utils";

import { authzGroupContext } from "context/authz/config";

const AddOauthRootForm: FC<IOauthRootFormProps> = ({
  closeModal,
  initialValues = {
    allChecked: false,
    branches: [],
    cloningStatus: {
      message: "",
      status: "UNKNOWN",
    },
    credentials: {
      id: "",
      isPat: false,
      isToken: false,
      name: "",
      oauthType: "",
      type: "OAUTH",
    },
    environmentUrls: [],
    environments: [],
    gitEnvironmentUrls: [],
    gitignore: [{ paths: [] }],
    hasExclusions: "",
    healthCheckConfirm: [],
    id: "",
    includesHealthCheck: "",
    reposByName: "",
    secrets: [],
    state: "ACTIVE",
    urls: [],
  },
  trialGroupName,
  trialOrgId,
  onUpdate,
  provider,
  setIsCredentialSelected,
  setProgress,
}): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();

  const attributes = useContext(authzGroupContext);
  const hasSquad = attributes.can("has_squad");

  const [repos, setRepos] = useState<Record<string, IIntegrationRepository>>(
    {}
  );

  const handleSubmit = useRootSubmit(
    _.isUndefined(provider) ? trialGroupName ?? groupName : groupName,
    repos,
    onUpdate,
    closeModal
  );

  return (
    <Formik
      initialValues={initialValues}
      name={"gitAddOauthRoot"}
      onSubmit={handleSubmit}
      validationSchema={validateOauthFormSchema(hasSquad, provider)}
    >
      <OauthForm
        provider={provider}
        setIsCredentialSelected={setIsCredentialSelected}
        setProgress={setProgress}
        setRepos={setRepos}
        trialOrgId={trialOrgId}
      />
    </Formik>
  );
};

export { AddOauthRootForm };

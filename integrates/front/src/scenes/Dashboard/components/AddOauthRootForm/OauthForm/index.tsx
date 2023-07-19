import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Form, useFormikContext } from "formik";
import type { ArrayHelpers } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { FC } from "react";
import React, { useCallback, useContext, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams } from "react-router-dom";

import { BranchesSection } from "./BranchesSection";
import { CredentialSection } from "./CredentialSection";
import { ExclusionsSection } from "./ExclusionsSection";
import { HealthCheckSection } from "./HealthCheckSection";
import { RepositoriesSection } from "./RepositoriesSection";
import type { IOauthFormProps } from "./types";

import { GET_INTEGRATION_REPOSITORIES } from "../queries";
import type { IFormValues, IIntegrationRepository } from "../types";
import { validateStep } from "../utils";
import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Lottie } from "components/Icon";
import { StepLapse } from "components/StepLapse";
import { Text } from "components/Text";
import { redLoader, whiteLoader } from "resources";
import { groupContext } from "scenes/Dashboard/group/context";
import type { IGroupContext } from "scenes/Dashboard/group/types";
import { Logger } from "utils/logger";

const OauthForm: FC<IOauthFormProps> = ({
  trialOrgId,
  provider,
  setIsCredentialSelected,
  setProgress,
  setRepos,
}): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();
  const { organizationName } = useParams<{ organizationName: string }>();
  const { organizationId }: IGroupContext = useContext(groupContext);
  const { isSubmitting, isValid, values } = useFormikContext<IFormValues>();

  const [credentialStep, setCredentialStep] = useState(true);
  const [noRepos, setNoRepos] = useState(false);
  const [repositories, setRepositories] = useState<
    Record<string, IIntegrationRepository>
  >({});

  const branchesArrayHelpersRef = useRef<ArrayHelpers | null>(null);
  const exclusionsArrayHelpersRef = useRef<ArrayHelpers | null>(null);
  const envsArrayHelpersRef = useRef<ArrayHelpers | null>(null);

  const onMoveToCredentials = useCallback((): void => {
    push(`/orgs/${organizationName}/credentials`);
  }, [organizationName, push]);

  const { loading } = useQuery<{
    organization: {
      credential: { integrationRepositories: IIntegrationRepository[] };
    };
  }>(GET_INTEGRATION_REPOSITORIES, {
    onCompleted: (data): void => {
      const { credential } = data.organization;
      setRepositories(
        credential.integrationRepositories.length > 0
          ? Object.fromEntries(
              credential.integrationRepositories.map(
                (repo): [string, IIntegrationRepository] => [repo.url, repo]
              )
            )
          : {}
      );
      setRepos(
        credential.integrationRepositories.length > 0
          ? Object.fromEntries(
              credential.integrationRepositories.map(
                (repo): [string, IIntegrationRepository] => [repo.url, repo]
              )
            )
          : {}
      );
      if (_.isUndefined(provider)) {
        setCredentialStep(false);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load integration repositories", error);
      });
    },
    skip: values.credentials.id === "",
    variables: {
      credId: values.credentials.id,
      organizationId: provider ? organizationId : trialOrgId,
    },
  });

  const steps = [
    {
      content: (
        <RepositoriesSection
          branchesArrayHelpersRef={branchesArrayHelpersRef}
          credentialName={values.credentials.name}
          envsArrayHelpersRef={envsArrayHelpersRef}
          exclusionsArrayHelpersRef={exclusionsArrayHelpersRef}
          repositories={repositories}
        />
      ),
      isDisabledNext: values.urls.length === 0,
      nextAction: setProgress
        ? (): void => {
            setProgress(70);
          }
        : undefined,
      title: t("components.oauthRootForm.steps.s1.title"),
    },
    {
      content: (
        <BranchesSection
          branchesArrayHelpersRef={branchesArrayHelpersRef}
          envsArrayHelpersRef={envsArrayHelpersRef}
          repositories={repositories}
        />
      ),
      isDisabledNext: validateStep(values),
      nextAction: setProgress
        ? (): void => {
            setProgress(90);
          }
        : undefined,
      previousAction: setProgress
        ? (): void => {
            setProgress(50);
          }
        : undefined,
      title: t("components.oauthRootForm.steps.s2.title"),
    },
    {
      content: (
        <Container
          bgColor={"#FFF"}
          border={"1px solid #F4F4F6"}
          br={"4px"}
          margin={"10px 0 0 0"}
          pb={"24px"}
          pl={"24px"}
          pr={"24px"}
          pt={"24px"}
          scroll={"none"}
        >
          <ExclusionsSection
            exclusionsArrayHelpersRef={exclusionsArrayHelpersRef}
            repositories={repositories}
          />
          <HealthCheckSection />
        </Container>
      ),
      isDisabledPrevious: isSubmitting,
      title: _.isUndefined(provider)
        ? t("components.oauthRootForm.steps.s3.titleEnrollment")
        : t("components.oauthRootForm.steps.s3.title"),
    },
  ];

  const nextStep = useCallback((): void => {
    if (_.isEmpty(repositories)) {
      setNoRepos(true);
    } else {
      if (setIsCredentialSelected) {
        setIsCredentialSelected(true);
      }
      setCredentialStep(false);
    }
  }, [repositories, setIsCredentialSelected]);

  const finalClick = useCallback((): void => {
    if (!_.isUndefined(setProgress)) {
      setProgress(100);
    }
  }, [setProgress]);

  return (
    <Form>
      {credentialStep ? (
        noRepos ? (
          <Container align={"center"} display={"flex"}>
            <Text disp={"inline-block"}>
              {t("components.oauthRootForm.steps.noRoots.text")}
            </Text>
            <ExternalLink onClick={onMoveToCredentials}>
              {t("components.oauthRootForm.steps.noRoots.link")}
            </ExternalLink>
          </Container>
        ) : (
          <Container scroll={"none"}>
            <Container
              display={_.isUndefined(provider) ? "none" : "block"}
              scroll={"none"}
            >
              <CredentialSection provider={provider} trialOrgId={trialOrgId} />
              <Container margin={"14px 0 0 0"}>
                <Button
                  disabled={values.credentials.id === "" || loading}
                  onClick={nextStep}
                  variant={"primary"}
                >
                  {loading ? (
                    <Container
                      align={"center"}
                      display={"flex"}
                      justify={"center"}
                      scroll={"none"}
                    >
                      <Container margin={"0 4px 0 0"} scroll={"none"}>
                        <Lottie animationData={whiteLoader} />
                      </Container>
                      {t("components.oauthRootForm.credentialSection.loading")}
                    </Container>
                  ) : (
                    t("components.oauthRootForm.credentialSection.continue")
                  )}
                </Button>
              </Container>
            </Container>
            {_.isUndefined(provider) ? (
              <Container
                align={"center"}
                display={"flex"}
                justify={"center"}
                scroll={"none"}
              >
                <Container display={"flex"} scroll={"none"}>
                  <Container margin={"0 4px 0 0"} scroll={"none"}>
                    <Lottie animationData={redLoader} />
                  </Container>
                  <Text>
                    {t(
                      "components.oauthRootForm.credentialSection.trialLoading"
                    )}
                  </Text>
                </Container>
              </Container>
            ) : undefined}
          </Container>
        )
      ) : (
        <Container width={"1200px"}>
          <StepLapse
            finalButtonText={
              provider
                ? t("components.oauthRootForm.onSubmit1")
                : t("components.oauthRootForm.onSubmit2")
            }
            finalButtonType={"submit"}
            finalClick={finalClick}
            isDisabledFinalButton={!isValid || isSubmitting}
            steps={steps}
          />
        </Container>
      )}
    </Form>
  );
};

export { OauthForm };

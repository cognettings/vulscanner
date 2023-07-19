// https://github.com/mixpanel/mixpanel-js/issues/321
/* eslint-disable import/no-named-default*/
import { Form, Formik } from "formik";
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useEffect } from "react";
import { useTranslation } from "react-i18next";

import { Label, ManualLink, Radio, RepoButton } from "./styles";
import type { IFastTrackDesktop, IFormValues } from "./types";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Text } from "components/Text";
import {
  azureLogoBig,
  bitbucketLogoBig,
  githubLogoBig,
  gitlabLogoBig,
} from "resources/index";

const FastTrackDesktop: React.FC<IFastTrackDesktop> = ({
  setPage,
}): JSX.Element => {
  const { t } = useTranslation();

  useEffect((): void => {
    mixpanel.track("FastTrack");
  }, []);

  const repositories = [
    {
      icon: gitlabLogoBig,
      id: "gitlab",
      text: t("components.repositoriesDropdown.gitLabButton.text"),
    },
    {
      icon: githubLogoBig,
      id: "github",
      text: t("components.repositoriesDropdown.gitHubButton.text"),
    },
    {
      icon: azureLogoBig,
      id: "azure",
      text: t("components.repositoriesDropdown.azureButton.text"),
    },
    {
      icon: bitbucketLogoBig,
      id: "bitbucket",
      text: t("components.repositoriesDropdown.bitbucketButton.text"),
    },
  ];

  function useSubmit(): ({ provider }: IFormValues) => void {
    return useCallback(({ provider }: IFormValues): void => {
      mixpanel.track("FastTrackOAuth", { provider });
      window.location.assign(`/d${provider}?fast_track=true`);
    }, []);
  }

  const onManualClick = useCallback((): void => {
    setPage("repository");
  }, [setPage]);

  const onSubmit = useSubmit();

  return (
    <Container display={"flex"} justify={"center"} width={"100%"} wrap={"wrap"}>
      <Formik
        initialValues={{
          provider: "",
        }}
        onSubmit={onSubmit}
      >
        {({ dirty, values }): JSX.Element => (
          <Form>
            <Container
              display={"flex"}
              justify={"center"}
              maxWidth={"655px"}
              width={"100%"}
              wrap={"wrap"}
            >
              {repositories.map(
                ({ icon, id, text }): JSX.Element | undefined => {
                  return (
                    <RepoButton key={id}>
                      <Label>
                        <Radio name={"provider"} type={"radio"} value={id} />
                        <Container
                          bgImage={`url(${icon})`}
                          bgImagePos={"100% 100%"}
                          height={id === "bitbucket" ? "30px" : "48px"}
                          margin={"0 20px 0 0;"}
                          width={id === "bitbucket" ? "32px" : "48px"}
                        />
                        <Text disp={"inline"} fw={9} size={"medium"}>
                          {text}
                        </Text>
                      </Label>
                    </RepoButton>
                  );
                }
              )}
              <Container
                display={"flex"}
                justify={"center"}
                margin={"25px 0 25px 0"}
                width={"100%"}
              >
                <Container>
                  <Text disp={"inline"}>
                    {t("autoenrollment.fastTrackDesktop.manual.text")}
                  </Text>
                  <ManualLink onClick={onManualClick}>
                    {t("autoenrollment.fastTrackDesktop.manual.button")}
                  </ManualLink>
                </Container>
              </Container>
              <Button disabled={!dirty} type={"submit"} variant={"primary"}>
                {`Authenticate ${values.provider
                  .charAt(0)
                  .toUpperCase()}${values.provider.slice(1)}`}
              </Button>
            </Container>
          </Form>
        )}
      </Formik>
    </Container>
  );
};

export { FastTrackDesktop };

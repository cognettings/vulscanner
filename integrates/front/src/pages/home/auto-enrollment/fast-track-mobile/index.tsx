// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useEffect } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import { useWindowSize } from "hooks";
import {
  azureIcon,
  bitBucketIcon,
  gitHubIcon,
  gitLabIcon,
} from "resources/index";

const FastTrackMobile: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { height } = useWindowSize();

  useEffect((): void => {
    mixpanel.track("FastTrack");
  }, []);

  const repositories = [
    {
      icon: gitLabIcon,
      id: "gitlab",
      text: t("components.repositoriesDropdown.gitLabButton.text"),
    },
    {
      icon: gitHubIcon,
      id: "github",
      text: t("components.repositoriesDropdown.gitHubButton.text"),
    },
    {
      icon: azureIcon,
      id: "azure",
      text: t("components.repositoriesDropdown.azureButton.text"),
    },
    {
      icon: bitBucketIcon,
      id: "bitbucket",
      text: t("components.repositoriesDropdown.bitbucketButton.text"),
    },
  ];

  const handleClick = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>): void => {
      const provider = (event.currentTarget as HTMLButtonElement).id;
      mixpanel.track("FastTrackOAuth", { provider });
      window.location.assign(`/d${provider}?fast_track=true`);
    },
    []
  );

  return (
    <Container display={"flex"} width={"100%"} wrap={"wrap"}>
      <Container
        align={"center"}
        display={"flex"}
        height={`${height}px`}
        justify={"center"}
        width={"100%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          display={"flex"}
          heightMd={"550px"}
          justify={"center"}
          widthMd={"380px"}
          wrap={"wrap"}
        >
          <Text bright={0} mt={5} ta={"center"} tone={"red"}>
            {t("autoenrollment.fastTrackMobile.begin")}
          </Text>
          <Text fw={7} mb={2} ml={5} mr={5} size={"big"} ta={"center"}>
            {t("autoenrollment.fastTrackMobile.title")}
          </Text>
          <Text mb={4} ml={4} mr={4} ta={"center"}>
            {t("autoenrollment.fastTrackMobile.subtitle")}
            <ExternalLink
              href={"https://docs.fluidattacks.com/about/security/"}
            >
              {t("autoenrollment.fastTrackMobile.principles")}
            </ExternalLink>
          </Text>
          {repositories.map(({ icon, id, text }): JSX.Element | undefined => {
            return (
              <Button
                id={id}
                key={id}
                onClick={handleClick}
                size={"lg"}
                variant={"input"}
              >
                <Container
                  align={"center"}
                  display={"flex"}
                  justify={"center"}
                  wrap={"wrap"}
                >
                  <Container
                    bgImage={`url(${icon})`}
                    bgImagePos={"100% 100%"}
                    height={"24px"}
                    width={"24px"}
                  />
                  <Container minWidth={"20px"} />
                  <Container pt={"2px"} width={"200px"}>
                    <Text bright={9} fontSize={"18px"}>
                      {`Continue with ${text}`}
                    </Text>
                  </Container>
                </Container>
              </Button>
            );
          })}
        </Container>
      </Container>
    </Container>
  );
};

export { FastTrackMobile };

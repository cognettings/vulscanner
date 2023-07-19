import { faCircleCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import type { IBenefits } from "../types";
import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import {
  loginBitBucketLogo,
  loginGoogleLogo,
  loginMicrosoftLogo,
  signUpLogo,
  signupBig,
} from "resources";

export const BigScreenSignUp: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const benefits: IBenefits[] = [
    {
      data: "Automatic SAST, DAST, SCA and CSPM",
      icon: faCircleCheck,
      id: 0,
    },
    {
      data: "Continuous vulnerability scanning",
      icon: faCircleCheck,
      id: 1,
    },
    {
      data: "No credit card required",
      icon: faCircleCheck,
      id: 2,
    },
  ];

  // Event handlers
  const handleBitbucketLogin: () => void = useCallback((): void => {
    mixpanel.track("Signup Bitbucket");
    window.location.assign("/dblogin");
  }, []);
  const handleGoogleLogin: () => void = useCallback((): void => {
    mixpanel.track("Signup Google");
    window.location.assign("/dglogin");
  }, []);
  const handleMicrosoftLogin: () => void = useCallback((): void => {
    mixpanel.track("Signup Azure");
    window.location.assign("/dalogin");
  }, []);

  return (
    <Container display={"flex"} height={"100%"} width={"100%"} wrap={"wrap"}>
      <Container
        display={"flex"}
        height={"100%"}
        maxHeight={"100%"}
        scroll={"none"}
        width={"50%"}
        widthMd={"53%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          bgColor={"#2e2e38"}
          display={"flex"}
          height={"100%"}
          justify={"center"}
          scroll={"none"}
          width={"105%"}
          wrap={"wrap"}
        >
          <Container
            align={"center"}
            display={"flex"}
            height={"50%"}
            justify={"center"}
            pl={"15%"}
            widthMd={"85%"}
          >
            <Container display={"flex"} wrap={"wrap"}>
              <Container
                letterSpacing={"2px"}
                maxWidth={"696px"}
                pb={"16px"}
                pt={"24px"}
                width={"100%"}
              >
                <Text bright={0} fontSize={"32px"} fw={9} tone={"light"}>
                  {t("signup.title")}
                </Text>
              </Container>
              <Container
                letterSpacing={"normal"}
                lineHeight={"23px"}
                maxWidth={"568px"}
                pb={"5px"}
                pt={"5px"}
                width={"100%"}
                widthMd={"85%"}
              >
                <Text bright={6} fontSize={"16px"} tone={"light"}>
                  {t("signup.subtitle")}
                </Text>
              </Container>
              {benefits.map(
                (benefit: IBenefits): JSX.Element => (
                  <Container
                    display={"flex"}
                    key={benefit.id}
                    pt={"16px"}
                    width={"100%"}
                    wrap={"wrap"}
                  >
                    <Container letterSpacing={"1.2px"} pr={"16px"} pt={"5px"}>
                      <FontAwesomeIcon color={"#b0b0bf"} icon={benefit.icon} />
                    </Container>
                    <Container
                      lineHeight={"21px"}
                      maxWidth={"522px"}
                      pt={"5px"}
                      widthMd={"75%"}
                    >
                      <Text bright={6} fontSize={"16px"} tone={"light"}>
                        {benefit.data}
                      </Text>
                    </Container>
                  </Container>
                )
              )}
              <Container
                letterSpacing={"normal"}
                lineHeight={"23px"}
                maxWidth={"668px"}
                pt={"30px"}
                width={"100%"}
                widthMd={"85%"}
              >
                <Text bright={0} fontSize={"16px"} fw={7} tone={"light"}>
                  {t("signup.subtitle2")}
                </Text>
              </Container>
            </Container>
          </Container>
          <Container
            display={"flex"}
            height={"50%"}
            justify={"end"}
            width={"100%"}
          >
            <Container
              bgImage={`url(${signupBig})`}
              bgImagePos={"cover"}
              height={"100%"}
              width={"90%"}
            />
          </Container>
        </Container>
      </Container>
      <Container
        align={"center"}
        bgColor={"#ffffff"}
        display={"flex"}
        height={"100%"}
        justify={"center"}
        width={"50%"}
        widthMd={"47%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          display={"flex"}
          height={"600px"}
          heightMd={"643px"}
          justify={"center"}
          scroll={"none"}
          width={"473px"}
          widthMd={"350px"}
          wrap={"wrap"}
        >
          <Container
            bgImage={`url(${signUpLogo})`}
            bgImagePos={"100% 100%"}
            height={"109px"}
            width={"237px"}
          />
          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            pt={"30px"}
            ptMd={"10px"}
            width={"413px"}
            wrap={"wrap"}
          >
            <Container>
              <Text
                bright={3}
                fontSize={"24px"}
                fw={9}
                ta={"center"}
                tone={"dark"}
              >
                {t("signup.journeyText")}
              </Text>
            </Container>
          </Container>
          <Container align={"center"} justify={"center"} widthMd={"350px"}>
            <Container pt={"20px"} width={"100%"}>
              <Button onClick={handleGoogleLogin} size={"lg"} variant={"input"}>
                <Container
                  align={"center"}
                  boxSizing={"border-box"}
                  display={"flex"}
                  height={"32px"}
                  justify={"center"}
                  minWidth={"310px"}
                  scroll={"none"}
                  width={"435px"}
                  widthMd={"100%"}
                  wrap={"wrap"}
                >
                  <Container
                    bgImage={`url(${loginGoogleLogo})`}
                    bgImagePos={"100% 100%"}
                    height={"24px"}
                    width={"24px"}
                  />
                  <Container minWidth={"20px"} />
                  <Container>
                    <Text bright={9} fontSize={"18px"}>
                      {"Continue with Google"}
                    </Text>
                  </Container>
                </Container>
              </Button>
            </Container>
            <Container pt={"16px"} width={"100%"}>
              <Button
                onClick={handleMicrosoftLogin}
                size={"lg"}
                variant={"input"}
              >
                <Container
                  align={"center"}
                  boxSizing={"border-box"}
                  display={"flex"}
                  height={"32px"}
                  justify={"center"}
                  minWidth={"310px"}
                  scroll={"none"}
                  width={"435px"}
                  widthMd={"100%"}
                  wrap={"wrap"}
                >
                  <Container width={"28px"} widthMd={"0px"} />
                  <Container
                    bgImage={`url(${loginMicrosoftLogo})`}
                    bgImagePos={"100% 100%"}
                    height={"24px"}
                    width={"24px"}
                  />
                  <Container minWidth={"20px"} />
                  <Container>
                    <Text bright={9} fontSize={"18px"}>
                      {"Continue with Microsoft"}
                    </Text>
                  </Container>
                </Container>
              </Button>
            </Container>
            <Container pt={"16px"} width={"100%"}>
              <Button
                onClick={handleBitbucketLogin}
                size={"lg"}
                variant={"input"}
              >
                <Container
                  align={"center"}
                  boxSizing={"border-box"}
                  display={"flex"}
                  height={"32px"}
                  justify={"center"}
                  minWidth={"310px"}
                  scroll={"none"}
                  width={"435px"}
                  widthMd={"100%"}
                  wrap={"wrap"}
                >
                  <Container width={"28px"} widthMd={"0px"} />
                  <Container
                    bgImage={`url(${loginBitBucketLogo})`}
                    bgImagePos={"100% 100%"}
                    height={"24px"}
                    width={"24px"}
                  />
                  <Container minWidth={"20px"} />
                  <Container>
                    <Text bright={9} fontSize={"18px"}>
                      {"Continue with Bitbucket"}
                    </Text>
                  </Container>
                </Container>
              </Button>
            </Container>
          </Container>

          <Container
            align={"center"}
            display={"flex"}
            pb={"10px"}
            pbMd={"15px"}
            pt={"22px"}
            ptMd={"10px"}
            wrap={"wrap"}
          >
            <Container width={"190px"}>
              <Text bright={7} fontSize={"16px"} tone={"dark"}>
                {"Already have an account?"}
                &nbsp;
              </Text>
            </Container>
            <Container borderBottom={"1.5px solid #bf0b1a"}>
              <Text fontSize={"14px"}>
                <Link to={"/"}>{"Log in"}</Link>
              </Text>
            </Container>
          </Container>
          <Container
            borderTop={"1.5px solid #b0b0bf"}
            display={"flex"}
            width={"473px"}
            wrap={"wrap"}
          />
          <Container
            align={"center"}
            display={"flex"}
            maxWidth={"473px"}
            textAlign={"center"}
            wrap={"wrap"}
          >
            <Text
              bright={9}
              disp={"inline"}
              fontSize={"16px"}
              ta={"center"}
              tone={"light"}
            >
              <ExternalLink href={"https://fluidattacks.com/terms-use/"}>
                {"Terms of use"}
              </ExternalLink>
              {"and"}
              <ExternalLink href={"https://fluidattacks.com/privacy/"}>
                {"Privacy policy"}
              </ExternalLink>
            </Text>
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

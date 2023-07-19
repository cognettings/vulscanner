import { faCircleCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import { useWindowSize } from "hooks";
import type { IBenefits } from "pages/sign-up/types";
import {
  loginBitBucketLogo,
  loginGoogleLogo,
  loginLogo,
  loginMicrosoftLogo,
  signupBig,
} from "resources";

export const SmallScreenSignUp: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { height } = useWindowSize();

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
    <Container display={"flex"} width={"100%"} wrap={"wrap"}>
      <Container
        align={"center"}
        bgColor={"#ffffff"}
        display={"flex"}
        height={`${height}px`}
        justify={"center"}
        width={"100%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          display={"flex"}
          heightMd={"643px"}
          justify={"center"}
          maxWidth={"390px"}
          width={"100%"}
          wrap={"wrap"}
        >
          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            width={"390px"}
            wrap={"wrap"}
          >
            <Container
              bgImage={`url(${loginLogo})`}
              bgImagePos={"100% 100%"}
              height={"109px"}
              width={"237px"}
            />
          </Container>

          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            pt={"15px"}
            width={"600px"}
            wrap={"wrap"}
          >
            <Container id={"login-auth"} maxWidth={"250px"}>
              <Text fontSize={"24px"} fw={9} ta={"center"} tone={"dark"}>
                {t("signup.journeyText")}
              </Text>
            </Container>
          </Container>
          <Container pt={"32px"} width={"80%"}>
            <Button onClick={handleGoogleLogin} size={"lg"} variant={"input"}>
              <Container
                align={"center"}
                boxSizing={"border-box"}
                display={"flex"}
                height={"32px"}
                justify={"center"}
                maxWidth={"435px"}
                minWidth={"250px"}
                scroll={"none"}
                wrap={"wrap"}
              >
                <Container width={"40px"} widthMd={"0px"} />
                <Container
                  bgImage={`url(${loginGoogleLogo})`}
                  bgImagePos={"100% 100%"}
                  height={"24px"}
                  width={"24px"}
                />
                <Container minWidth={"20px"} />
                <Container pt={"2px"} width={"200px"}>
                  <Text bright={9} fontSize={"18px"} ta={"center"}>
                    {"Continue with Google"}
                  </Text>
                </Container>
              </Container>
            </Button>
          </Container>
          <Container pt={"16px"} width={"80%"}>
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
                maxWidth={"435px"}
                minWidth={"250px"}
                scroll={"none"}
                wrap={"wrap"}
              >
                <Container width={"40px"} widthMd={"0px"} />
                <Container
                  bgImage={`url(${loginMicrosoftLogo})`}
                  bgImagePos={"100% 100%"}
                  height={"24px"}
                  pl={"20px"}
                  width={"24px"}
                />
                <Container minWidth={"20px"} />
                <Container pt={"2px"} width={"200px"}>
                  <Text bright={9} fontSize={"18px"} ta={"center"}>
                    {"Continue with Microsoft"}
                  </Text>
                </Container>
              </Container>
            </Button>
          </Container>
          <Container pt={"16px"} width={"80%"}>
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
                maxWidth={"435px"}
                minWidth={"250px"}
                scroll={"none"}
                wrap={"wrap"}
              >
                <Container width={"40px"} widthMd={"0px"} />
                <Container
                  bgImage={`url(${loginBitBucketLogo})`}
                  bgImagePos={"100% 100%"}
                  height={"24px"}
                  pl={"20px"}
                  width={"24px"}
                />
                <Container minWidth={"20px"} />
                <Container pt={"2px"} width={"200px"}>
                  <Text bright={9} fontSize={"18px"} ta={"center"}>
                    {"Continue with Bitbucket"}
                  </Text>
                </Container>
              </Container>
            </Button>
          </Container>
          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            pb={"60px"}
            pbMd={"10px"}
            pt={"20px"}
            width={"350px"}
            wrap={"wrap"}
          >
            <Container width={"200px"}>
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
            align={"center"}
            borderTop={"1.5px solid #b0b0bf"}
            display={"inline"}
            justify={"center"}
            pt={"10px"}
            width={"350px"}
          >
            <Text bright={9} fontSize={"14px"} ta={"center"} tone={"light"}>
              <ExternalLink href={"https://fluidattacks.com/terms-use/"}>
                {"Terms of use"}
              </ExternalLink>
              {"and"}
              <ExternalLink href={"https://fluidattacks.com/privacy/"}>
                {"Privacy policy"}
              </ExternalLink>
            </Text>
          </Container>
          <Container
            align={"center"}
            display={"flex"}
            justify={"center"}
            width={"350px"}
          />
        </Container>
      </Container>
      <Container
        display={"flex"}
        height={"100%"}
        maxHeight={"100%"}
        scroll={"none"}
        width={"100%"}
        wrap={"wrap"}
      >
        <Container
          align={"end"}
          bgColor={"#2e2e38"}
          display={"flex"}
          height={`${height}px`}
          justify={"center"}
          width={"100%"}
          wrap={"wrap"}
        >
          <Container
            align={"center"}
            display={"flex"}
            height={"50%"}
            justify={"center"}
            pl={"20px"}
            plMd={"0px"}
            prMd={"0px"}
            pt={"20px"}
            widthMd={"85%"}
          >
            <Container>
              <Container
                letterSpacing={"2px"}
                maxWidth={"696px"}
                pb={"16px"}
                width={"100%"}
              >
                <Text bright={0} fontSize={"28px"} fw={9} tone={"light"}>
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
                    pt={"5px"}
                    wrap={"wrap"}
                  >
                    <Container letterSpacing={"1.2px"} pr={"16px"} pt={"12px"}>
                      <FontAwesomeIcon color={"#b0b0bf"} icon={benefit.icon} />
                    </Container>
                    <Container
                      lineHeight={"21px"}
                      maxWidth={"522px"}
                      pt={"12px"}
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
              bgImagePos={"center"}
              height={"100%"}
              width={"90%"}
            />
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

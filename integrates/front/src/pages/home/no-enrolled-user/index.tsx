import { faCircleCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import type { IBenefits } from "./types";

import { Autoenrollment } from "../auto-enrollment";
import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import { signUpLogo } from "resources";

interface INoEnrolledUserProps {
  email: string;
}

const NoEnrolledUser: React.FC<INoEnrolledUserProps> = ({
  email,
}): JSX.Element => {
  const { t } = useTranslation();
  const [enrollmentVisible, setEnrollmentVisible] = useState(false);

  const showEnrollment = useCallback((): void => {
    setEnrollmentVisible(true);
  }, []);

  const benefits: IBenefits[] = [
    {
      data: "Automatic SAST, DAST and SCA",
      icon: faCircleCheck,
      id: 0,
    },
    {
      data: "Continuous vulnerability reporting",
      icon: faCircleCheck,
      id: 1,
    },
    {
      data: `Vulnerability management
        (+  GraphQL API)`,
      icon: faCircleCheck,
      id: 2,
    },
    {
      data: "Control and accelerate vulnerability remediation",
      icon: faCircleCheck,
      id: 3,
    },
    {
      data: "Integration with your CI/CD for stronger control",
      icon: faCircleCheck,
      id: 4,
    },
  ];

  if (enrollmentVisible) {
    return <Autoenrollment />;
  }

  return (
    <Container
      align={"center"}
      bgColor={"#e9e9ed"}
      display={"flex"}
      height={"100%"}
      justify={"center"}
      width={"100%"}
      wrap={"wrap"}
    >
      <Container
        display={"flex"}
        height={"741px"}
        width={"1136px"}
        wrap={"wrap"}
      >
        <Container height={"auto"} pl={"20px"} width={"50%"}>
          <Container
            bgImage={`url(${signUpLogo})`}
            bgImagePos={"100% 100%"}
            height={"109px"}
            width={"237px"}
          />
          <Container pt={"110px"}>
            <Text bright={3} fontSize={"48px"} fw={9} tone={"dark"}>
              {t("login.noEnrolledUser.title")}
            </Text>
          </Container>
          <Container pt={"24px"}>
            <Text bright={7} disp={"inline"} fontSize={"20px"} tone={"dark"}>
              {t("login.noEnrolledUser.subtitle1")}
            </Text>
            <Text
              bright={7}
              disp={"inline"}
              fontSize={"20px"}
              fw={9}
              tone={"dark"}
            >
              {email}
            </Text>
            <Text bright={7} disp={"inline"} fontSize={"20px"} tone={"dark"}>
              {t("login.noEnrolledUser.subtitle2")}
            </Text>
            <Text
              bright={7}
              disp={"inline"}
              fontSize={"20px"}
              fw={9}
              tone={"dark"}
            >
              {t("login.noEnrolledUser.subtitle3")}
            </Text>
            <Text bright={7} disp={"inline"} fontSize={"20px"} tone={"dark"}>
              {t("login.noEnrolledUser.subtitle4")}
              {t("login.noEnrolledUser.subtitle5")}
            </Text>
          </Container>
          <Container pt={"32px"}>
            <ExternalLink>
              <Button onClick={showEnrollment} size={"md"} variant={"primary"}>
                <Container>
                  <Text bright={0} fontSize={"20px"} tone={"light"}>
                    {t("login.noEnrolledUser.button")}
                  </Text>
                </Container>
              </Button>
            </ExternalLink>
          </Container>
        </Container>
        <Container
          align={"center"}
          display={"flex"}
          height={"auto"}
          justify={"center"}
          pl={"53px"}
          width={"50%"}
          wrap={"wrap"}
        >
          <Container
            align={"center"}
            bgColor={"#2e2e38"}
            borderBL={"18px"}
            borderBR={"18px"}
            borderTR={"18px"}
            borderTl={"18px"}
            boxShadow={"0 3px 6px 0 #00000029"}
            display={"flex"}
            height={"432px"}
            justify={"center"}
            width={"527px"}
          >
            <Container>
              {benefits.map(
                (benefit: IBenefits): JSX.Element => (
                  <Container
                    align={"center"}
                    display={"flex"}
                    key={benefit.id}
                    pt={"24px"}
                    wrap={"wrap"}
                  >
                    <Container pr={"8px"}>
                      <FontAwesomeIcon color={"#f4f4f6"} icon={benefit.icon} />
                    </Container>
                    <Container maxWidth={"390px"}>
                      <Text bright={0} fontSize={"20px"} tone={"light"}>
                        {benefit.data}
                      </Text>
                    </Container>
                  </Container>
                )
              )}
            </Container>
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

export { NoEnrolledUser };

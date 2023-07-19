import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Dashboard } from "../dashboard";
import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import { enrolledUserCase, signUpLogo } from "resources";

interface IEnrolledUserProps {
  email: string;
}

const EnrolledUser: React.FC<IEnrolledUserProps> = ({ email }): JSX.Element => {
  const { t } = useTranslation();
  const [dashboardVisible, setDashboardVisible] = useState(false);

  const showDashboard = useCallback((): void => {
    setDashboardVisible(true);
  }, []);

  if (dashboardVisible) {
    return <Dashboard />;
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
              {t("signup.enrolledUser.title")}
            </Text>
          </Container>
          <Container pt={"24px"}>
            <Text bright={7} fontSize={"20px"} tone={"dark"}>
              <Text
                bright={7}
                disp={"inline"}
                fontSize={"20px"}
                fw={9}
                tone={"dark"}
              >
                {email}
              </Text>
              {t("signup.enrolledUser.subtitle")}
            </Text>
          </Container>
          <Container pt={"32px"}>
            <ExternalLink>
              <Button onClick={showDashboard} size={"md"} variant={"primary"}>
                <Container>
                  <Text bright={0} fontSize={"20px"} tone={"light"}>
                    {t("signup.enrolledUser.button")}
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
          width={"50%"}
          wrap={"wrap"}
        >
          <Container
            bgImage={`url(${enrolledUserCase})`}
            bgImagePos={"100% 100%"}
            height={"522px"}
            pt={"109px"}
            scroll={"none"}
            width={"522px"}
          />
        </Container>
      </Container>
    </Container>
  );
};

export { EnrolledUser };

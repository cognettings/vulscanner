import { useQuery } from "@apollo/client";
import { isUndefined } from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddRoot } from "./add-root";
import { FastTrackDesktop } from "./fast-track-desktop";
import { FastTrackMobile } from "./fast-track-mobile";
import { LanguagesButton } from "./languages-button";
import { NavBar } from "./navbar";
import { isPersonalEmail } from "./utils";

import { AddOauthRootForm } from "../../../scenes/Dashboard/components/AddOauthRootForm";
import { Announce } from "components/Announce";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import { useWindowSize } from "hooks";
import { GET_STAKEHOLDER_GROUPS } from "pages/home/auto-enrollment/queries";
import type {
  IAutoenrollment,
  IGetStakeholderGroupsResult,
  IOrgAttr,
  IRootAttr,
  TEnrollPages,
} from "pages/home/auto-enrollment/types";
import { autoEnrollmentBg } from "resources";
import { Logger } from "utils/logger";

const Autoenrollment: React.FC<IAutoenrollment> = ({
  initialPage,
  trialGroupName,
  trialOrgId,
  trialOrgName,
}): JSX.Element => {
  const { t } = useTranslation();
  const { width } = useWindowSize();

  // State management
  const [page, setPage] = useState<TEnrollPages>(initialPage ?? "fastTrack");
  const [progress, setProgress] = useState(50);
  const [userName, setUserName] = useState("");
  const [rootMessages, setRootMessages] = useState({
    message: "",
    type: "success",
  });

  const [repository, setRepository] = useState<IRootAttr>({
    branch: "",
    credentials: {
      auth: "TOKEN",
      azureOrganization: undefined,
      isPat: false,
      key: "",
      name: "",
      password: "",
      token: "",
      type: "",
      typeCredential: "",
      user: "",
    },
    env: "",
    exclusions: [],
    hasExclusions: "",
    url: "",
  });

  const [organizationValues, setOrganizationValues] = useState<IOrgAttr>({
    groupDescription: "",
    groupName: "",
    organizationCountry: "",
    organizationName: "",
    reportLanguage: "",
    terms: [],
  });

  const [successMutation, setSuccessMutation] = useState({
    group: false,
    organization: false,
  });

  const [hasPersonalEmail, setHasPersonalEmail] = useState<boolean | undefined>(
    undefined
  );

  // API operations
  const { data } = useQuery<IGetStakeholderGroupsResult>(
    GET_STAKEHOLDER_GROUPS,
    {
      onCompleted: async ({ me }): Promise<void> => {
        const organizationCountry = me.organizations[0]?.country || "";
        const organizationName = me.organizations[0]?.name || "";
        const group = me.organizations[0]?.groups[0]?.name || "";
        setUserName(me.userName);

        setOrganizationValues({
          ...organizationValues,
          groupName: group,
          organizationCountry,
          organizationName,
        });
        setSuccessMutation({
          group: group !== "",
          organization: organizationName !== "",
        });
        setHasPersonalEmail(await isPersonalEmail(me.userEmail));
      },
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          Logger.error("An error occurred loading stakeholder groups", message);
        });
      },
    }
  );

  const onAddRoot = useCallback((): void => {
    if (!isUndefined(trialOrgName) && !isUndefined(trialGroupName)) {
      location.replace(
        `/orgs/${trialOrgName.toLowerCase()}/groups/${trialGroupName.toLowerCase()}/vulns`
      );
    }
  }, [trialOrgName, trialGroupName]);

  if (data === undefined || hasPersonalEmail === undefined) {
    return <div />;
  }

  const { trial } = data.me;

  if (hasPersonalEmail) {
    return <Announce message={t("autoenrollment.corporateOnly")} />;
  }

  if (trial && isUndefined(initialPage)) {
    return <Announce message={t("autoenrollment.alreadyInTrial")} />;
  }

  const pages: Record<TEnrollPages, JSX.Element> = {
    fastTrack: (
      <div>
        {width < 940 ? (
          <FastTrackMobile />
        ) : (
          <Container pb={"32px"} pt={"32px"}>
            <LanguagesButton />
            <Container margin={"auto"} maxWidth={"800px"}>
              <Text fw={7} mb={2} mt={3} size={"big"} ta={"center"}>
                {t("autoenrollment.fastTrackDesktop.title")}
              </Text>
              <Text mb={4} ta={"center"}>
                {t("autoenrollment.fastTrackDesktop.subtitle")}
                <ExternalLink
                  href={"https://docs.fluidattacks.com/about/security"}
                >
                  {t("autoenrollment.fastTrackDesktop.principles")}
                </ExternalLink>
              </Text>
            </Container>
            <Container
              margin={"auto"}
              maxHeight={"600px"}
              maxWidth={"800px"}
              pb={"24px"}
              pl={"16px"}
              pr={"16px"}
              pt={"24px"}
              scroll={"y"}
            >
              <FastTrackDesktop setPage={setPage} />
            </Container>
          </Container>
        )}
      </div>
    ),
    oauthRepoForm: (
      <Container pb={"32px"} pt={"32px"}>
        <Container margin={"auto"} maxWidth={"800px"}>
          <Text fw={7} mb={4} mt={3} size={"big"} ta={"center"}>
            {t("autoenrollment.oauthFormTitle")}
          </Text>
        </Container>
        <Container
          bgColor={"#fafafa"}
          border={"1px solid #e9e9ed"}
          boxShadow={"0px 3px 6px 0px rgba(0,0,0,0.05);"}
          br={"5px"}
          margin={"auto"}
          maxHeight={"610px"}
          maxWidth={"1000px"}
          pb={"24px"}
          pl={"16px"}
          pr={"16px"}
          pt={"24px"}
          scroll={"y"}
        >
          <AddOauthRootForm
            onUpdate={onAddRoot}
            setProgress={setProgress}
            trialGroupName={trialGroupName}
            trialOrgId={trialOrgId}
          />
        </Container>
      </Container>
    ),
    repository: (
      <Container pb={"32px"} pt={"32px"}>
        <LanguagesButton />
        <Container margin={"auto"} maxWidth={"800px"}>
          <Text fw={7} mb={1} mt={3} size={"big"} ta={"center"}>
            {t("autoenrollment.title")}
          </Text>
          <Text mb={4} ta={"center"}>
            {t("autoenrollment.subtitle.main")}
            <ExternalLink href={"https://docs.fluidattacks.com/about/security"}>
              {t("autoenrollment.subtitle.link")}
            </ExternalLink>
          </Text>
        </Container>
        <Container
          bgColor={"#fafafa"}
          border={"1px solid #e9e9ed"}
          boxShadow={"0px 3px 6px 0px rgba(0,0,0,0.05);"}
          br={"5px"}
          margin={"auto"}
          maxHeight={"600px"}
          maxWidth={"800px"}
          pb={"24px"}
          pl={"16px"}
          pr={"16px"}
          pt={"24px"}
          scroll={"y"}
        >
          <AddRoot
            initialValues={repository}
            mutationsState={successMutation}
            organizationValues={organizationValues}
            rootMessages={rootMessages}
            setPage={setPage}
            setProgress={setProgress}
            setRepositoryValues={setRepository}
            setRootMessages={setRootMessages}
          />
        </Container>
      </Container>
    ),
    standBy: <div />,
  };

  return (
    <Container
      bgImage={`url(${autoEnrollmentBg})`}
      bgImagePos={"cover"}
      height={"100%"}
    >
      <React.Fragment>
        <NavBar progressWidth={progress} userName={userName} />
        <Container id={"dashboard"} scroll={"none"}>
          {pages[page]}
        </Container>
      </React.Fragment>
    </Container>
  );
};

export { Autoenrollment };

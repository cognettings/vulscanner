/* eslint react/forbid-component-props: 0 */
import React from "react";
import {
  FaFacebookSquare,
  FaInstagramSquare,
  FaLinkedin,
  FaTwitterSquare,
  FaYoutubeSquare,
} from "react-icons/fa";

import { AirsLink } from "../../../components/AirsLink";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Text } from "../../../components/Typography";
import { useDateYear } from "../../../utils/hooks/useSafeDate";
import { i18next, translate } from "../../../utils/translations/translate";

const DesktopFooter: React.FC = (): JSX.Element => {
  const currentYear = useDateYear();

  return (
    <Container align={"end"}>
      <Container
        bgColor={"#121216"}
        display={"flex"}
        justify={"center"}
        minHeight={"200px"}
        pv={5}
        wrap={"wrap"}
      >
        <Container display={"flex"} maxWidth={"1440px"} wrap={"wrap"}>
          <Container maxWidth={"470px"} ph={3} width={"30%"}>
            <Container pb={3} width={"190px"}>
              <AirsLink href={"/"}>
                <CloudImage
                  alt={"Fluid Logo Footer"}
                  src={"fluid-attacks-logo-2022-light"}
                />
              </AirsLink>
            </Container>
            <Container maxWidth={"360px"}>
              <Text color={"#8f8fa3"} mb={2} size={"big"} weight={"bold"}>
                {translate.t("footer.title")}
              </Text>
              <Text color={"#8f8fa3"} size={"medium"}>
                {translate.t("footer.subtitle")}
              </Text>
            </Container>
            <Container pv={4}>
              <AirsLink
                hovercolor={"#b0b0bf"}
                href={"https://www.linkedin.com/company/fluidattacks/"}
              >
                <FaLinkedin
                  size={28}
                  style={{ color: "#ffffff", marginRight: "16px" }}
                />
              </AirsLink>
              <AirsLink
                href={"https://www.facebook.com/Fluid-Attacks-267692397253577/"}
              >
                <FaFacebookSquare
                  size={28}
                  style={{ color: "#ffffff", marginRight: "16px" }}
                />
              </AirsLink>
              <AirsLink href={"https://twitter.com/fluidattacks/"}>
                <FaTwitterSquare
                  size={28}
                  style={{ color: "#ffffff", marginRight: "16px" }}
                />
              </AirsLink>
              <AirsLink href={"https://www.youtube.com/c/fluidattacks/"}>
                <FaYoutubeSquare
                  size={28}
                  style={{ color: "#ffffff", marginRight: "16px" }}
                />
              </AirsLink>
              <AirsLink href={"https://www.instagram.com/fluidattacks/"}>
                <FaInstagramSquare size={27} style={{ color: "#ffffff" }} />
              </AirsLink>
            </Container>
          </Container>
          <Container display={"flex"} ph={2} width={"65%"} wrap={"wrap"}>
            <Container height={"100%"} width={"25%"}>
              <Text color={"#8f8fa3"} mb={2} mt={2} size={"small"}>
                {translate.t("footer.service.title")}
              </Text>
              <AirsLink
                hovercolor={"#b0b0bf"}
                href={"/services/continuous-hacking/"}
              >
                <Text color={"#ffffff"} mb={2} size={"small"}>
                  {translate.t("menu.services.allInOne.continuous.title")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/platform/"}>
                <Text color={"#ffffff"} mb={4} size={"small"}>
                  {translate.t(
                    "menu.platform.aSinglePane.platformOverview.title"
                  )}
                </Text>
              </AirsLink>
              <Text color={"#8f8fa3"} mb={2} mt={3} size={"small"}>
                {translate.t("footer.solutions.title")}
              </Text>
              <AirsLink hovercolor={"#b0b0bf"} href={"/solutions/"}>
                <Text color={"#ffffff"} mb={2} size={"small"}>
                  {translate.t("menu.services.solutions.applicationSec.title")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/compliance/"}>
                <Text color={"#ffffff"} mb={2} size={"small"}>
                  {translate.t("menu.services.solutions.compliance.title")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/systems/"}>
                <Text color={"#ffffff"} size={"small"}>
                  {translate.t("footer.solutions.systems")}
                </Text>
              </AirsLink>
            </Container>
            <Container pl={4} width={"25%"}>
              <Text color={"#8f8fa3"} mb={2} mt={2} size={"small"}>
                {translate.t("footer.products.title")}
              </Text>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/aspm/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"ASPM"}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/sast/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"SAST"}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/dast/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"DAST"}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/mpt/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"MPT"}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/mast/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"MAST"}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/sca/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"SCA"}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/cspm/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"CSPM"}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/platform/arm/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("menu.platform.aSinglePane.ARMplatform.title")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/ptaas/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"PTaaS"}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/product/re/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {"RE"}
                </Text>
              </AirsLink>
            </Container>
            <Container pl={5} width={"25%"}>
              <Text color={"#8f8fa3"} mb={2} mt={2} size={"small"}>
                {translate.t("footer.plans.title")}
              </Text>
              <AirsLink hovercolor={"#b0b0bf"} href={"/plans/"}>
                <Text color={"#ffffff"} mb={2} size={"small"}>
                  {translate.t("footer.plans.machine")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/plans/"}>
                <Text color={"#ffffff"} mb={4} size={"small"}>
                  {translate.t("footer.plans.squad")}
                </Text>
              </AirsLink>
              <Text color={"#8f8fa3"} mb={2} mt={2} size={"small"}>
                {translate.t("footer.resources.title")}
              </Text>
              <AirsLink hovercolor={"#b0b0bf"} href={"/blog/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("menu.resources.learn.blog.title")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/advisories/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("footer.resources.advisories")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/clients/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("menu.resources.learn.clients.title")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/resources/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("menu.resources.learn.downloadables.title")}
                </Text>
              </AirsLink>
              <AirsLink
                decoration={"none"}
                hovercolor={"#b0b0bf"}
                href={"https://docs.fluidattacks.com/"}
              >
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("menu.resources.help.documentation.title")}
                </Text>
              </AirsLink>
            </Container>
            <Container pl={5} width={"25%"}>
              <Text color={"#8f8fa3"} mb={2} mt={2} size={"small"}>
                {translate.t("footer.company.title")}
              </Text>
              <AirsLink hovercolor={"#b0b0bf"} href={"/about-us/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("footer.company.about")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/certifications/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("footer.company.certifications")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/partners/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("footer.company.partners")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/careers/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("footer.company.careers")}
                </Text>
              </AirsLink>
              <AirsLink hovercolor={"#b0b0bf"} href={"/contact-us/"}>
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("footer.company.contact")}
                </Text>
              </AirsLink>
              <AirsLink
                decoration={"none"}
                hovercolor={"#b0b0bf"}
                href={"https://speakup.fluidattacks.tech/contactform/mail"}
              >
                <Text color={"#ffffff"} mb={3} size={"small"}>
                  {translate.t("footer.company.speakup")}
                </Text>
              </AirsLink>
            </Container>
          </Container>
        </Container>
      </Container>
      <Container
        align={"center"}
        bgColor={"#25252d"}
        display={"flex"}
        height={"80px"}
        justify={"center"}
      >
        <Container display={"flex"} maxWidth={"1440px"}>
          <Container
            display={"flex"}
            height={"20px"}
            justify={"center"}
            pl={2}
            pr={3}
            width={i18next.language === "es" ? "40%" : "33%"}
          >
            <Text color={"#b0b0bf"} size={"xs"} textAlign={"start"}>
              {`Copyright © ${currentYear} Fluid Attacks. We hack your software. ${translate.t(
                "footer.copyright"
              )}`}
            </Text>
          </Container>
          <Container
            align={"center"}
            display={"flex"}
            height={"25px"}
            justify={"start"}
            width={"66%"}
          >
            <AirsLink
              decoration={"none"}
              hovercolor={"#b0b0bf"}
              href={"https://status.fluidattacks.com/"}
            >
              <Text color={"#ffffff"} mr={2} size={"xs"}>
                {translate.t("footer.links.service")}
              </Text>
            </AirsLink>
            <AirsLink hovercolor={"#b0b0bf"} href={"/terms-use/"}>
              <Text color={"#ffffff"} mr={2} size={"xs"}>
                {translate.t("footer.links.termsOfUse")}
              </Text>
            </AirsLink>
            <AirsLink hovercolor={"#b0b0bf"} href={"/privacy/"}>
              <Text color={"#ffffff"} mr={2} size={"xs"}>
                {translate.t("footer.links.privacy")}
              </Text>
            </AirsLink>
            <AirsLink hovercolor={"#b0b0bf"} href={"/cookie/"}>
              <Text color={"#ffffff"} mr={2} size={"xs"}>
                {translate.t("footer.links.cookie")}
              </Text>
            </AirsLink>
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

export { DesktopFooter };

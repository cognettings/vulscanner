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
import { translate } from "../../../utils/translations/translate";

const MobileFooter: React.FC = (): JSX.Element => {
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
          <Container display={"flex"} justify={"center"}>
            <Container
              borderBottomColor={"#8f8fa3"}
              display={"flex"}
              maxWidth={"760px"}
              pb={4}
              ph={4}
              wrap={"wrap"}
            >
              <Container height={"max-content"} width={"50%"}>
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
                    {translate.t(
                      "menu.services.solutions.applicationSec.title"
                    )}
                  </Text>
                </AirsLink>
                <AirsLink hovercolor={"#b0b0bf"} href={"/compliance/"}>
                  <Text color={"#ffffff"} mb={2} size={"small"}>
                    {translate.t("menu.services.solutions.compliance.title")}
                  </Text>
                </AirsLink>
                <AirsLink hovercolor={"#b0b0bf"} href={"/systems/"}>
                  <Text color={"#ffffff"} mb={4} size={"small"}>
                    {translate.t("footer.solutions.systems")}
                  </Text>
                </AirsLink>
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
              <Container pl={3} width={"50%"}>
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
                  <Text color={"#ffffff"} mb={4} size={"small"}>
                    {translate.t("menu.resources.help.documentation.title")}
                  </Text>
                </AirsLink>
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
          <Container>
            <Container display={"flex"} mb={3} ph={3} pt={4} wrap={"wrap"}>
              <Container maxWidth={"223px"} width={"40%"}>
                <AirsLink href={"/"}>
                  <CloudImage
                    alt={"Fluid Logo Footer"}
                    src={"logo-fluid-dark-2022"}
                  />
                </AirsLink>
              </Container>
              <Container
                display={"flex"}
                justify={"end"}
                maxWidth={"600px"}
                pv={4}
                width={"60%"}
              >
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
                  href={
                    "https://www.facebook.com/Fluid-Attacks-267692397253577/"
                  }
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
            <Container ph={4}>
              <Text color={"#8f8fa3"} mb={4} size={"big"} weight={"bold"}>
                {translate.t("footer.title")}
              </Text>
              <Text color={"#8f8fa3"} size={"medium"}>
                {translate.t("footer.subtitle")}
              </Text>
            </Container>
          </Container>
        </Container>
      </Container>
      <Container
        align={"center"}
        bgColor={"#25252d"}
        display={"flex"}
        height={"130px"}
        justify={"center"}
        wrap={"wrap"}
      >
        <Container
          display={"flex"}
          height={"30px"}
          justify={"center"}
          width={"100%"}
        >
          <Text color={"#b0b0bf"} size={"xs"} textAlign={"center"}>
            {`Copyright © ${currentYear} Fluid Attacks. We hack your software. ${translate.t(
              "footer.copyright"
            )}`}
          </Text>
        </Container>
        <Container
          display={"flex"}
          height={"15px"}
          justify={"center"}
          width={"100%"}
        >
          <AirsLink hovercolor={"#b0b0bf"} href={"/"}>
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {translate.t("footer.links.service")}
            </Text>
          </AirsLink>
          <AirsLink hovercolor={"#b0b0bf"} href={"/"}>
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {translate.t("footer.links.termsOfUse")}
            </Text>
          </AirsLink>
        </Container>
        <Container
          display={"flex"}
          height={"15px"}
          justify={"center"}
          width={"100%"}
        >
          <AirsLink hovercolor={"#b0b0bf"} href={"/"}>
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {translate.t("footer.links.privacy")}
            </Text>
          </AirsLink>
          <AirsLink hovercolor={"#b0b0bf"} href={"/"}>
            <Text color={"#ffffff"} mr={2} size={"xs"}>
              {translate.t("footer.links.cookie")}
            </Text>
          </AirsLink>
        </Container>
      </Container>
    </Container>
  );
};

export { MobileFooter };

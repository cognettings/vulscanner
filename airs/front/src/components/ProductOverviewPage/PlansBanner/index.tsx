/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { BsArrowRightShort } from "react-icons/bs";

import { CardButton, CardContainer, Container } from "./styledComponents";

import { translate } from "../../../utils/translations/translate";
import { Paragraph, Title } from "../../Texts";

const PlansBanner: React.FC = (): JSX.Element => (
  <Container>
    <CardContainer>
      <Title fColor={"#2e2e38"} fSize={"36"}>
        {translate.t("productOverview.plansBanner.title")}
      </Title>
      <Paragraph
        fColor={"#5c5c70"}
        fSize={"24"}
        marginBottom={"1"}
        marginTop={"1"}
      >
        {translate.t("productOverview.plansBanner.subtitle")}
      </Paragraph>
      <Link className={"no-underline"} to={"/plans"}>
        <CardButton>
          <Title fColor={"#2e2e38"} fSize={"24"}>
            {translate.t("productOverview.plansBanner.link")}
          </Title>
          <BsArrowRightShort />
        </CardButton>
      </Link>
    </CardContainer>
  </Container>
);

export { PlansBanner };

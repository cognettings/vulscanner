/* eslint react/jsx-no-bind:0 */
/* eslint react/forbid-component-props: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { useCallback } from "react";
import ReactMarkdown from "react-markdown";

import {
  Container,
  MainTextContainer,
  ProductParagraph,
} from "./styledComponents";

import {
  FlexCenterItemsContainer,
  FullWidthContainer,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { Button } from "../../Button";
import { CloudImage } from "../../CloudImage";
import { Title } from "../../Texts";

interface IProps {
  description: string;
}

const MainSection: React.FC<IProps> = ({
  description,
}: IProps): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "main-free-trial-click",
      category: "product-overview",
    });
  }, [trackEvent]);

  return (
    <Container>
      <MainTextContainer>
        <Title fColor={"#f4f4f6"} fSize={"48"}>
          {translate.t("productOverview.title")}
        </Title>
        <ProductParagraph>
          <ReactMarkdown>{description}</ReactMarkdown>
        </ProductParagraph>
        <FlexCenterItemsContainer className={"flex-wrap"}>
          <Link
            onClick={matomoFreeTrialEvent}
            to={"https://app.fluidattacks.com/SignUp"}
          >
            <Button className={"mh2 mv3"} variant={"primary"}>
              {translate.t("productOverview.mainButton1")}
            </Button>
          </Link>
          <Link to={"/contact-us-demo/"}>
            <Button className={"mh2"} variant={"darkTertiary"}>
              {translate.t("productOverview.mainButton2")}
            </Button>
          </Link>
        </FlexCenterItemsContainer>
      </MainTextContainer>
      <FullWidthContainer>
        <CloudImage
          alt={"hero-product-overview"}
          src={"/airs/product-overview/portrait/product-portrait-1.png"}
          styles={"center flex product-portrait w-100"}
        />
      </FullWidthContainer>
    </Container>
  );
};

export { MainSection };

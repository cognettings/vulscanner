import React from "react";
import { FaFacebookF, FaLinkedinIn, FaTwitter } from "react-icons/fa";
import {
  FacebookShareButton,
  LinkedinShareButton,
  TwitterShareButton,
} from "react-share";

import { IconContainer, StickyContainer } from "./styledComponents";

import { Container } from "../../../../components/Container";
import { Text } from "../../../../components/Typography";
import { translate } from "../../../../utils/translations/translate";

interface IShareProps {
  slug: string;
}

const ShareSection: React.FC<IShareProps> = ({ slug }): JSX.Element => {
  return (
    <StickyContainer>
      <Container display={"flex"} justifySm={"center"} wrap={"wrap"}>
        <Container mv={3} width={"auto"} widthSm={"100%"}>
          <Text
            color={"#2e2e38"}
            size={"big"}
            textAlign={"center"}
            weight={"bold"}
          >
            {translate.t("blog.share.title")}
          </Text>
        </Container>
        <Container widthSm={"auto"}>
          <FacebookShareButton
            title={translate.t("blog.share.facebook")}
            url={`https://fluidattacks.com/blog/${slug}`}
          >
            <Container
              align={"center"}
              bgColor={"#2e2e38"}
              br={100}
              display={"flex"}
              height={"54px"}
              justify={"center"}
              width={"54px"}
            >
              <IconContainer>
                <FaFacebookF />
              </IconContainer>
            </Container>
          </FacebookShareButton>
        </Container>
        <Container phSm={3} pv={3} pvSm={0} widthSm={"auto"}>
          <LinkedinShareButton
            title={translate.t("blog.share.linkedin")}
            url={`https://fluidattacks.com/blog/${slug}`}
          >
            <Container
              align={"center"}
              bgColor={"#2e2e38"}
              br={100}
              display={"flex"}
              height={"54px"}
              justify={"center"}
              width={"54px"}
            >
              <IconContainer>
                <FaLinkedinIn />
              </IconContainer>
            </Container>
          </LinkedinShareButton>
        </Container>
        <Container widthSm={"auto"}>
          <TwitterShareButton
            title={translate.t("blog.share.twitter")}
            url={`https://fluidattacks.com/blog/${slug}`}
          >
            <Container
              align={"center"}
              bgColor={"#2e2e38"}
              br={100}
              display={"flex"}
              height={"54px"}
              justify={"center"}
              width={"54px"}
            >
              <IconContainer>
                <FaTwitter />
              </IconContainer>
            </Container>
          </TwitterShareButton>
        </Container>
      </Container>
    </StickyContainer>
  );
};

export { ShareSection };

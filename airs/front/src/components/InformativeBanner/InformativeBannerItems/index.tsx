/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import React from "react";
import { BsArrowRight } from "react-icons/bs";
import { RiCloseFill } from "react-icons/ri";

import { AirsLink } from "../../AirsLink";
import {
  BannerButton,
  BannerItem,
  BannerList,
  BannerTitle,
  CloseContainer,
} from "../styles/styledComponents";

interface IProps {
  buttonText: string;
  close: () => void;
  title: string;
  url: string;
}

const InformativeBannerItems: React.FC<IProps> = ({
  buttonText,
  close,
  title,
  url,
}: IProps): JSX.Element => (
  <BannerList>
    <div className={"w-auto flex flex-wrap center"}>
      <BannerItem>
        <BannerTitle>{title} &nbsp;</BannerTitle>
      </BannerItem>
      <BannerItem>
        <AirsLink decoration={"none"} href={url}>
          <BannerButton>
            {buttonText} <BsArrowRight size={15} />
          </BannerButton>
        </AirsLink>
      </BannerItem>
      <CloseContainer>
        <RiCloseFill className={"pointer white"} onClick={close} size={25} />
      </CloseContainer>
    </div>
  </BannerList>
);

export { InformativeBannerItems };

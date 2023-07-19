import styled from "styled-components";

const BannerList = styled.ul.attrs({
  className: `
    list
    ma0
    pa0
    overflow-hidden
    flex
    flex-nowrap
  `,
})``;

const InformativeBannerContainer = styled.div.attrs({
  className: `
    cssmenu
    lh-solid
    cover
    w-100
    top-0
    t-all-linear-3
  `,
})<{ bgColor: string; isClose: boolean }>`
  background-color: ${({ bgColor }): string => bgColor};
  display: ${({ isClose }): string => (isClose ? "none" : "block")};
`;

const BannerItem = styled.li.attrs({
  className: `
    flex
    flex-wrap
  `,
})`
  align-items: center;
`;

const CloseContainer = styled.li.attrs({})`
  > svg {
    color: #fcbabe;
    position: absolute;
    right: 2%;
    top: 0;
    padding-top: 8px;
  }
`;

const BannerButton = styled.button.attrs({})`
  background-color: transparent;
  border: none;
  color: #ffffff;
  font-size: 14px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 0;
  text-decoration: none;
  :hover {
    color: #fda6ab;
  }
  > svg {
    padding-left: 5px;
  }
  :hover > svg {
    transform: translateX(5px);
    transition: all 0.2s ease-in-out;
  }
`;

const BannerTitle = styled.p.attrs({
  className: `
  white
  `,
})`
  font-size: 14px;
`;

export {
  BannerButton,
  BannerItem,
  BannerList,
  BannerTitle,
  CloseContainer,
  InformativeBannerContainer,
};

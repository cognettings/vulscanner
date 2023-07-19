import styled from "styled-components";

const HomeVideoContainer = styled.div.attrs({})<{ isVisible: boolean }>`
  display: ${({ isVisible }): string => (isVisible ? "flex" : "none")};
  justify-content: center;
  width: 100%;
  iframe {
    max-width: 845px;
    width: 845px;
    height: 475px;
    max-height: 475px;
    @media screen and (max-width: 40em) {
      max-width: 347px;
      max-height: 195px;
    }
  }
`;

const HomeImageContainer = styled.div.attrs({})<{ isVisible: boolean }>`
  display: ${({ isVisible }): string => (isVisible ? "none" : "flex")};
  margin-left: 2%;
  margin-right: 2%;
  max-width: 845px;
  max-height: 475px;
`;

const PlayButtonContainer = styled.div.attrs({
  className: `
    fl
    flex
    relative
    pointer
  `,
})`
  width: 70px;
  height: 70px;
  top: 40%;
  left: 45%;
  z-index: 1;

  @media screen and (max-width: 480px) {
    top: 35%;
    left: 40%;
  }
`;

const PlayImageContainer = styled.div.attrs({
  className: `
    dib
    center
    relative
  `,
})`
  > div + img {
    margin-top: -64px;
  }
`;

export {
  HomeVideoContainer,
  HomeImageContainer,
  PlayButtonContainer,
  PlayImageContainer,
};

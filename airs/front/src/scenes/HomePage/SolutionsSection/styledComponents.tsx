import styled, { keyframes } from "styled-components";

const SolutionAnimation = keyframes`
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(-330px * 8));}
  `;

const CardFooter = styled.div`
  margin-top: auto;
`;

const CardLink = styled.div`
  &:hover > #link {
    color: #da1e28;
    text-decoration-color: #da1e28;

    p {
      color: #da1e28;
      margin-right: 3px;
    }
  }
`;

const MainCoverHome = styled.div.attrs({
  className: `
    flex
    cover-s
  `,
})`
  background-image: url("https://res.cloudinary.com/fluid-attacks/image/upload/v1673463494/airs/home/Solutions/solutions-bg.webp");
  background-size: cover;
  background-position-x: center;
`;

const SolutionsContainer = styled.div.attrs({
  className: `
  flex
  wrap
    w-100
    relative
    center
    overflow-hidden
  `,
})<{ gradientColor: string; maxWidth: number }>`
  z-index: 0;
  max-width: ${({ maxWidth }): string => `${maxWidth}px`};
  margin-bottom: 90px;

  &::before,
  &::after {
    background: linear-gradient(
      to left,
      transparent,
      ${({ gradientColor }): string => gradientColor}
    );
    content: "";
    height: 100%;
    width: 100px;
    z-index: 2;
  }

  &::after {
    right: 0;
    top: 0;
    transform: rotateZ(180deg);
  }

  &::before {
    left: 0;
    top: 0;
  }
`;

const SlideShow = styled.div.attrs({
  className: `
    flex
  `,
})`
  animation: ${SolutionAnimation} 100s linear infinite;
  width: calc(330px * 8);
  &:hover {
    animation-play-state: paused;
  }
  > div {
    margin-left: 30px;
    margin-top: 30px;
    min-width: 300px;
    max-width: 300px;
    max-height: 318px;
  }
`;

export { CardFooter, CardLink, MainCoverHome, SolutionsContainer, SlideShow };

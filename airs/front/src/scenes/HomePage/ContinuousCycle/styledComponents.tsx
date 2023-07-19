import styled from "styled-components";

const SlideShow = styled.div.attrs({
  className: `
    flex
    overflow-hidden-l
    overflow-x-auto
    scroll-smooth
    center
  `,
})`
  width: 100%;
`;

const SlideHook = styled.div.attrs({
  className: `
    flex
  `,
})`
  width: 0%;
`;

const ScrollButton = styled.div`
  button {
    &:enabled {
      svg {
        &:hover {
          background: radial-gradient(
            closest-side,
            #bf0b1a 0%,
            #bf0b1a 60%,
            #ffffff 50%,
            #ffffff 100%
          );
          fill: #fda6ab;
        }
      }
    }
  }
`;

const DropdownBar = styled.div.attrs({
  className: `
    flex
    flex-wrap
    w-100
  `,
})`
  background-color: transparent;
  > button {
    width: inherit;
  }
`;

const SplitBar = styled.div.attrs({
  className: `
  w-100
`,
})`
  border: 1px solid #dddde3;
  height: 1px;
  opacity: 0.5;
`;

const DescriptionCard = styled.div.attrs({
  classname: ``,
})<{ isCycleIncomplete: boolean }>`
  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
  display: ${({ isCycleIncomplete }): string =>
    isCycleIncomplete ? "block" : "none"};
  animation: ${({ isCycleIncomplete }): string =>
    isCycleIncomplete ? "fadeIn 2s" : ""};
  }
`;

const ProgressBar = styled.div.attrs({
  className: `
    relative
    w3-round
  `,
})<{ width: string }>`
  @keyframes fill-bar {
    from {
      width: 0%;
    }
    to {
      width: 100%;
    }
  }
  background-color: #bf0b1a;
  width: ${({ width }): string => width};
  height: 4px;
  transition: fill-bar 0.25s ease-in-out;
`;

export {
  DescriptionCard,
  DropdownBar,
  ScrollButton,
  SlideShow,
  SlideHook,
  SplitBar,
  ProgressBar,
};

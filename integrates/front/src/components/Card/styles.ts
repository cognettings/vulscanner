import styled from "styled-components";

interface ICardBoxProps {
  cover?: boolean;
  float?: boolean;
  onClick?: () => void;
}

const handleFloatEffet = (
  onClick: (React.MouseEventHandler<HTMLDivElement> & (() => void)) | undefined
): string =>
  onClick === undefined
    ? ""
    : `
      :hover {
        box-shadow: 0 2px 5px 0 #8f8fa3;
      }`;

const handleEffet = (
  onClick: (React.MouseEventHandler<HTMLDivElement> & (() => void)) | undefined
): string =>
  onClick === undefined
    ? ""
    : `
    :hover {
      border-color: #b0b0bf;
    }`;

const CardBox = styled.div.attrs({
  className: "comp-card",
})<ICardBoxProps>`
  ${({ cover = false, float = false, onClick }): string => `
  background-color: #f4f4f6;
  border-radius: 4px;
  transition: all 0.3s ease;

  ${cover ? "padding: 0px;" : "padding: 24px;"}
  ${
    float
      ? `box-shadow: 0 2px 5px 0 #b0b0bf;
    ${handleFloatEffet(onClick)}`
      : `border: solid 1px #d2d2da;
    ${handleEffet(onClick)}
  `
  }
  `}
`;

const CardImgBox = styled.div`
  background-color: #e9e9ed;
  border-radius: 4px 4px 0 0;
  margin: -20px -20px 20px -20px;

  > * {
    border-radius: 4px 4px 0 0;
    height: 100%;
    max-height: 300px;
    min-height: 100px;
    object-fit: cover;
    width: 100%;
  }
`;

export type { ICardBoxProps };
export { CardBox, CardImgBox };

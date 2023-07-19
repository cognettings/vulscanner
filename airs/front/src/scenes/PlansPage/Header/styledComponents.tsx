import styled from "styled-components";

const MainCoverHome = styled.div`
  width: 100%;
  display: block;
  justify-content: center;
  background-size: cover;
  background-image: url("https://res.cloudinary.com/fluid-attacks/image/upload/v1685126157/airs/plans/portrait-bg.png");
  background-repeat: no-repeat;
  background-position: center;
`;

const IconBlock = styled.div`
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0.3px 21.5px 21.7px 0;
  box-shadow: 0 3px 6px 0 rgba(0, 0, 0, 0.16);
  border: solid 1px #f4f4f6;
  border-radius: 7px;
`;

const Tag = styled.span`
  align-items: center;
  border-radius: 50px;
  display: inline-flex;
  font-weight: 700;
  padding: 0px 12px;
  font-size: 12px;
  text-align: center;
  background-color: #fdd8da;
  border: 1px solid #bf0b1a;
  color: #bf0b1a;
`;

const KnowLink = styled.a`
  color: #bf0b1a;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 12px;
  > svg {
    margin-left: 5px;
  }
  :hover {
    color: #da1e28;
    > svg {
      transform: translateY(2px);
    }
  }
`;

const Span = styled.span.attrs({
  className: `
    b
  `,
})<{ fColor: string }>`
  color: ${({ fColor }): string => fColor};
`;

export { KnowLink, MainCoverHome, Span, IconBlock, Tag };

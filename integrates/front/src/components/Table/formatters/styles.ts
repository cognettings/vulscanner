import styled from "styled-components";

type Nums0To7 = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;

interface ILittleFlagProps {
  className?: string;
  ml?: Nums0To7;
  bgColor?: string;
}

const LittleFlag = styled.span.attrs(
  ({ ml = 1 }: ILittleFlagProps): ILittleFlagProps => ({
    className: `ml${ml}`,
  })
)<ILittleFlagProps>`
  ${({ bgColor = "#7f0540" }): string => `
  background-color: ${bgColor};
  border-radius: 5px;
  color: #fff;
  font-size: 10px;
  padding: 2px 4px 2px 4px;
  `}
`;

export { LittleFlag };

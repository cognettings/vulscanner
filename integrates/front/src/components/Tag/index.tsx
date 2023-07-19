import styled from "styled-components";

type TVariant =
  | "blue"
  | "gray"
  | "grayNoBd"
  | "green"
  | "orange"
  | "red"
  | "redNoBd"
  | "techCspm"
  | "techDast"
  | "techMpt"
  | "techRe"
  | "techSast"
  | "techSca"
  | "techScr";

interface ITagProps {
  variant: TVariant;
}

interface IVariant {
  bgColor: string;
  borderColor: string;
  color: string;
}

const variants: Record<TVariant, IVariant> = {
  blue: {
    bgColor: "#dce4f7",
    borderColor: "#3778ff",
    color: "#3778ff",
  },
  gray: {
    bgColor: "#d2d2da",
    borderColor: "#2e2e38",
    color: "#2e2e38",
  },
  grayNoBd: {
    bgColor: "#b0b0bf",
    borderColor: "#d2d2da",
    color: "#ffffff",
  },
  green: {
    bgColor: "#c2ffd4",
    borderColor: "#009245",
    color: "#009245",
  },
  orange: {
    bgColor: "#ffeecc",
    borderColor: "#d88218",
    color: "#d88218",
  },
  red: {
    bgColor: "#fdd8da",
    borderColor: "#bf0b1a",
    color: "#bf0b1a",
  },
  redNoBd: {
    bgColor: "#fdd8da",
    borderColor: "#fdd8da",
    color: "#bf0b1a",
  },
  techCspm: {
    bgColor: "#ccffeb",
    borderColor: "#33cc99",
    color: "#33cc99",
  },
  techDast: {
    bgColor: "#b2f0f0",
    borderColor: "#177e89",
    color: "#177e89",
  },
  techMpt: {
    bgColor: "#ffa6a6",
    borderColor: "#da1e28",
    color: "#da1e28",
  },
  techRe: {
    bgColor: "#b2f2e2",
    borderColor: "#1e8c7d",
    color: "#1e8c7d",
  },
  techSast: {
    bgColor: "#fff2cc",
    borderColor: "#ffc857",
    color: "#ffc857",
  },
  techSca: {
    bgColor: "#b8d8d8",
    borderColor: "#084c61",
    color: "#084c61",
  },
  techScr: {
    bgColor: "#ffebcc",
    borderColor: "#ed7340",
    color: "#ed7340",
  },
};

const Tag = styled.span<ITagProps>`
  align-items: center;
  border-radius: 50px;
  display: inline-flex;
  font-weight: 400;
  padding: 4px 12px;
  text-align: center;
  ${({ variant }): string => {
    const { bgColor, borderColor, color } = variants[variant];

    return `
      background-color: ${bgColor};
      border: 1px solid ${borderColor};
      color: ${color};
    `;
  }}
`;

export type { ITagProps };
export { Tag };

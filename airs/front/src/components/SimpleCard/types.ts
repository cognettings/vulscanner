import type { TSize } from "../Typography/types";

type Nums0To4 = 0 | 1 | 2 | 3 | 4;

interface ISimpleCardProps {
  bgColor?: string;
  bgGradient?: string;
  borderColor?: string;
  br?: Nums0To4 | 100;
  description: string;
  descriptionColor: string;
  hovercolor?: string;
  hoverShadow?: boolean;
  image: string;
  title?: string;
  titleColor?: string;
  titleMinHeight?: string;
  titleSize?: TSize;
  maxWidth?: string;
  widthMd?: string;
  widthSm?: string;
}

export type { ISimpleCardProps };

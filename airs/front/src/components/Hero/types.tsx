import type { TSize } from "../Typography/types";

type THeroVariant = "center" | "right";
type THeroTone = "dark" | "darkGradient" | "light";
type TVariant =
  | "darkGhost"
  | "darkSecondary"
  | "darkTertiary"
  | "ghost"
  | "primary"
  | "secondary"
  | "tertiary";
interface IHeroTone {
  bgColor: string;
  button1: TVariant;
  button2: TVariant;
  subtitleColor: string;
  titleColor: string;
  paragraphColor: string;
}
interface IHeroProps {
  button1Link: string;
  button1Text: string;
  button2Link: string;
  button2Text: string;
  title: string;
  paragraph: string;
  subtitle?: string;
  image: string;
  matomoAction: string;
  size?: TSize;
  sizeMd?: TSize;
  sizeSm?: TSize;
  variant?: THeroVariant;
  tone?: THeroTone;
}

export type { IHeroProps, THeroTone, IHeroTone };

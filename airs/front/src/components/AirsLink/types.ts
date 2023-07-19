import type { MouseEventHandler } from "react";

type TDecorations = "none" | "underline";

interface ILinkProps {
  decoration?: TDecorations;
  hovercolor?: string;
  onClick?: MouseEventHandler<HTMLAnchorElement> &
    MouseEventHandler<HTMLDivElement>;
}

export type { ILinkProps, TDecorations };

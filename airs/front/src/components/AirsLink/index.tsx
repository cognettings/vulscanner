import i18next from "i18next";
import React from "react";

import { ExternalLink, InternalLink } from "./styledComponents";
import type { ILinkProps } from "./types";

import { translatedPages } from "../../utils/translations/spanishPages";

interface IAirsLinkProps extends ILinkProps {
  children: React.ReactNode;
  href: string;
}

const AirsLink: React.FC<IAirsLinkProps> = ({
  children,
  decoration,
  hovercolor,
  href,
  onClick,
}): JSX.Element => {
  const allowLinks = [
    "https://status.fluidattacks.com",
    "https://docs.fluidattacks.com",
    "https://try.fluidattacks.com",
    "https://app.fluidattacks.com",
    "https://www.instagram.com/fluidattacks",
    "https://www.facebook.com/Fluid-Attacks-267692397253577/",
    "https://twitter.com/fluidattacks",
    "https://www.youtube.com/c/fluidattacks",
    "https://www.linkedin.com/company/fluidattacks",
    "https://try.fluidattacks.tech",
  ];
  const currentLanguage = i18next.language;
  const spanishHref: { en: string; es: string } | undefined =
    translatedPages.find((page): boolean => page.en === href);
  const locationEs = spanishHref
    ? spanishHref.es
      ? spanishHref.es
      : href
    : href;
  const translatedLocation = currentLanguage === "es" ? locationEs : href;
  if (allowLinks.some((link): boolean => href.startsWith(link))) {
    return (
      <ExternalLink
        decoration={decoration}
        hovercolor={hovercolor}
        href={href}
        onClick={onClick}
        rel={"noopener noreferrer"}
        target={"_blank"}
      >
        {children}
      </ExternalLink>
    );
  } else if (href.startsWith("https://") || href.startsWith("http://")) {
    return (
      <ExternalLink
        decoration={decoration}
        hovercolor={hovercolor}
        href={href}
        onClick={onClick}
        rel={"nofollow noopener noreferrer"}
        target={"_blank"}
      >
        {children}
      </ExternalLink>
    );
  }

  return (
    <InternalLink
      decoration={decoration}
      hovercolor={hovercolor}
      onClick={onClick}
      to={translatedLocation ? translatedLocation : href}
    >
      {children}
    </InternalLink>
  );
};

export { AirsLink };
export type { IAirsLinkProps };

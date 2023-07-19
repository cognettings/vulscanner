/* eslint import/no-namespace:0 */
/* eslint fp/no-mutating-methods:0 */
/* eslint @typescript-eslint/no-non-null-assertion:0 */
import i18next from "i18next";
import { string } from "prop-types"; // eslint-disable-line import/default
import React from "react";
import { Helmet } from "react-helmet";

import { translatedPages } from "../../utils/translations/spanishPages";

interface IMetaItem {
  content: string;
  name: string;
  property?: string;
}

interface ILinkItem {
  hreflang?: string;
  href: string;
  rel: string;
}

interface ISeoProps {
  title?: string;
  description?: string;
  url?: string;
  author?: string;
  keywords?: string;
  meta?: IMetaItem[];
  image?: string;
}

const Seo: React.FC<ISeoProps> = ({
  title,
  description,
  url,
  author,
  keywords,
  meta,
  image,
}: ISeoProps): JSX.Element => {
  const siteTitle: string = title!;
  const siteDescription: string = description!;
  const siteUrl: string = url!;
  const siteAuthor: string = author!;
  const siteImage: string = image!;
  const siteKeywords: string = keywords!;
  const newLocation = `/${siteUrl}`;
  const translatedPage = translatedPages.find(
    (page): boolean =>
      page.en === newLocation || page.es === `/es${newLocation}`
  );
  const englishLink = translatedPage?.en;
  const spanishLink = translatedPage?.es;

  const metaData: IMetaItem[] = [
    {
      content: siteAuthor,
      name: "author",
    },
    {
      content: siteUrl,
      name: "canonical",
    },
    {
      content: siteDescription,
      name: "description",
    },
    {
      content: siteImage,
      name: "image",
      property: "og:image",
    },
    {
      content: siteUrl,
      name: "og:url",
    },
    {
      content: "article",
      name: "og:type",
    },
    {
      content: siteTitle,
      name: "og:title",
    },
    {
      content: siteDescription,
      name: "og:description",
    },
    {
      content: siteImage,
      name: "og:image",
    },
    {
      content: "summary_large_image",
      name: "twitter:card",
    },
    {
      content: siteAuthor,
      name: "twitter:creator",
    },
    {
      content: siteTitle,
      name: "twitter:title",
    },
    {
      content: siteDescription,
      name: "twitter:description",
    },
    {
      content: siteImage,
      name: "twitter:image",
    },
    {
      content: siteKeywords,
      name: "keywords",
    },
  ].concat(meta!);

  const linkData: ILinkItem[] = [
    {
      href: "https://res.cloudinary.com/fluid-attacks/image/upload/v1669232201/airs/favicon-2022.webp",
      rel: "shortcut icon",
    },
  ];
  if (englishLink !== undefined && spanishLink !== undefined) {
    linkData.push(
      {
        href: `https://fluidattacks.com${
          translatedPages.find((page): boolean => page.en === newLocation)
            ? newLocation
            : `/es${newLocation}`
        }`,
        hreflang: "x-default",
        rel: "alternate",
      },
      {
        href: `https://fluidattacks.com${englishLink}`,
        hreflang: "en",
        rel: "alternate",
      },
      {
        href: `https://fluidattacks.com${spanishLink}`,
        hreflang: "es",
        rel: "alternate",
      }
    );
  }

  return (
    <Helmet
      htmlAttributes={{ lang: i18next.language }}
      link={linkData}
      meta={metaData}
      title={siteTitle}
    />
  );
};

// eslint-disable-next-line fp/no-mutation
Seo.propTypes = {
  author: string,
  description: string,
  image: string,
  keywords: string,
  title: string,
  url: string,
};

// eslint-disable-next-line fp/no-mutation
Seo.defaultProps = {
  author: "",
  description: "",
  image: "",
  keywords: "",
  meta: [
    {
      content: "",
      name: "",
    },
  ],
  title: "",
  url: "",
};

export { Seo };

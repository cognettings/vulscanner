/*
 *There is no danger using dangerouslySetInnerHTML since everything is built in
 *compile time, also
 *Default exports are needed for pages used in nodes by default to create pages
 *like index.tsx or this one
 */
/* eslint react/no-danger:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import React from "react";

import { Breadcrumbs } from "../../components/Breadcrumbs";
import { CertificationsPage } from "../../components/CertificationsPage";
import { ClientsPage } from "../../components/ClientsPage";
import { PartnerPage } from "../../components/PartnerPage";
import { Seo } from "../../components/Seo";
import { Layout } from "../../scenes/Footer/Layout";
import { NavbarComponent } from "../../scenes/Menu";
import {
  BannerContainer,
  BannerTitle,
  CardsContainer1200,
  FullWidthContainer,
  PageArticle,
} from "../../styles/styledComponents";

const CardsgenIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const {
    banner,
    clientsindex,
    certificationsindex,
    description,
    keywords,
    partnersindex,
    slug,
    title,
  } = data.markdownRemark.frontmatter;

  function getMetaImage(): string {
    if (partnersindex === "yes") {
      return "https://res.cloudinary.com/fluid-attacks/image/upload/v1619633627/airs/partners/cover-partners_n4sshp.png";
    } else if (clientsindex === "yes") {
      return "https://res.cloudinary.com/fluid-attacks/image/upload/v1619635918/airs/clients/cover-clients_llnlaw.png";
    }

    return "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632703/airs/certifications/cover-certifications_dos6xu.png";
  }

  const metaImage: string = getMetaImage();

  if (partnersindex === "yes") {
    return (
      <React.Fragment>
        <Seo
          description={description}
          image={metaImage}
          keywords={keywords}
          title={`${title} | Fluid Attacks`}
          url={slug}
        />

        <Layout>
          <div>
            <NavbarComponent />
            <Breadcrumbs currentPath={path} />

            <PageArticle bgColor={"#f9f9f9"}>
              <BannerContainer className={banner}>
                <FullWidthContainer>
                  <BannerTitle>{title}</BannerTitle>
                </FullWidthContainer>
              </BannerContainer>
              <CardsContainer1200>
                <div
                  dangerouslySetInnerHTML={{
                    __html: data.markdownRemark.html,
                  }}
                />
                <PartnerPage />
              </CardsContainer1200>
            </PageArticle>
          </div>
        </Layout>
      </React.Fragment>
    );
  } else if (clientsindex === "yes") {
    return (
      <React.Fragment>
        <Seo
          description={description}
          image={metaImage}
          keywords={keywords}
          title={`${title} | Fluid Attacks`}
          url={slug}
        />

        <Layout>
          <div>
            <NavbarComponent />
            <Breadcrumbs currentPath={path} />

            <PageArticle bgColor={"#f9f9f9"}>
              <BannerContainer className={banner}>
                <FullWidthContainer>
                  <BannerTitle>{title}</BannerTitle>
                </FullWidthContainer>
              </BannerContainer>
              <CardsContainer1200>
                <div
                  dangerouslySetInnerHTML={{
                    __html: data.markdownRemark.html,
                  }}
                />
                <ClientsPage />
              </CardsContainer1200>
            </PageArticle>
          </div>
        </Layout>
      </React.Fragment>
    );
  }

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={metaImage}
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumbs currentPath={path} />

          <PageArticle bgColor={"#f9f9f9"}>
            <BannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </BannerContainer>
            <CardsContainer1200>
              <div
                dangerouslySetInnerHTML={{
                  __html: data.markdownRemark.html,
                }}
              />
              {certificationsindex === "yes" ? (
                <CertificationsPage />
              ) : undefined}
            </CardsContainer1200>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default CardsgenIndex;

export const query: StaticQueryDocument = graphql`
  query CardsgenPages($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        banner
        certificationsindex
        clientsindex
        description
        keywords
        slug
        partnersindex
        title
      }
    }
  }
`;

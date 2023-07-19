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
/* eslint fp/no-mutation: 0 */
/* eslint react/forbid-component-props: 0 */
/* eslint react/jsx-no-bind:0 */
import { graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { decode } from "he";
import React, { useCallback, useEffect, useState } from "react";
import type { SetStateAction } from "react";

import { Breadcrumbs } from "../components/Breadcrumbs";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import {
  CenteredSpacedContainer,
  FaqContainer,
  PageArticle,
  PhantomRegularRedButton,
} from "../styles/styledComponents";

const FaqIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const { banner, description, keywords, slug, subtext, subtitle, title } =
    data.markdownRemark.frontmatter;

  const hasBanner: boolean = typeof banner === "string";

  const questions = data.markdownRemark.html.split("</div>");
  const questionsPerPage = 10;

  // eslint-disable-next-line fp/no-let
  let arrayForHoldingQuestions: string[] = [];

  const [questionsToShow, setQuestionsToShow] = useState([]);
  const [next, setNext] = useState(questionsPerPage);

  const loopWithSlice = (start: number, end: number): void => {
    const slicedPosts = questions.slice(start, end);
    // eslint-disable-next-line fp/no-mutation
    arrayForHoldingQuestions = [...slicedPosts];
    setQuestionsToShow(arrayForHoldingQuestions as SetStateAction<never[]>);
  };

  useEffect((): void => {
    loopWithSlice(0, questionsPerPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleShowMorePosts = useCallback((): void => {
    loopWithSlice(0, next + questionsPerPage);
    setNext(next + questionsPerPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [next, questionsPerPage]);

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1669230787/airs/logo-fluid-2022.png"
        }
        keywords={keywords}
        title={"FAQ | Fluid Attacks"}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumbs currentPath={path} />

          <PageArticle bgColor={"#f4f4f6"}>
            <PageHeader
              banner={banner}
              pageWithBanner={hasBanner}
              slug={slug}
              subtext={subtext}
              subtitle={subtitle}
              title={decode(title)}
            />
            <FaqContainer>
              {questionsToShow.map((question): JSX.Element => {
                return (
                  <div
                    dangerouslySetInnerHTML={{
                      __html: question,
                    }}
                    key={question}
                  />
                );
              })}

              <CenteredSpacedContainer>
                <PhantomRegularRedButton
                  className={"w-50-ns w-100"}
                  onClick={handleShowMorePosts}
                >
                  {"Show more"}
                </PhantomRegularRedButton>
              </CenteredSpacedContainer>
            </FaqContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default FaqIndex;

export const query: StaticQueryDocument = graphql`
  query FaqIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        banner
        description
        keywords
        slug
        title
      }
    }
  }
`;

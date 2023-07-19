import i18next from "i18next";
import { join } from "path-browserify";
import React from "react";

import {
  Breadcrumb,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbListItem,
  BreadcrumbSeparator,
} from "./StyledComponents";

import { translate } from "../../utils/translations/translate";
import { capitalizeDashedString } from "../../utils/utilities";

interface IProps {
  currentPath: string[];
}

const Breadcrumbs: React.FC<IProps> = ({
  currentPath,
}: IProps): JSX.Element => {
  // eslint-disable-next-line fp/no-let
  let linkPath = "";

  const lastPage = currentPath.length > 0 ? currentPath.length - 1 : 0;

  return (
    <Breadcrumb>
      <BreadcrumbList>
        {currentPath.map((page, index): JSX.Element => {
          // eslint-disable-next-line fp/no-mutation
          linkPath = join(linkPath, page === "es" ? "" : page);

          const currentPage =
            page === "/" ? translate.t("breadcrumb.home") : page;
          const link = i18next.language === "es" ? `/es${linkPath}` : linkPath;

          if (currentPage !== "es") {
            return (
              <BreadcrumbListItem key={currentPage}>
                {index === lastPage ? (
                  <BreadcrumbLink to={link}>
                    {capitalizeDashedString(page)}
                  </BreadcrumbLink>
                ) : (
                  <div>
                    <BreadcrumbLink to={link}>
                      {capitalizeDashedString(currentPage)}
                    </BreadcrumbLink>
                    <BreadcrumbSeparator>{"/"}</BreadcrumbSeparator>
                  </div>
                )}
              </BreadcrumbListItem>
            );
          }

          return <div key={currentPage} />;
        })}
      </BreadcrumbList>
    </Breadcrumb>
  );
};

export { Breadcrumbs };

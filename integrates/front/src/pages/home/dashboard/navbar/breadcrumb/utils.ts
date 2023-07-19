import _ from "lodash";

import { translate } from "utils/translations/translate";

export const stylizeBreadcrumbItem: (item: string) => string = (
  item: string
): string => {
  if (/^F?\d{3}./u.exec(item)) {
    // In case of a finding title (i.e. "083. XML injection (XXE)")
    return item;
  }
  switch (item) {
    case "devsecops":
      return "DevSecOps";
    case "assigned-locations":
      return translate.t("todoList.tabs.assignedLocations");
    case "location-drafts":
      return translate.t("todoList.tabs.locationDrafts");
    case "vulns":
      return "Vulnerabilities";
    default:
      return _.capitalize(item);
  }
};

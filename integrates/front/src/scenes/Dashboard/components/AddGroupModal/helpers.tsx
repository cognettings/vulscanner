import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleCreateError = ({ graphQLErrors }: ApolloError): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - The action is not allowed during the free trial":
        msgError(translate.t("organization.tabs.groups.newGroup.trial"));
        break;
      case "Exception - Error invalid group name":
        msgError(translate.t("organization.tabs.groups.newGroup.invalidName"));
        break;
      case "Exception - User is not a member of the target organization":
        msgError(
          translate.t("organization.tabs.groups.newGroup.userNotInOrganization")
        );
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred adding a group", error);
    }
  });
};

const handleUpdateError = ({ graphQLErrors }: ApolloError): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        msgError(translate.t("group.scope.git.errors.invalid"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error(`Couldn't update tours`, error);
    }
  });
};

export { handleCreateError, handleUpdateError };

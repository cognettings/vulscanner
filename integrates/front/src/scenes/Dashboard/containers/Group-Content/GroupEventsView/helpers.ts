import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";

import type { RequestVulnerabilitiesHoldResult } from "./AffectedReattackAccordion/types";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleCreationError: (creationError: ApolloError) => void = (
  creationError: ApolloError
): void => {
  creationError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Invalid file size":
        msgError(translate.t("validations.fileSize", { count: 10 }));
        break;
      case "Exception - Invalid characters in filename":
        msgError(translate.t("validations.invalidFileName"));
        break;
      case "Exception - Invalid file type: EVENT_IMAGE":
        msgError(translate.t("group.events.form.wrongImageType"));
        break;
      case "Exception - Invalid file type: EVENT_FILE":
        msgError(translate.t("group.events.form.wrongFileType"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      case "Exception - Invalid file name: Format organizationName-groupName-10 alphanumeric chars.extension":
        msgError(translate.t("group.events.form.wrongImageName"));
        break;
      case "Exception - Unsanitized input found":
        msgError(translate.t("validations.unsanitizedInputFound"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred updating event evidence",
          creationError
        );
    }
  });
};

const handleRequestHoldError = (holdError: ApolloError): void => {
  holdError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - The event has already been closed":
        msgError(translate.t("group.events.alreadyClosed"));
        break;
      case "Exception - Request verification already on hold":
        msgError(
          translate.t("group.events.form.affectedReattacks.alreadyOnHold")
        );
        break;
      case "Exception - The vulnerability has already been closed":
        msgError(
          translate.t("group.events.form.affectedReattacks.alreadyClosed")
        );
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred requesting reattack holds",
          holdError
        );
    }
  });
};

const handleRequestVerificationError = (error: ApolloError): void => {
  error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - The event has already been closed":
        msgError(translate.t("group.events.alreadyClosed"));
        break;
      case "Exception - The event verification has been requested":
        msgError(translate.t("group.events.verificationAlreadyRequested"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred requesting event verification",
          error
        );
    }
  });
};

const handleRequestHoldsHelper = async (
  requestHold: (
    variables: Record<string, unknown>
  ) => Promise<RequestVulnerabilitiesHoldResult>,
  formattedReattacks: Record<string, string[]>,
  eventId: string,
  groupName: string
): Promise<boolean> => {
  const requestedHolds = Object.entries(formattedReattacks).map(
    async ([findingId, vulnIds]): Promise<
      RequestVulnerabilitiesHoldResult[]
    > => {
      return Promise.all([
        requestHold({
          variables: {
            eventId,
            findingId,
            groupName,
            vulnerabilities: vulnIds,
          },
        }),
      ]);
    }
  );

  const holdResults = await Promise.all(requestedHolds);

  return holdResults.every((currentResult): boolean => {
    return currentResult[0].data?.requestVulnerabilitiesHold.success ?? false;
  });
};

export {
  handleCreationError,
  handleRequestHoldError,
  handleRequestHoldsHelper,
  handleRequestVerificationError,
};

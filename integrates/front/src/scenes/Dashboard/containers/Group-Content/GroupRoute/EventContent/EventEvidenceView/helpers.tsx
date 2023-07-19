import type { ApolloError, FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleUpdateEvidenceError = (updateError: ApolloError): void => {
  updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - The event has already been closed":
        msgError(translate.t("group.events.alreadyClosed"));
        break;
      case "Exception - Invalid file size":
        msgError(translate.t("validations.fileSize", { count: 10 }));
        break;
      case "Exception - Invalid file type: EVENT_IMAGE":
        msgError(translate.t("group.events.form.wrongImageType"));
        break;
      case "Exception - Invalid file type: EVENT_FILE":
        msgError(translate.t("group.events.form.wrongFileType"));
        break;
      case "Exception - Unsanitized input found":
        msgError(translate.t("validations.unsanitizedInputFound"));
        break;
      case "Exception - Invalid file name: Format organizationName-groupName-10 alphanumeric chars.extension":
        msgError(translate.t("group.events.form.wrongImageName"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred updating event evidence",
          updateError
        );
    }
  });
};

const getDownloadHandler = (
  isEditing: boolean,
  downloadEvidence: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  eventId: string,
  data: { event: { evidenceFile: File } }
): (() => void) => {
  return (): void => {
    if (!isEditing) {
      void downloadEvidence({
        variables: { eventId, fileName: data.event.evidenceFile },
      });
    }
  };
};

export { handleUpdateEvidenceError, getDownloadHandler };

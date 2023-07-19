import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { useAbility } from "@casl/react";
import {
  faImage,
  faPen,
  faRotateRight,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import {
  handleUpdateDescriptionError,
  handleUpdateEvidenceError,
  setAltDescription,
  setPreffix,
  updateChangesHelper,
} from "./helpers";
import { formatEvidenceImages, formatEvidenceList } from "./utils";

import { Button } from "components/Button";
import { ButtonToolbarRow, Row } from "components/Layout";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";
import { meetingModeContext } from "context/meetingMode";
import { EvidenceImage } from "scenes/Dashboard/components/EvidenceImage/index";
import { EvidenceLightbox } from "scenes/Dashboard/components/EvidenceLightbox";
import {
  APPROVE_EVIDENCE_MUTATION,
  GET_FINDING_EVIDENCES,
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_DESCRIPTION_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/EvidenceView/queries";
import type {
  IEvidenceItem,
  IGetFindingEvidences,
} from "scenes/Dashboard/containers/Finding-Content/EvidenceView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import {
  composeValidators,
  isValidEvidenceName,
  isValidFileSize,
  validEvidenceImage,
} from "utils/validations";

const EvidenceView: React.FC = (): JSX.Element => {
  const { findingId, groupName, organizationName } = useParams<{
    findingId: string;
    groupName: string;
    organizationName: string;
  }>();
  const { t } = useTranslation();

  const { meetingMode } = useContext(meetingModeContext);
  const permissions = useAbility(authzPermissionsContext);
  const canApprove = permissions.can("api_mutations_approve_evidence_mutate");

  // State management
  const [isEditing, setIsEditing] = useState(false);
  const handleEditClick: () => void = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);

  const [currentImage, setCurrentImage] = useState(0);
  const [isViewerOpen, setIsViewerOpen] = useState(false);

  const closeImageViewer = useCallback(
    (index: number, isOpen: boolean): void => {
      setCurrentImage(index);
      setIsViewerOpen(isOpen);
    },
    []
  );

  const setOpenImageViewer = useCallback((index: number): void => {
    setCurrentImage(index);
    setIsViewerOpen(true);
  }, []);

  // GraphQL operations
  const { data, networkStatus, refetch } = useQuery<IGetFindingEvidences>(
    GET_FINDING_EVIDENCES,
    {
      notifyOnNetworkStatusChange: true,
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading finding evidences", error);
        });
      },
      variables: { findingId },
    }
  );
  const isRefetching = networkStatus === NetworkStatus.refetch;

  const [removeEvidence] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onCompleted: async (): Promise<void> => {
      await refetch({ findingId });
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred removing finding evidences", error);
      });
    },
  });

  const [approveEvidence, { loading: approving }] = useMutation(
    APPROVE_EVIDENCE_MUTATION,
    {
      onCompleted: async (): Promise<void> => {
        await refetch({ findingId });
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred approving finding evidences",
            error
          );
        });
      },
    }
  );

  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
    onError: (updateError): void => {
      handleUpdateDescriptionError(updateError);
    },
  });

  const [updateEvidence] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onError: (updateError): void => {
      handleUpdateEvidenceError(updateError);
    },
  });

  const openImage = useCallback(
    (index: number): VoidFunction => {
      return (): void => {
        if (!isEditing && !isRefetching) {
          setOpenImageViewer(index);
        }
      };
    },
    [isEditing, isRefetching, setOpenImageViewer]
  );

  const removeImage = useCallback(
    (evidenceId: string): VoidFunction => {
      return async (): Promise<void> => {
        mixpanel.track("RemoveEvidence");
        setIsEditing(false);
        await removeEvidence({
          variables: {
            evidenceId: evidenceId.toUpperCase(),
            findingId,
          },
        });
      };
    },
    [findingId, removeEvidence]
  );

  const approveImage = useCallback(
    (evidenceId: string): VoidFunction => {
      return async (): Promise<void> => {
        mixpanel.track("ApproveEvidence");
        setIsEditing(false);
        await approveEvidence({
          variables: {
            evidenceId: evidenceId.toUpperCase(),
            findingId,
          },
        });
      };
    },
    [findingId, approveEvidence]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const evidenceImages = formatEvidenceImages(data.finding.evidence);
  const evidenceList = formatEvidenceList(
    evidenceImages,
    isEditing,
    meetingMode
  );

  const handleUpdate = async (
    values: Record<string, IEvidenceItem>
  ): Promise<void> => {
    setIsEditing(false);

    const updateChanges = async (
      evidence: IEvidenceItem & { file?: FileList },
      key: string
    ): Promise<void> => {
      const { description, file } = evidence;
      const descriptionChanged =
        description !== evidenceImages[key].description;

      await updateChangesHelper(
        updateEvidence,
        updateDescription,
        file,
        key,
        description,
        findingId,
        descriptionChanged
      );
    };

    await Promise.all(_.map(values, updateChanges));
    setCurrentImage(0);

    await refetch();
  };

  const MAX_FILE_SIZE = 10;
  const maxFileSize = isValidFileSize(MAX_FILE_SIZE);
  const validEvidenceName = isValidEvidenceName(organizationName, groupName);

  return (
    <React.StrictMode>
      <ButtonToolbarRow>
        <Can do={"api_mutations_update_evidence_mutate"}>
          <Tooltip
            id={"searchFindings.tabEvidence.editableTooltip.id"}
            tip={t("searchFindings.tabEvidence.editableTooltip")}
          >
            <Button onClick={handleEditClick} variant={"secondary"}>
              <FontAwesomeIcon icon={faPen} />
              &nbsp;{t("searchFindings.tabEvidence.editable")}
            </Button>
          </Tooltip>
        </Can>
      </ButtonToolbarRow>
      <br />
      {_.isEmpty(evidenceList) ? (
        <div className={"no-data"}>
          <FontAwesomeIcon icon={faImage} size={"3x"} />
          <p>{t("group.findings.evidence.noData")}</p>
        </div>
      ) : (
        <Formik
          enableReinitialize={true}
          initialValues={evidenceImages}
          name={"editEvidences"}
          // eslint-disable-next-line
          onSubmit={handleUpdate} // NOSONAR
        >
          {({ dirty }): JSX.Element => (
            <Form data-private={true}>
              <React.Fragment>
                {isEditing ? (
                  <ButtonToolbarRow>
                    <Tooltip
                      id={t("searchFindings.tabEvidence.updateTooltip.id")}
                      tip={t("searchFindings.tabEvidence.updateTooltip")}
                    >
                      <Button
                        disabled={!dirty}
                        type={"submit"}
                        variant={"primary"}
                      >
                        <FontAwesomeIcon icon={faRotateRight} />
                        &nbsp;{t("searchFindings.tabEvidence.update")}
                      </Button>
                    </Tooltip>
                  </ButtonToolbarRow>
                ) : undefined}
                <Row>
                  {evidenceList.map((name, index): JSX.Element => {
                    const evidence = evidenceImages[name];
                    const content =
                      _.isEmpty(evidence.url) || isRefetching
                        ? ""
                        : `${location.href}/${evidence.url}`;
                    const preffix = setPreffix(name);
                    const altDescription = setAltDescription(preffix, evidence);

                    return (
                      <EvidenceImage
                        acceptedMimes={"image/png,video/webm"}
                        content={content}
                        date={evidence.date}
                        description={altDescription}
                        isDescriptionEditable={true}
                        isDraft={evidence.isDraft}
                        isEditing={isEditing}
                        isRemovable={!_.isEmpty(evidence.url)}
                        key={name}
                        name={name}
                        onApprove={
                          canApprove && !approving
                            ? approveImage(name)
                            : undefined
                        }
                        onClick={openImage(index)}
                        onDelete={removeImage(name)}
                        validate={composeValidators([
                          validEvidenceImage,
                          maxFileSize,
                          validEvidenceName,
                        ])}
                      />
                    );
                  })}
                </Row>
              </React.Fragment>
            </Form>
          )}
        </Formik>
      )}
      {isViewerOpen && (
        <EvidenceLightbox
          currentImage={currentImage}
          evidenceImages={evidenceList.map((name): string => {
            return evidenceImages[name].url;
          })}
          onClose={closeImageViewer}
        />
      )}
    </React.StrictMode>
  );
};

export type { IEvidenceItem };
export { EvidenceView };

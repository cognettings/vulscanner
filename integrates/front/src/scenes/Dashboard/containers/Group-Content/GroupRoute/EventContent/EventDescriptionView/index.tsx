import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { useAbility } from "@casl/react";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import { object, string } from "yup";

import { ActionButtons } from "./ActionButtons";
import type {
  IDescriptionFormValues,
  IEventDescriptionData,
  IRejectEventSolutionResultAttr,
  IUpdateEventAttr,
} from "./types";
import { UpdateSolvingReason } from "./updateSolvigReason";

import { Editable, Input, Select } from "components/Input";
import { FormGroup } from "components/Input/styles";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal";
import {
  GET_EVENT_DESCRIPTION,
  REJECT_EVENT_SOLUTION_MUTATION,
  SOLVE_EVENT_MUTATION,
  UPDATE_EVENT_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/EventDescriptionView/queries";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/queries";
import { castEventType } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { required } from "utils/validations";

const EventDescriptionView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { eventId, groupName } =
    useParams<{ eventId: string; groupName: string }>();
  const permissions = useAbility(authzPermissionsContext);
  const canUpdateEvent: boolean = permissions.can(
    "api_mutations_update_event_mutate"
  );

  const solvingReasons: Record<string, string> = {
    ACCESS_GRANTED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.accessGranted"
    ),
    AFFECTED_RESOURCE_REMOVED_FROM_SCOPE: t(
      "searchFindings.tabSeverity.common.deactivation.reason.removedFromScope"
    ),
    CLONED_SUCCESSFULLY: t(
      "searchFindings.tabSeverity.common.deactivation.reason.clonedSuccessfully"
    ),
    CREDENTIALS_ARE_WORKING_NOW: t(
      "searchFindings.tabSeverity.common.deactivation.reason.credentialsAreWorkingNow"
    ),
    DATA_UPDATED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.dataUpdated"
    ),
    ENVIRONMENT_IS_WORKING_NOW: t(
      "searchFindings.tabSeverity.common.deactivation.reason.environmentIsWorkingNow"
    ),
    INSTALLER_IS_WORKING_NOW: t(
      "searchFindings.tabSeverity.common.deactivation.reason.installerIsWorkingNow"
    ),
    IS_OK_TO_RESUME: t(
      "searchFindings.tabSeverity.common.deactivation.reason.isOkToResume"
    ),
    NEW_CREDENTIALS_PROVIDED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.newCredentialsProvided"
    ),
    NEW_ENVIRONMENT_PROVIDED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.newEnvironmentProvided"
    ),
    OTHER: t("searchFindings.tabSeverity.common.deactivation.reason.other"),
    PERMISSION_DENIED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.permissionDenied"
    ),
    PERMISSION_GRANTED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.permissionGranted"
    ),
    SUPPLIES_WERE_GIVEN: t(
      "searchFindings.tabSeverity.common.deactivation.reason.suppliesWereGiven"
    ),
    TOE_CHANGE_APPROVED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.toeApproved"
    ),
    TOE_WILL_REMAIN_UNCHANGED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.toeUnchanged"
    ),
  };
  const allSolvingReasons: Record<string, string> = {
    ...solvingReasons,
    PROBLEM_SOLVED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.problemSolved"
    ),
  };
  const solutionReasonByEventType: Record<string, string[]> = {
    AUTHORIZATION_SPECIAL_ATTACK: ["PERMISSION_DENIED", "PERMISSION_GRANTED"],
    CLIENT_CANCELS_PROJECT_MILESTONE: ["OTHER"],
    CLIENT_EXPLICITLY_SUSPENDS_PROJECT: [
      "IS_OK_TO_RESUME",
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "OTHER",
    ],
    CLONING_ISSUES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "CLONED_SUCCESSFULLY",
    ],
    CREDENTIAL_ISSUES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "CREDENTIALS_ARE_WORKING_NOW",
      "NEW_CREDENTIALS_PROVIDED",
    ],
    DATA_UPDATE_REQUIRED: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "DATA_UPDATED",
      "OTHER",
    ],
    ENVIRONMENT_ISSUES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "ENVIRONMENT_IS_WORKING_NOW",
      "NEW_ENVIRONMENT_PROVIDED",
    ],
    INSTALLER_ISSUES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "INSTALLER_IS_WORKING_NOW",
      "OTHER",
    ],
    MISSING_SUPPLIES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "SUPPLIES_WERE_GIVEN",
      "OTHER",
    ],
    NETWORK_ACCESS_ISSUES: [
      "PERMISSION_GRANTED",
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "OTHER",
    ],
    OTHER: ["OTHER"],
    REMOTE_ACCESS_ISSUES: [
      "ACCESS_GRANTED",
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "OTHER",
    ],
    TOE_DIFFERS_APPROVED: ["TOE_CHANGE_APPROVED", "TOE_WILL_REMAIN_UNCHANGED"],
    VPN_ISSUES: [
      "ACCESS_GRANTED",
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "OTHER",
    ],
  };

  // State management
  const [isSolvingModalOpen, setIsSolvingModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const openSolvingModal: () => void = useCallback((): void => {
    setIsSolvingModalOpen(true);
  }, []);
  const closeSolvingModal: () => void = useCallback((): void => {
    setIsSolvingModalOpen(false);
  }, []);
  const toggleEdit: () => void = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);

  const [isRejectSolutionModalOpen, setIsRejectSolutionModalOpen] =
    useState(false);
  const openRejectSolutionModal: () => void = useCallback((): void => {
    setIsRejectSolutionModalOpen(true);
  }, []);
  const closeRejectSolutionModal: () => void = useCallback((): void => {
    setIsRejectSolutionModalOpen(false);
  }, []);

  const handleErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading event description", error);
      });
    },
    [t]
  );

  const { data, refetch } = useQuery<IEventDescriptionData>(
    GET_EVENT_DESCRIPTION,
    {
      onError: handleErrors,
      variables: {
        canRetrieveHacker: permissions.can(
          "api_resolvers_event_hacker_resolve"
        ),
        eventId,
        groupName,
      },
    }
  );

  const handleUpdateResult: () => void = (): void => {
    void refetch();
  };

  const handleUpdateError: (updateError: ApolloError) => void = (
    updateError: ApolloError
  ): void => {
    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message === "Exception - The event has already been closed") {
        msgError(t("group.events.alreadyClosed"));
      } else {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred updating event", updateError);
      }
    });
  };

  const [solveEvent, { loading: submitting }] = useMutation(
    SOLVE_EVENT_MUTATION,
    {
      onCompleted: handleUpdateResult,
      onError: handleUpdateError,
      refetchQueries: [
        { query: GET_EVENT_HEADER, variables: { eventId } },
        {
          query: GET_EVENT_DESCRIPTION,
          variables: {
            canRetrieveHacker: permissions.can(
              "api_resolvers_event_hacker_resolve"
            ),
            eventId,
            groupName,
          },
        },
      ],
    }
  );

  const [rejectSolution] = useMutation(REJECT_EVENT_SOLUTION_MUTATION, {
    onCompleted: (mtResult: IRejectEventSolutionResultAttr): void => {
      if (mtResult.rejectEventSolution.success) {
        msgSuccess(
          t("group.events.description.alerts.rejectSolution.success"),
          t("groupAlerts.updatedTitle")
        );
        setIsRejectSolutionModalOpen(false);
      }
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Event not found":
            msgError(
              t(
                `group.events.description.alerts.editSolvingReason.eventNotFound`
              )
            );
            break;
          case "Exception - The event verification has not been requested":
            msgError(
              t(
                "group.events.description.alerts.rejectSolution.nonRequestedVerification"
              )
            );
            break;
          case "Exception - The event has already been closed":
            msgError(t("group.events.alreadyClosed"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred rejecting the event solution",
              error
            );
        }
      });
    },
    refetchQueries: [
      { query: GET_EVENT_HEADER, variables: { eventId } },
      {
        query: GET_EVENT_DESCRIPTION,
        variables: {
          canRetrieveHacker: permissions.can(
            "api_resolvers_event_hacker_resolve"
          ),
          eventId,
          groupName,
        },
      },
    ],
  });

  const [updateEvent] = useMutation(UPDATE_EVENT_MUTATION, {
    onCompleted: (mtResult: IUpdateEventAttr): void => {
      if (mtResult.updateEvent.success) {
        msgSuccess(
          t("group.events.description.alerts.editEvent.success"),
          t("groupAlerts.updatedTitle")
        );
        setIsEditing(false);
      }
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Event not found":
            msgError(
              t(`group.events.description.alerts.editEvent.eventNotFound`)
            );
            break;
          case "Exception - The event has not been solved":
            msgError(
              t(`group.events.description.alerts.editEvent.nonSolvedEvent`)
            );
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred updating the event", error);
        }
      });
    },
    refetchQueries: [
      {
        query: GET_EVENT_DESCRIPTION,
        variables: {
          canRetrieveHacker: permissions.can(
            "api_resolvers_event_hacker_resolve"
          ),
          eventId,
          groupName,
        },
      },
    ],
  });

  const handleRejectSolution: (values: Record<string, unknown>) => void =
    useCallback(
      async (values: Record<string, unknown>): Promise<void> => {
        await rejectSolution({
          variables: {
            comments: values.treatmentJustification,
            eventId,
            groupName,
          },
        });
        closeRejectSolutionModal();
      },
      [rejectSolution, eventId, groupName, closeRejectSolutionModal]
    );

  const handleSubmit: (values: Record<string, unknown>) => void = useCallback(
    (values: Record<string, unknown>): void => {
      const otherReason = values.reason === "OTHER" ? values.other : undefined;
      void solveEvent({
        variables: {
          eventId,
          groupName,
          other: otherReason,
          reason: values.reason,
        },
      });
      closeSolvingModal();
    },
    [solveEvent, eventId, groupName, closeSolvingModal]
  );

  const handleDescriptionSubmit: (values: IDescriptionFormValues) => void =
    useCallback(
      (values: IDescriptionFormValues): void => {
        const otherSolvingReason =
          values.solvingReason === "OTHER"
            ? values.otherSolvingReason
            : undefined;

        if (!_.isUndefined(data)) {
          void updateEvent({
            variables: {
              eventId,
              eventType: values.eventType,
              groupName,
              otherSolvingReason,
              solvingReason: values.solvingReason,
            },
          });
        }
      },
      [data, eventId, groupName, updateEvent]
    );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const markAsSolvedValidations = object().shape({
    other: string().when("reason", {
      is: "OTHER",
      otherwise: string().nullable(),
      then: string().required(t("validations.required")),
    }),
    reason: string().required(t("validations.required")),
  });

  const editValidations = object().shape({
    otherSolvingReason: string().when("solvingReason", {
      is: "OTHER",
      otherwise: string().nullable(),
      then: string().nullable().required(t("validations.required")),
    }),
    solvingReason: string().when("eventStatus", {
      is: "SOLVED",
      otherwise: string().nullable(),
      then: string().nullable().required(t("validations.required")),
    }),
  });

  return (
    <React.StrictMode>
      <React.Fragment>
        {isRejectSolutionModalOpen ? (
          <RemediationModal
            isLoading={false}
            isOpen={true}
            maxJustificationLength={20000}
            message={t(
              "group.events.description.rejectSolution.modal.observations"
            )}
            onClose={closeRejectSolutionModal}
            onSubmit={handleRejectSolution}
            title={t("group.events.description.rejectSolution.modal.title")}
          />
        ) : undefined}
        <Modal
          onClose={closeSolvingModal}
          open={isSolvingModalOpen}
          title={t("group.events.description.markAsSolved")}
        >
          <Formik
            enableReinitialize={true}
            initialValues={{ other: "", reason: "" }}
            name={"solvingReason"}
            onSubmit={handleSubmit}
            validationSchema={markAsSolvedValidations}
          >
            {({ dirty, values }): React.ReactNode => (
              <Form id={"solvingReason"}>
                <Row>
                  <Col>
                    <FormGroup>
                      <Select
                        label={t(
                          "searchFindings.tabSeverity.common.deactivation.reason.label"
                        )}
                        name={"reason"}
                      >
                        <option value={""} />
                        {_.map(
                          solutionReasonByEventType[data.event.eventType],
                          (reasonValue: string): JSX.Element => (
                            <option key={reasonValue} value={reasonValue}>
                              {solvingReasons[reasonValue]}
                            </option>
                          )
                        )}
                      </Select>
                    </FormGroup>
                    {values.reason === "OTHER" ? (
                      <FormGroup>
                        <Input
                          label={t(
                            "searchFindings.tabSeverity.common.deactivation.other"
                          )}
                          name={"other"}
                        />
                      </FormGroup>
                    ) : undefined}
                  </Col>
                </Row>
                {_.isEmpty(data.event.affectedReattacks) ? undefined : (
                  <Row>
                    <Col>
                      {t("group.events.description.solved.holds", {
                        length: data.event.affectedReattacks.length,
                      })}
                    </Col>
                  </Row>
                )}
                <ModalConfirm
                  disabled={!dirty || submitting}
                  onCancel={closeSolvingModal}
                />
              </Form>
            )}
          </Formik>
        </Modal>
        <Formik
          enableReinitialize={true}
          initialValues={data.event}
          name={"editEvent"}
          onSubmit={handleDescriptionSubmit}
          validationSchema={editValidations}
        >
          {({ values, dirty, setFieldValue }): React.ReactNode => {
            if (
              !_.isNull(values.solvingReason) &&
              !_.isEmpty(values.solvingReason) &&
              !_.isEmpty(values.eventType) &&
              !solutionReasonByEventType[values.eventType].includes(
                values.solvingReason
              )
            ) {
              setFieldValue("solvingReason", "");
            }

            return (
              <Form id={"editEvent"}>
                <div>
                  <div>
                    <ActionButtons
                      eventStatus={values.eventStatus}
                      isDirtyForm={dirty}
                      isEditing={isEditing}
                      onEdit={toggleEdit}
                      openRejectSolutionModal={openRejectSolutionModal}
                      openSolvingModal={openSolvingModal}
                    />
                    <br />
                    {isEditing && canUpdateEvent ? (
                      <Row>
                        <Col>
                          <Select
                            label={t("searchFindings.tabEvents.type")}
                            name={"eventType"}
                            validate={required}
                          >
                            <option value={""} />
                            <option value={"AUTHORIZATION_SPECIAL_ATTACK"}>
                              {t(castEventType("AUTHORIZATION_SPECIAL_ATTACK"))}
                            </option>
                            <option
                              value={"CLIENT_EXPLICITLY_SUSPENDS_PROJECT"}
                            >
                              {t(
                                castEventType(
                                  "CLIENT_EXPLICITLY_SUSPENDS_PROJECT"
                                )
                              )}
                            </option>
                            <option value={"CLONING_ISSUES"}>
                              {t(castEventType("CLONING_ISSUES"))}
                            </option>
                            <option value={"CREDENTIAL_ISSUES"}>
                              {t(castEventType("CREDENTIAL_ISSUES"))}
                            </option>
                            <option value={"DATA_UPDATE_REQUIRED"}>
                              {t(castEventType("DATA_UPDATE_REQUIRED"))}
                            </option>
                            <option value={"ENVIRONMENT_ISSUES"}>
                              {t(castEventType("ENVIRONMENT_ISSUES"))}
                            </option>
                            <option value={"INSTALLER_ISSUES"}>
                              {t(castEventType("INSTALLER_ISSUES"))}
                            </option>
                            <option value={"MISSING_SUPPLIES"}>
                              {t(castEventType("MISSING_SUPPLIES"))}
                            </option>
                            <option value={"NETWORK_ACCESS_ISSUES"}>
                              {t(castEventType("NETWORK_ACCESS_ISSUES"))}
                            </option>
                            <option value={"OTHER"}>
                              {t(castEventType("OTHER"))}
                            </option>
                            <option value={"REMOTE_ACCESS_ISSUES"}>
                              {t(castEventType("REMOTE_ACCESS_ISSUES"))}
                            </option>
                            <option value={"TOE_DIFFERS_APPROVED"}>
                              {t(castEventType("TOE_DIFFERS_APPROVED"))}
                            </option>
                            <option value={"VPN_ISSUES"}>
                              {t(castEventType("VPN_ISSUES"))}
                            </option>
                          </Select>
                        </Col>
                      </Row>
                    ) : undefined}
                    <Row>
                      <Col lg={50} md={50}>
                        <Editable
                          currentValue={data.event.detail}
                          isEditing={false}
                          label={t("searchFindings.tabEvents.description")}
                        >
                          <Input
                            label={t("searchFindings.tabEvents.description")}
                            name={"detail"}
                          />
                        </Editable>
                      </Col>
                      <Col lg={50} md={50}>
                        <Editable
                          currentValue={data.event.client}
                          isEditing={false}
                          label={t("searchFindings.tabEvents.client")}
                        >
                          <Input
                            label={t("searchFindings.tabEvents.client")}
                            name={"client"}
                          />
                        </Editable>
                      </Col>
                    </Row>
                    <Row>
                      <Col lg={50} md={50}>
                        <Can do={"api_resolvers_event_hacker_resolve"}>
                          <Editable
                            currentValue={data.event.hacker}
                            isEditing={false}
                            label={t("searchFindings.tabEvents.hacker")}
                          >
                            <Input
                              label={t("searchFindings.tabEvents.hacker")}
                              name={"hacker"}
                            />
                          </Editable>
                        </Can>
                      </Col>
                      <Col lg={50} md={50}>
                        <Editable
                          currentValue={
                            _.isEmpty(data.event.affectedReattacks)
                              ? "0"
                              : String(data.event.affectedReattacks.length)
                          }
                          isEditing={false}
                          label={t(
                            "searchFindings.tabEvents.affectedReattacks"
                          )}
                        >
                          <Input
                            label={t(
                              "searchFindings.tabEvents.affectedReattacks"
                            )}
                            name={"affectedReattacks"}
                          />
                        </Editable>
                      </Col>
                    </Row>
                    {data.event.eventStatus === "SOLVED" ? (
                      <UpdateSolvingReason
                        allSolvingReasons={allSolvingReasons}
                        canUpdateEvent={canUpdateEvent}
                        data={data}
                        isEditing={isEditing}
                        solutionReasonByEventType={solutionReasonByEventType}
                        solvingReasons={solvingReasons}
                        values={values}
                      />
                    ) : undefined}
                  </div>
                </div>
              </Form>
            );
          }}
        </Formik>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { EventDescriptionView };

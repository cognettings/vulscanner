import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faCloudUploadAlt,
  faList,
  faPen,
  faTrashAlt,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import { mixed, object } from "yup";

import { Button } from "components/Button";
import { InputFile } from "components/Input";
import { Col, Row } from "components/Layout";
import { Table } from "components/Table";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";
import {
  REMOVE_EVIDENCE_MUTATION,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/EvidenceView/queries";
import { GET_FINDING_RECORDS } from "scenes/Dashboard/containers/Finding-Content/RecordsView/queries";
import type { IGetFindingRecords } from "scenes/Dashboard/containers/Finding-Content/RecordsView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const RecordsView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { findingId, groupName, organizationName } = useParams<{
    findingId: string;
    groupName: string;
    organizationName: string;
  }>();

  const [isEditing, setIsEditing] = useState(false);
  const handleEditClick: () => void = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);

  const handleErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading finding records", error);
    });
  };

  const handleRemoveErrors: (removeError: ApolloError) => void = (
    removeError: ApolloError
  ): void => {
    msgError(t("groupAlerts.errorTextsad"));
    Logger.warning("An error occurred removing records", removeError);
  };

  const { data, refetch } = useQuery<IGetFindingRecords>(GET_FINDING_RECORDS, {
    onError: handleErrors,
    variables: { findingId },
  });

  const handleUpdateResult: () => void = (): void => {
    void refetch();
  };

  const handleUpdateError: (updateError: ApolloError) => void = (
    updateError: ApolloError
  ): void => {
    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      switch (message) {
        case "Exception - Invalid file name: Format organizationName-groupName-10 alphanumeric chars.extension":
          msgError(t("group.events.form.wrongImageName"));
          break;
        case "Exception - Wrong file structure":
          msgError(t("groupAlerts.invalidStructure"));
          break;
        case "Exception - Invalid file size":
          msgError(t("validations.fileSize", { count: 1 }));
          break;
        case "Exception - Invalid file type":
          msgError(t("groupAlerts.fileTypeCsv"));
          break;
        default:
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred updating records", updateError);
      }
    });
  };

  const [updateRecords, updateRes] = useMutation(UPDATE_EVIDENCE_MUTATION, {
    onCompleted: handleUpdateResult,
    onError: handleUpdateError,
  });

  const handleSubmit: (values: Record<string, FileList>) => void = useCallback(
    (values: Record<string, FileList>): void => {
      setIsEditing(false);
      void updateRecords({
        variables: {
          evidenceId: "RECORDS",
          file: values.filename[0],
          findingId,
        },
      });
    },
    [findingId, updateRecords]
  );

  const [removeRecords, removeRes] = useMutation(REMOVE_EVIDENCE_MUTATION, {
    onCompleted: handleUpdateResult,
    onError: handleRemoveErrors,
  });

  const handleRemoveClick: () => void = useCallback((): void => {
    mixpanel.track("RemoveRecords");
    setIsEditing(false);
    void removeRecords({ variables: { evidenceId: "RECORDS", findingId } });
  }, [findingId, removeRecords]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const recordData: object[] = JSON.parse(data.finding.records);

  const columns: { accessorKey: string }[] = _.isEmpty(recordData)
    ? []
    : Object.keys(recordData[0]).map((key: string): { accessorKey: string } => {
        return { accessorKey: key };
      });

  const getFileExtension: (file: File) => string = (file: File): string => {
    const splittedName: string[] = file.name.split(".");
    const extension: string =
      splittedName.length > 1 ? (_.last(splittedName) as string) : "";

    return extension.toLowerCase();
  };

  const hasExtension: (
    allowedExtensions: string[] | string,
    file?: File
  ) => boolean = (
    allowedExtensions: string[] | string,
    file?: File
  ): boolean => {
    if (!_.isUndefined(file)) {
      return _.includes(allowedExtensions, getFileExtension(file));
    }

    return false;
  };

  const validations = object().shape({
    filename: mixed()
      .required(t("validations.required"))
      .test(
        "validRecordsFile",
        t("groupAlerts.fileTypeCsv"),
        (value?: FileList): boolean => {
          if (value === undefined || _.isEmpty(value)) {
            return false;
          }

          return hasExtension("csv", _.first(value));
        }
      )
      .test(
        "validEvidenceName",
        t("group.events.form.wrongImageName"),
        (value?: FileList): boolean => {
          if (value === undefined || _.isEmpty(value)) {
            return false;
          }

          return [...Array(value.length).keys()].every(
            (index: number): boolean => {
              const file = value[index].name.toLocaleLowerCase();
              const extensions = getFileExtension(value[index]);
              const starts = `${organizationName.toLocaleLowerCase()}-${groupName.toLocaleLowerCase()}-`;
              const [ends] = file.split(starts).slice(-1);
              const regex = /^[a-zA-Z0-9]{10}$/u;

              return (
                file.startsWith(starts) &&
                regex.test(ends.replace(`.${extensions}`, ""))
              );
            }
          );
        }
      ),
  });

  return (
    <React.StrictMode>
      <React.Fragment>
        <Can do={"api_mutations_update_evidence_mutate"}>
          <Row justify={"end"}>
            <Col>
              <div>
                <Tooltip
                  id={t("searchFindings.tabRecords.editableTooltip.id")}
                  tip={t("searchFindings.tabRecords.editableTooltip")}
                >
                  <Button onClick={handleEditClick} variant={"secondary"}>
                    <FontAwesomeIcon icon={faPen} />
                    &nbsp;{t("searchFindings.tabRecords.editable")}
                  </Button>
                </Tooltip>
              </div>
            </Col>
          </Row>
        </Can>
        <br />
        {isEditing ? (
          <Formik
            enableReinitialize={true}
            initialValues={{}}
            name={"records"}
            onSubmit={handleSubmit}
            validationSchema={validations}
          >
            {({ dirty }): React.ReactNode => (
              <Form id={"records"}>
                <Row justify={"end"}>
                  <Col lg={15} md={15}>
                    <InputFile
                      accept={".csv"}
                      id={"recordsFile"}
                      name={"filename"}
                    />
                  </Col>
                  <Col lg={5} md={5}>
                    <Button
                      disabled={!dirty || updateRes.loading}
                      type={"submit"}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon icon={faCloudUploadAlt} />
                      &nbsp;{t("searchFindings.tabEvidence.update")}
                    </Button>
                  </Col>
                </Row>
              </Form>
            )}
          </Formik>
        ) : undefined}
        {isEditing && !_.isEmpty(JSON.parse(data.finding.records)) ? (
          <Row>
            <Col>
              <Button
                disabled={removeRes.loading}
                onClick={handleRemoveClick}
                variant={"secondary"}
              >
                <FontAwesomeIcon icon={faTrashAlt} />
                &nbsp;{t("searchFindings.tabEvidence.remove")}
              </Button>
            </Col>
          </Row>
        ) : undefined}
        <Row justify={"center"}>
          {_.isEmpty(JSON.parse(data.finding.records)) ? (
            <div className={"no-data"}>
              <FontAwesomeIcon icon={faList} size={"3x"} />
              <p>{t("group.findings.records.noData")}</p>
            </div>
          ) : (
            <Table
              columns={columns}
              data={JSON.parse(data.finding.records)}
              data-private={true}
              id={"tblRecords"}
            />
          )}
        </Row>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { RecordsView };

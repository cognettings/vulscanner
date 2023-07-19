import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IAffectedReattacks, IEventDescriptionData } from "./types";

import { Editable, Input, Label, Select } from "components/Input";
import { Col, Row } from "components/Layout";
import { composeValidators, required } from "utils/validations";

interface IUpdateSolvingReasonProps {
  allSolvingReasons: Record<string, string>;
  canUpdateEvent: boolean;
  data: IEventDescriptionData | undefined;
  isEditing: boolean;
  solvingReasons: Record<string, string>;
  solutionReasonByEventType: Record<string, string[]>;
  values: {
    affectedReattacks: IAffectedReattacks[];
    closingDate: string;
    hacker: string;
    client: string;
    detail: string;
    eventType: string;
    eventStatus: string;
    id: string;
    otherSolvingReason: string | null;
    solvingReason: string | null;
  };
}

export const UpdateSolvingReason: React.FC<IUpdateSolvingReasonProps> = ({
  allSolvingReasons,
  data,
  canUpdateEvent,
  isEditing,
  solvingReasons,
  solutionReasonByEventType,
  values,
}: IUpdateSolvingReasonProps): JSX.Element => {
  const { t } = useTranslation();

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }
  if (isEditing && canUpdateEvent) {
    return (
      <Row>
        <Col>
          <Row>
            <Col lg={50} md={50}>
              <Label>
                <b>{t("searchFindings.tabEvents.solvingReason")} </b>
              </Label>
              <Select
                name={"solvingReason"}
                validate={composeValidators([required])}
              >
                <option value={""} />
                {_.map(
                  solutionReasonByEventType[values.eventType],
                  (reasonValue: string): JSX.Element => (
                    <option key={reasonValue} value={reasonValue}>
                      {solvingReasons[reasonValue]}
                    </option>
                  )
                )}
              </Select>
            </Col>
            {values.solvingReason === "OTHER" ? (
              <Col lg={50} md={50}>
                <React.StrictMode>
                  <Editable
                    currentValue={
                      _.isNil(data.event.otherSolvingReason)
                        ? ""
                        : data.event.otherSolvingReason
                    }
                    isEditing={isEditing}
                    label={t(
                      "searchFindings.tabSeverity.common.deactivation.other"
                    )}
                  >
                    <Input
                      label={
                        <b>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.other"
                          )}
                        </b>
                      }
                      name={"otherSolvingReason"}
                    />
                  </Editable>
                </React.StrictMode>
              </Col>
            ) : undefined}
          </Row>
        </Col>
      </Row>
    );
  }

  return (
    <Row>
      {data.event.solvingReason === "OTHER" ? (
        <Col lg={50} md={50}>
          <Editable
            currentValue={
              _.isNil(data.event.otherSolvingReason)
                ? "-"
                : _.capitalize(data.event.otherSolvingReason)
            }
            isEditing={false}
            label={t("searchFindings.tabEvents.solvingReason")}
          >
            <Input
              label={t("searchFindings.tabEvents.solvingReason")}
              name={"otherSolvingReason"}
            />
          </Editable>
        </Col>
      ) : (
        <Col lg={50} md={50}>
          <Editable
            currentValue={
              _.isNil(data.event.solvingReason)
                ? "-"
                : allSolvingReasons[data.event.solvingReason]
            }
            isEditing={false}
            label={t("searchFindings.tabEvents.solvingReason")}
          >
            <Input
              label={t("searchFindings.tabEvents.solvingReason")}
              name={"solvingReason"}
            />
          </Editable>
        </Col>
      )}
      <Col lg={50} md={50}>
        <Editable
          currentValue={
            _.isNil(data.event.closingDate) ? "-" : data.event.closingDate
          }
          isEditing={false}
          label={t("searchFindings.tabEvents.dateClosed")}
        >
          <Input
            label={t("searchFindings.tabEvents.dateClosed")}
            name={"dateClosed"}
          />
        </Editable>
      </Col>
    </Row>
  );
};

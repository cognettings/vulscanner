import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import { getVulnerabilitySummaries } from "./utils";

import { Col, Row } from "components/Layout";
import type { IExecution } from "scenes/Dashboard/containers/Group-Content/GroupForcesView/types";

interface IExecutionDetailsProps {
  execution: IExecution;
}

const ExecutionDetails: React.FC<IExecutionDetailsProps> = (
  props: Readonly<IExecutionDetailsProps>
): JSX.Element => {
  const { t } = useTranslation();
  const { execution } = props;

  return (
    <Fragment>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.date")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2"}>{execution.date}</p>
        </Col>
      </Row>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.status.title")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2"}>{execution.status}</p>
        </Col>
      </Row>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.strictness.title")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2"}>{execution.strictness}</p>
        </Col>
      </Row>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.severityThreshold.title")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2"}>{execution.severityThreshold}</p>
        </Col>
      </Row>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.gracePeriod.title")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2"}>{execution.gracePeriod}</p>
        </Col>
      </Row>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.kind.title")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2"}>{execution.kind}</p>
        </Col>
      </Row>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.gitRepo")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2"}>{execution.gitRepo}</p>
        </Col>
      </Row>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.identifier")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2"}>{execution.executionId}</p>
        </Col>
      </Row>
      <Row>
        <Col lg={25} md={25} sm={50}>
          <p className={"mv2"}>
            <b>{t("group.forces.foundVulnerabilities.title")}</b>
          </p>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <p className={"mv2 word-wrap"}>
            {getVulnerabilitySummaries(execution.foundVulnerabilities)}
          </p>
        </Col>
      </Row>
    </Fragment>
  );
};

export { ExecutionDetails };

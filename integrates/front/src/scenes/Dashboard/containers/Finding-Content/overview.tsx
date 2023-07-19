import {
  faCalendarDay,
  faClock,
  faHeartPulse,
  faSquareCaretDown,
  faUnlock,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { CVSSFContainer } from "./styles";

import { Card } from "components/Card";
import { Col } from "components/Layout/Col";
import { Gap } from "components/Layout/Gap";
import { Row } from "components/Layout/Row";
import { Pill } from "components/Pill";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import failIcon from "resources/fail.svg";
import okIcon from "resources/ok.svg";
import { RiskExposureTour } from "scenes/Dashboard/components/RiskExposureTour/RiskExposureTour";
import { getRiskExposure } from "utils/cvss";

interface IFindingOverviewProps {
  discoveryDate: string;
  estRemediationTime: string;
  groupOpenCVSSF: number;
  maxOpenSeverityScore: number;
  openVulns: number;
  status: string;
  findingOpenCVSSF: number;
}

const FindingOverview: React.FC<IFindingOverviewProps> = ({
  discoveryDate,
  estRemediationTime,
  groupOpenCVSSF,
  maxOpenSeverityScore,
  openVulns,
  status,
  findingOpenCVSSF,
}: IFindingOverviewProps): JSX.Element => {
  const { t } = useTranslation();
  const SEVERITY_THRESHOLD_CRITICAL: number = 9;
  const SEVERITY_THRESHOLD_HIGH: number = 6.9;
  const SEVERITY_THRESHOLD_MED: number = 3.9;
  const SEVERITY_THRESHOLD_LOW: number = 0.1;

  function setSeverityLevel(
    severitylvl: number
  ): ["CRITICAL" | "HIGH" | "LOW" | "MED" | "NONE", string] {
    if (severitylvl >= SEVERITY_THRESHOLD_CRITICAL) {
      return ["CRITICAL", t("searchFindings.header.severity.level.critical")];
    }
    if (severitylvl > SEVERITY_THRESHOLD_HIGH) {
      return ["HIGH", t("searchFindings.header.severity.level.high")];
    }
    if (severitylvl > SEVERITY_THRESHOLD_MED) {
      return ["MED", t("searchFindings.header.severity.level.medium")];
    }
    if (severitylvl >= SEVERITY_THRESHOLD_LOW) {
      return ["LOW", t("searchFindings.header.severity.level.low")];
    }

    return ["NONE", t("searchFindings.header.severity.level.none")];
  }

  const severityConfigs: Record<
    string,
    { color: "darkRed" | "orange" | "red" | "yellow"; text: string }
  > = {
    CRITICAL: {
      color: "darkRed",
      text: t("searchFindings.criticalSeverity"),
    },
    HIGH: {
      color: "red",
      text: t("searchFindings.highSeverity"),
    },
    LOW: { color: "yellow", text: t("searchFindings.lowSeverity") },
    MED: {
      color: "orange",
      text: t("searchFindings.mediumSeverity"),
    },
    NONE: {
      color: "yellow",
      text: t("searchFindings.noneSeverity"),
    },
  };

  const [severityLevel, severityLevelTooltip] =
    setSeverityLevel(maxOpenSeverityScore);
  const { color, text: severityText } = severityConfigs[severityLevel];

  const statusConfigs: Record<
    string,
    { icon: string; text: string; tooltip: string }
  > = {
    DRAFT: {
      icon: okIcon,
      text: t("searchFindings.header.status.stateLabel.draft"),
      tooltip: t("searchFindings.header.status.stateTooltip.draft"),
    },
    SAFE: {
      icon: okIcon,
      text: t("searchFindings.header.status.stateLabel.closed"),
      tooltip: t("searchFindings.header.status.stateTooltip.closed"),
    },
    VULNERABLE: {
      icon: failIcon,
      text: t("searchFindings.header.status.stateLabel.open"),
      tooltip: t("searchFindings.header.status.stateTooltip.open"),
    },
  };
  const { text: statusText, tooltip: statusTooltip } = statusConfigs[status];

  const cvssfColor =
    statusText === t("searchFindings.header.status.stateLabel.closed")
      ? "green"
      : "red";

  const cvssfTextColor =
    statusText === t("searchFindings.header.status.stateLabel.closed")
      ? "dark"
      : "red";

  const remediatedLabel =
    statusText === t("searchFindings.header.status.stateLabel.closed")
      ? t("searchFindings.header.riskExposure.remediated")
      : t("searchFindings.header.riskExposure.unremediated");

  const riskExposure = getRiskExposure(
    findingOpenCVSSF,
    groupOpenCVSSF,
    status
  );

  return (
    <React.StrictMode>
      <Row>
        <Row>
          <Col lg={20} md={50} sm={100}>
            <CVSSFContainer id={"riskExposureCard"} variant={cvssfColor}>
              <Card float={true}>
                <Text
                  bright={0}
                  fw={9}
                  size={"small"}
                  ta={"start"}
                  tone={cvssfTextColor}
                >
                  {remediatedLabel}
                </Text>
                <br />
                {/* eslint-disable-next-line react/forbid-component-props */}
                <Gap style={{ border: "transparent" }}>
                  <FontAwesomeIcon
                    color={"#bf0b1a"}
                    icon={faSquareCaretDown}
                    size={"2x"}
                  />
                  <Text
                    data-private={true}
                    disp={"inline"}
                    fw={9}
                    size={"big"}
                    ta={"start"}
                  >
                    {`${riskExposure} `}
                    <span className={"comp-text fw4 f6 mb0 ml0 mr0 mt0"}>
                      {t("searchFindings.header.riskExposure.label")}
                    </span>
                  </Text>
                </Gap>
              </Card>
            </CVSSFContainer>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true}>
              <Row>
                <Col>
                  <Tooltip
                    id={"statusTooltip"}
                    tip={
                      t("searchFindings.header.status.tooltip") + statusTooltip
                    }
                  >
                    <Text data-private={true} fw={9} size={"big"} ta={"start"}>
                      {_.capitalize(status)}
                    </Text>
                  </Tooltip>
                </Col>
                <Col>
                  <Row data-private={true} justify={"end"}>
                    <Tooltip
                      id={"statusTooltip"}
                      tip={
                        t("searchFindings.header.severity.tooltip") +
                        severityLevelTooltip
                      }
                    >
                      <Pill
                        textL={maxOpenSeverityScore.toFixed(1)}
                        textR={severityText}
                        variant={color}
                      />
                    </Tooltip>
                  </Row>
                </Col>
                <Gap>
                  <FontAwesomeIcon
                    color={"#2e2e38"}
                    icon={faHeartPulse}
                    size={"lg"}
                  />
                  <Text>{t("searchFindings.header.status.label")}</Text>
                </Gap>
              </Row>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true}>
              <Row>
                <Tooltip
                  id={"openVulnsTooltip"}
                  tip={t("searchFindings.header.openVulns.tooltip")}
                >
                  <Text data-private={true} fw={9} size={"big"} ta={"start"}>
                    {openVulns}
                  </Text>
                </Tooltip>
                <Gap>
                  <FontAwesomeIcon
                    color={"#2e2e38"}
                    icon={faUnlock}
                    size={"lg"}
                  />
                  <Text>{t("searchFindings.header.openVulns.label")}</Text>
                </Gap>
              </Row>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true}>
              <Row>
                <Tooltip
                  id={"discoveryDateTooltip"}
                  tip={t("searchFindings.header.discoveryDate.tooltip")}
                >
                  <Text data-private={true} fw={9} size={"big"} ta={"start"}>
                    {discoveryDate}
                  </Text>
                </Tooltip>
                <Gap>
                  <FontAwesomeIcon
                    color={"#2e2e38"}
                    icon={faCalendarDay}
                    size={"lg"}
                  />
                  <Text>{t("searchFindings.header.discoveryDate.label")}</Text>
                </Gap>
              </Row>
            </Card>
          </Col>
          <Col lg={20} md={50} sm={100}>
            <Card float={true}>
              <Row>
                <Tooltip
                  id={"estRemediationTime"}
                  tip={t("searchFindings.header.estRemediationTime.tooltip")}
                >
                  <Text data-private={true} fw={9} size={"big"} ta={"start"}>
                    {estRemediationTime}
                  </Text>
                </Tooltip>
                <Gap>
                  <FontAwesomeIcon
                    color={"#2e2e38"}
                    icon={faClock}
                    size={"lg"}
                  />
                  <Text>
                    {t("searchFindings.header.estRemediationTime.label")}
                  </Text>
                </Gap>
              </Row>
            </Card>
          </Col>
        </Row>
      </Row>
      <RiskExposureTour findingRiskExposure={riskExposure} step={2} />
    </React.StrictMode>
  );
};

export { FindingOverview };

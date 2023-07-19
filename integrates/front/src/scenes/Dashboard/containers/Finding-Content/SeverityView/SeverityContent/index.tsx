import React from "react";
import { useTranslation } from "react-i18next";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { SeverityTile, severityImages } from "./tile";

import {
  attackComplexityBgColors,
  attackVectorBgColors,
  availabilityImpactBgColors,
  confidentialityImpactBgColors,
  exploitabilityBgColors,
  integrityImpactBgColors,
  privilegesRequiredBgColors,
  remediationLevelBgColors,
  reportConfidenceBgColors,
  severityScopeBgColors,
  userInteractionBgColors,
} from "../utils";
import { Tooltip } from "components/Tooltip";
import {
  attackComplexityValues,
  attackVectorValues,
  availabilityImpactValues,
  confidentialityImpactValues,
  exploitabilityValues,
  integrityImpactValues,
  privilegesRequiredValues,
  remediationLevelValues,
  reportConfidenceValues,
  severityScopeValues,
  userInteractionValues,
} from "utils/cvss";
import type { ICVSS3TemporalMetrics } from "utils/cvss";

const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "w-100-m w-25-ns pa1",
})``;

const Col: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "pa1 w-100 mb3-l mb2-m mb1-ns",
})``;

const FlexCol: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "flex flex-column items-center",
})``;

export const SeverityContent: React.FC<ICVSS3TemporalMetrics> = ({
  attackComplexity,
  attackVector,
  availabilityImpact,
  confidentialityImpact,
  exploitability,
  integrityImpact,
  privilegesRequired,
  remediationLevel,
  reportConfidence,
  severityScope,
  userInteraction,
}: ICVSS3TemporalMetrics): JSX.Element => {
  const { t } = useTranslation();

  function getTooltips(
    metricOptions: Record<string, string>,
    metricValue: string,
    bgColor: Record<string, string>
  ): string {
    const ind = 3;

    return (
      "<table aria-label='" +
      `${metricOptions[metricValue].split(".")[2]}` +
      "Table'><tr><td colspan='2'>" +
      `${t(
        `${metricOptions[metricValue].split(".").slice(0, ind).join(".")}` +
          ".tooltip"
      )}` +
      "</td></tr>" +
      `${Object.keys(metricOptions)
        .map(function tooltipsRow(key): string {
          return (
            `${
              metricOptions[key] === metricOptions[metricValue]
                ? `<tr class='${bgColor[key]} black'><td style='width: 20%'>`
                : `<tr><td style='width: 20%' class='${bgColor[key]} black'>`
            }` +
            "<img src='" +
            `${
              severityImages[
                metricOptions[key].split(".")[2] +
                  t(metricOptions[key]).split(" ")[0]
              ]
            }` +
            "'></td><td style='padding: 10px; text-align: left;'>" +
            `${t(metricOptions[key].replace(/label/u, "tooltip"))}` +
            "</td></tr>"
          );
        })
        .join("\n")}` +
      "</table>"
    );
  }

  return (
    <React.StrictMode>
      <div className={"flex flex-wrap items-center h-100 w-100"}>
        <Row>
          <FlexCol>
            <Col>
              <Tooltip
                effect={"float"}
                id={"userInteractionTooltip"}
                tip={getTooltips(
                  userInteractionValues,
                  userInteraction,
                  userInteractionBgColors
                )}
              >
                <SeverityTile
                  color={userInteractionBgColors[userInteraction]}
                  name={"userInteraction"}
                  valueText={t(userInteractionValues[userInteraction])}
                />
              </Tooltip>
            </Col>
            <Col>
              <Tooltip
                effect={"float"}
                id={"privilegesRequiredTooltip"}
                tip={getTooltips(
                  privilegesRequiredValues,
                  privilegesRequired,
                  privilegesRequiredBgColors
                )}
              >
                <SeverityTile
                  color={privilegesRequiredBgColors[privilegesRequired]}
                  name={"privilegesRequired"}
                  valueText={t(privilegesRequiredValues[privilegesRequired])}
                />
              </Tooltip>
            </Col>
          </FlexCol>
        </Row>
        <Row>
          <FlexCol>
            <Col>
              <Tooltip
                effect={"float"}
                id={"attackVectorTooltip"}
                tip={getTooltips(
                  attackVectorValues,
                  attackVector,
                  attackVectorBgColors
                )}
              >
                <SeverityTile
                  color={attackVectorBgColors[attackVector]}
                  name={"attackVector"}
                  valueText={t(attackVectorValues[attackVector])}
                />
              </Tooltip>
            </Col>
            <Col>
              <Tooltip
                effect={"float"}
                id={"attackComplexityTooltip"}
                tip={getTooltips(
                  attackComplexityValues,
                  attackComplexity,
                  attackComplexityBgColors
                )}
              >
                <SeverityTile
                  color={attackComplexityBgColors[attackComplexity]}
                  name={"attackComplexity"}
                  valueText={t(attackComplexityValues[attackComplexity])}
                />
              </Tooltip>
            </Col>
            <Col>
              <Tooltip
                effect={"float"}
                id={"exploitabilityTooltip"}
                tip={getTooltips(
                  exploitabilityValues,
                  exploitability,
                  exploitabilityBgColors
                )}
              >
                <SeverityTile
                  color={exploitabilityBgColors[exploitability]}
                  name={"exploitability"}
                  valueText={t(exploitabilityValues[exploitability])}
                />
              </Tooltip>
            </Col>
            <Col>
              <Tooltip
                effect={"float"}
                id={"severityScopeTooltip"}
                tip={getTooltips(
                  severityScopeValues,
                  severityScope,
                  severityScopeBgColors
                )}
              >
                <SeverityTile
                  color={severityScopeBgColors[severityScope]}
                  name={"severityScope"}
                  valueText={t(severityScopeValues[severityScope])}
                />
              </Tooltip>
            </Col>
          </FlexCol>
        </Row>
        <Row>
          <FlexCol>
            <Col>
              <Tooltip
                effect={"float"}
                id={"availabilityImpactTooltip"}
                tip={getTooltips(
                  availabilityImpactValues,
                  availabilityImpact,
                  availabilityImpactBgColors
                )}
              >
                <SeverityTile
                  color={availabilityImpactBgColors[availabilityImpact]}
                  name={"availabilityImpact"}
                  valueText={t(availabilityImpactValues[availabilityImpact])}
                />
              </Tooltip>
            </Col>
            <Col>
              <Tooltip
                effect={"float"}
                id={"integrityImpactTooltip"}
                tip={getTooltips(
                  integrityImpactValues,
                  integrityImpact,
                  integrityImpactBgColors
                )}
              >
                <SeverityTile
                  color={integrityImpactBgColors[integrityImpact]}
                  name={"integrityImpact"}
                  valueText={t(integrityImpactValues[integrityImpact])}
                />
              </Tooltip>
            </Col>
            <Col>
              <Tooltip
                effect={"float"}
                id={"confidentialityImpactTooltip"}
                tip={getTooltips(
                  confidentialityImpactValues,
                  confidentialityImpact,
                  confidentialityImpactBgColors
                )}
              >
                <SeverityTile
                  color={confidentialityImpactBgColors[confidentialityImpact]}
                  name={"confidentialityImpact"}
                  valueText={t(
                    confidentialityImpactValues[confidentialityImpact]
                  )}
                />
              </Tooltip>
            </Col>
          </FlexCol>
        </Row>
        <Row>
          <FlexCol>
            <Col>
              <Tooltip
                effect={"float"}
                id={"remediationLevelTooltip"}
                tip={getTooltips(
                  remediationLevelValues,
                  remediationLevel,
                  remediationLevelBgColors
                )}
              >
                <SeverityTile
                  color={remediationLevelBgColors[remediationLevel]}
                  name={"remediationLevel"}
                  valueText={t(remediationLevelValues[remediationLevel])}
                />
              </Tooltip>
            </Col>
            <Col>
              <Tooltip
                effect={"float"}
                id={"reportConfidenceTooltip"}
                tip={getTooltips(
                  reportConfidenceValues,
                  reportConfidence,
                  reportConfidenceBgColors
                )}
              >
                <SeverityTile
                  color={reportConfidenceBgColors[reportConfidence]}
                  name={"reportConfidence"}
                  valueText={t(reportConfidenceValues[reportConfidence])}
                />
              </Tooltip>
            </Col>
          </FlexCol>
        </Row>
      </div>
    </React.StrictMode>
  );
};

import type { FC } from "react";
import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";

import type { IStandardComplianceAttr } from "../types";
import { getProgressBarColor, handleCompliancePercentageValue } from "../utils";
import { Card } from "components/Card";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { ProgressBar } from "components/ProgressBar";
import { Text } from "components/Text";

const TextOverview = styled(Text)`
  display: inline;
  margin-left: auto;
  width: auto;
`;

interface IBenchmarkCardProps {
  standardCompliance: IStandardComplianceAttr;
}

const BenchmarkCard: FC<IBenchmarkCardProps> = (
  props: IBenchmarkCardProps
): JSX.Element => {
  const { standardCompliance } = props;
  const { t } = useTranslation();

  return (
    <Card>
      <Row>
        <Text fw={6} size={"small"} ta={"center"}>
          {standardCompliance.standardTitle.toUpperCase()}
        </Text>
      </Row>
      <br />
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"start"}>
            {t(
              "organization.tabs.compliance.tabs.overview.cards.myOrganization"
            )}
          </Text>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <div className={"flex items-center"}>
            <TextOverview mr={1}>
              {`${handleCompliancePercentageValue(
                standardCompliance.complianceLevel
              )}%`}
            </TextOverview>
            <ProgressBar
              height={10}
              maxWidth={35}
              percentage={handleCompliancePercentageValue(
                standardCompliance.complianceLevel
              )}
              progressColor={getProgressBarColor(
                handleCompliancePercentageValue(
                  standardCompliance.complianceLevel
                )
              )}
            />
          </div>
        </Col>
      </Row>
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"start"}>
            {t(
              "organization.tabs.compliance.tabs.overview.cards.bestOrganization"
            )}
          </Text>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <div className={"flex items-center"}>
            <TextOverview mr={1}>
              {`${handleCompliancePercentageValue(
                standardCompliance.bestOrganizationComplianceLevel
              )}%`}
            </TextOverview>
            <ProgressBar
              height={10}
              maxWidth={35}
              percentage={handleCompliancePercentageValue(
                standardCompliance.bestOrganizationComplianceLevel
              )}
              progressColor={getProgressBarColor(
                handleCompliancePercentageValue(
                  standardCompliance.bestOrganizationComplianceLevel
                )
              )}
            />
          </div>
        </Col>
      </Row>
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"start"}>
            {t(
              "organization.tabs.compliance.tabs.overview.cards.avgOrganization"
            )}
          </Text>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <div className={"flex justify-between items-center"}>
            <TextOverview mr={1}>
              {`${handleCompliancePercentageValue(
                standardCompliance.avgOrganizationComplianceLevel
              )}%`}
            </TextOverview>
            <ProgressBar
              height={10}
              maxWidth={35}
              percentage={handleCompliancePercentageValue(
                standardCompliance.avgOrganizationComplianceLevel
              )}
              progressColor={getProgressBarColor(
                handleCompliancePercentageValue(
                  standardCompliance.avgOrganizationComplianceLevel
                )
              )}
            />
          </div>
        </Col>
      </Row>
      <Row>
        <Col lg={50} md={50} sm={50}>
          <Text ta={"start"}>
            {t(
              "organization.tabs.compliance.tabs.overview.cards.worstOrganization"
            )}
          </Text>
        </Col>
        <Col lg={50} md={50} sm={50}>
          <div className={"flex justify-between items-center"}>
            <TextOverview mr={1}>
              {`${handleCompliancePercentageValue(
                standardCompliance.worstOrganizationComplianceLevel
              )}%`}
            </TextOverview>
            <ProgressBar
              height={10}
              maxWidth={35}
              percentage={handleCompliancePercentageValue(
                standardCompliance.worstOrganizationComplianceLevel
              )}
              progressColor={getProgressBarColor(
                handleCompliancePercentageValue(
                  standardCompliance.worstOrganizationComplianceLevel
                )
              )}
            />
          </div>
        </Col>
      </Row>
    </Card>
  );
};
export { BenchmarkCard };

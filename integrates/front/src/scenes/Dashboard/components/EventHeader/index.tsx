import React from "react";
import { useTranslation } from "react-i18next";

import { EventHeaderGrid, EventHeaderLabel, HeaderContainer } from "./styles";

import { Col, Row } from "components/Layout";
import { Tag } from "components/Tag";
import { castEventStatus, castEventType } from "utils/formatHelpers";

interface IEventHeaderProps {
  eventDate: string;
  eventStatus: string;
  eventType: string;
  id: string;
}

const EventHeader: (props: IEventHeaderProps) => JSX.Element = ({
  eventDate,
  eventStatus,
  eventType,
  id,
}: IEventHeaderProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <HeaderContainer>
      <Row>
        <Col>
          <h2>{t(castEventType(eventType))}</h2>
        </Col>
      </Row>
      <Row>
        <Col>
          <EventHeaderGrid>
            <EventHeaderLabel>
              {t("searchFindings.tabEvents.id")}
              &nbsp;<Tag variant={"gray"}>{id}</Tag>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {t("searchFindings.tabEvents.date")}
              &nbsp;<Tag variant={"gray"}>{eventDate}</Tag>
            </EventHeaderLabel>
            <EventHeaderLabel>
              {t("searchFindings.tabEvents.status")}
              &nbsp;
              <Tag variant={"gray"}>{t(castEventStatus(eventStatus))}</Tag>
            </EventHeaderLabel>
          </EventHeaderGrid>
        </Col>
      </Row>
    </HeaderContainer>
  );
};

export type { IEventHeaderProps };
export { EventHeader };

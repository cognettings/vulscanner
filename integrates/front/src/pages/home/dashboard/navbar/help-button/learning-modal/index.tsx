import {
  faChalkboardUser,
  faCirclePlay,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Card } from "components/Card";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";

interface ILearningModalProps {
  closeLearningModal: () => void;
}

const LearningModal: React.FC<ILearningModalProps> = ({
  closeLearningModal,
}: ILearningModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [isContinueButtonEnabled, setIsContinueButtonEnabled] = useState(false);
  const enableContinueButton = useCallback((): void => {
    setIsContinueButtonEnabled(true);
  }, []);

  const handleSubmit = useCallback((values: { source: string }): void => {
    const youTube: string =
      "https://www.youtube.com/watch?v=g8H_c0b7fwo&list=PLKPXyOiQVsn1mXmT4npbmcek3Qvafet1q";
    const demo: string =
      "https://calendar.google.com/calendar/u/0/appointments/schedules/AcZssZ0pQK5FqJgW7EKqGY1msaShj8Lu4yyQEVzBYg5R72dWVu2f-rhNVXhvIOUEwEhpy0cLT22yKJNh";
    if (values.source === "VIDEO_TUTORIALS") {
      window.open(youTube, "_blank", "noreferrer");
    } else {
      window.open(demo, "_blank", "noreferrer");
    }
  }, []);

  return (
    <Modal
      minWidth={400}
      onClose={closeLearningModal}
      open={true}
      title={t("navbar.help.options.learn.title")}
    >
      <Formik
        initialValues={{
          source: "",
        }}
        name={"updateAccessToken"}
        onSubmit={handleSubmit}
      >
        <Form>
          <Row>
            <Col>
              <Text mb={1}>{t("navbar.help.options.learn.description")}</Text>
            </Col>
          </Row>
          <Row>
            <Col>
              <Card cover={true} float={true} title={""}>
                <Row>
                  <Col>
                    &nbsp;
                    <Field
                      name={"source"}
                      onClick={enableContinueButton}
                      type={"radio"}
                      value={"LIVE_DEMO"}
                    />
                    <Text fw={9} ta={"center"}>
                      <FontAwesomeIcon icon={faChalkboardUser} size={"xl"} />
                      &nbsp;
                      {t("navbar.help.options.learn.liveDemo")}
                    </Text>
                  </Col>
                </Row>
                <br />
              </Card>
            </Col>
            <Col>
              <Card cover={true} float={true} title={""}>
                <Row>
                  <Col>
                    &nbsp;
                    <Field
                      name={"source"}
                      onClick={enableContinueButton}
                      type={"radio"}
                      value={"VIDEO_TUTORIALS"}
                    />
                    <Text fw={9} ta={"center"}>
                      <FontAwesomeIcon icon={faCirclePlay} size={"xl"} />
                      &nbsp;
                      {t("navbar.help.options.learn.videoTutorials")}
                    </Text>
                  </Col>
                </Row>
                <br />
              </Card>
            </Col>
          </Row>
          <ModalConfirm
            disabled={!isContinueButtonEnabled}
            onCancel={closeLearningModal}
            txtCancel={t("navbar.help.options.learn.cancelBtn")}
            txtConfirm={t("navbar.help.options.learn.confirmBtn")}
          />
        </Form>
      </Formik>
    </Modal>
  );
};

export type { ILearningModalProps };
export { LearningModal };

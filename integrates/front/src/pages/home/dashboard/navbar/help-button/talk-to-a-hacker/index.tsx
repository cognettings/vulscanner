import { Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Select } from "components/Input";
import { Col, Row } from "components/Layout";
import { Modal } from "components/Modal";
import { Text } from "components/Text";
import { useCalendly } from "hooks";
import { documentation } from "resources/index";

interface ITalkToHackerModalProps {
  closeTalkToHackerModal: () => void;
}

const TalkToHackerModal: React.FC<ITalkToHackerModalProps> = ({
  closeTalkToHackerModal,
}: ITalkToHackerModalProps): JSX.Element => {
  const { t } = useTranslation();
  const { openCalendly } = useCalendly();

  const handleSubmit = useCallback(
    (values: { checkDocumentation: string }): void => {
      if (values.checkDocumentation === "YES") {
        openCalendly();
      } else {
        window.open(
          "https://docs.fluidattacks.com/criteria/vulnerabilities/",
          "_blank",
          "noreferrer"
        );
      }
      closeTalkToHackerModal();
    },
    [closeTalkToHackerModal, openCalendly]
  );

  return (
    <Modal
      maxWidth={"460px"}
      onClose={closeTalkToHackerModal}
      open={true}
      title={t("navbar.help.options.expert.title")}
    >
      <Formik
        initialValues={{ checkDocumentation: "" }}
        name={"scheduleTalkToAHacker"}
        onSubmit={handleSubmit}
      >
        {({ values }): React.ReactNode => (
          <Form>
            <Row>
              <Col>
                <Text mb={3}>
                  {t("navbar.help.options.expert.documentation.description")}
                </Text>
              </Col>
            </Row>
            <Row>
              <Col>
                <Text fw={9} mb={3}>
                  {t("navbar.help.options.expert.documentation.check")}
                </Text>
                <Select id={"check"} name={"checkDocumentation"}>
                  <option
                    disabled={true}
                    hidden={true}
                    selected={true}
                    value={""}
                  >
                    {t("navbar.help.options.expert.documentation.placeholder")}
                  </option>
                  <option value={"NO"}>
                    {t("navbar.help.options.expert.documentation.deny")}
                  </option>
                  <option value={"YES"}>
                    {t("navbar.help.options.expert.documentation.confirm")}
                  </option>
                </Select>
                &nbsp;
                {values.checkDocumentation === "YES" ? (
                  <Col>
                    <Button type={"submit"} variant={"primary"}>
                      {t("navbar.help.options.expert.documentation.btnConfirm")}
                    </Button>
                  </Col>
                ) : undefined}
                {values.checkDocumentation === "NO" ? (
                  <Col>
                    <Container
                      align={"center"}
                      display={"block"}
                      justify={"center"}
                      width={"100%"}
                    >
                      <Container
                        bgImage={`url(${documentation})`}
                        bgImagePos={"100% 100%"}
                        height={"135px"}
                        width={"433px"}
                      />
                      &nbsp;
                      <Text lineHeight={"1.4"} mb={3}>
                        {t(
                          "navbar.help.options.expert.documentation.descriptionDeny"
                        )}
                      </Text>
                      <Button type={"submit"} variant={"secondary"}>
                        {t("navbar.help.options.expert.documentation.btnDeny")}
                      </Button>
                    </Container>
                  </Col>
                ) : undefined}
              </Col>
            </Row>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export { TalkToHackerModal };

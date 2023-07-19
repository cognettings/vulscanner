import type { ApolloQueryResult } from "@apollo/client";
import dayjs from "dayjs";
import { Form, Formik } from "formik";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Input, InputDate, TextArea } from "components/Input";
import { Gap, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { useAddAccessToken } from "pages/home/dashboard/navbar/user-profile/api-token-modal/hooks";
import type { IGetAccessTokenAttr } from "pages/home/dashboard/navbar/user-profile/api-token-modal/types";
import { validateSchema } from "pages/home/dashboard/navbar/user-profile/api-token-modal/validations";
import { msgError, msgSuccess } from "utils/notifications";

interface IAddTokenModalProps {
  open: boolean;
  onClose: () => void;
  refetch: () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>;
}

interface IAccessTokenAttr {
  expirationTime: string;
  name: string;
}

const AddTokenModal: React.FC<IAddTokenModalProps> = ({
  open,
  onClose,
  refetch,
}): JSX.Element => {
  const { t } = useTranslation();
  const sixMonthsLater = dayjs().add(6, "months").format("YYYY-MM-DD");
  const oneDayLater = dayjs().add(1, "day").format("YYYY-MM-DD");

  const [addAccessToken, mtResponse] = useAddAccessToken(refetch);
  const handleUpdateAPIToken = useCallback(
    async (values: IAccessTokenAttr): Promise<void> => {
      mixpanel.track("GenerateAPIToken");
      await addAccessToken({
        variables: {
          expirationTime: dayjs(values.expirationTime).unix(),
          name: values.name,
        },
      });
    },
    [addAccessToken]
  );

  const handleCopy = useCallback(async (): Promise<void> => {
    const { clipboard } = navigator;

    if (_.isUndefined(clipboard)) {
      msgError(t("updateAccessToken.copy.failed"));
    } else {
      await clipboard.writeText(
        mtResponse.data?.addAccessToken.sessionJwt ?? ""
      );
      msgSuccess(
        t("updateAccessToken.copy.successfully"),
        t("updateAccessToken.copy.success")
      );
    }
  }, [mtResponse.data?.addAccessToken.sessionJwt, t]);

  return (
    <Modal
      onClose={onClose}
      open={open}
      title={t("updateAccessToken.addTitle")}
    >
      <Formik
        enableReinitialize={true}
        initialValues={{
          expirationTime: "",
          name: "",
          sessionJwt: mtResponse.data?.addAccessToken.sessionJwt ?? "",
        }}
        name={"updateAccessToken"}
        onSubmit={handleUpdateAPIToken}
        validationSchema={validateSchema}
      >
        {({ isSubmitting, values }): JSX.Element => {
          if (values.sessionJwt === "") {
            return (
              <Form>
                <Row>
                  <Input
                    id={"name"}
                    label={t("updateAccessToken.fields.name")}
                    name={"name"}
                    type={"text"}
                  />
                </Row>
                <Row>
                  <InputDate
                    label={t("updateAccessToken.expirationTime")}
                    max={sixMonthsLater}
                    min={oneDayLater}
                    name={"expirationTime"}
                  />
                </Row>
                <ModalConfirm disabled={isSubmitting} onCancel={onClose} />
              </Form>
            );
          }

          return (
            <Gap disp={"block"} mh={0}>
              <Text fw={7}>{t("updateAccessToken.message")}</Text>
              <TextArea disabled={true} name={"sessionJwt"} rows={5} />
              <Button onClick={handleCopy} variant={"secondary"}>
                {t("updateAccessToken.copy.copy")}
              </Button>
            </Gap>
          );
        }}
      </Formik>
    </Modal>
  );
};

export { AddTokenModal };

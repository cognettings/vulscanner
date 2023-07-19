import { useMutation } from "@apollo/client";
import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddCreditCardModal } from "./AddCreditCard";
import { AddOtherMethodModal } from "./AddOtherMethod";
import { ADD_OTHER_PAYMENT_METHOD } from "./queries";

import { FormikSelect } from "components/Input/Formik/FormikSelect";
import { Row as Container } from "components/Layout";
import { Modal } from "components/Modal";
import { getEnvironment } from "utils/environment";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const STRIPE_PK_LIVE_MODE = "pk_live_ATYIex0kuszLHUTMo5dJ7ffx";
const STRIPE_PK_TEST_MODE = "pk_test_hfBDuDH6n4MevubIYN0NrAAA";

interface IAddMethodPaymentProps {
  organizationId: string;
  onClose: () => void;
  onUpdate: () => void;
}

export const AddPaymentMethod: React.FC<IAddMethodPaymentProps> = ({
  organizationId,
  onClose,
  onUpdate,
}: IAddMethodPaymentProps): JSX.Element => {
  const { t } = useTranslation();

  const stripePk =
    getEnvironment() === "production"
      ? STRIPE_PK_LIVE_MODE
      : STRIPE_PK_TEST_MODE;
  const stripePromise = loadStripe(stripePk);
  const [paymentType, setPaymentType] = useState("");

  const [addOtherPaymentMethod] = useMutation(ADD_OTHER_PAYMENT_METHOD, {
    onCompleted: (): void => {
      onUpdate();
      onClose();
      msgSuccess(
        t("organization.tabs.billing.paymentMethods.add.success.body"),
        t("organization.tabs.billing.paymentMethods.add.success.title")
      );
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't create payment method", error);
      });
    },
  });
  const handleFileListUpload = (
    file: FileList | undefined
  ): File | undefined => {
    return _.isEmpty(file) ? undefined : (file as FileList)[0];
  };
  const handleAddOtherMethodSubmit = useCallback(
    async ({
      businessName,
      city,
      country,
      email,
      rutList,
      state,
      taxIdList,
    }: {
      businessName: string;
      city: string;
      country: string;
      email: string;
      rutList: FileList | undefined;
      state: string;
      taxIdList: FileList | undefined;
    }): Promise<void> => {
      const rut = handleFileListUpload(rutList);
      const taxId = handleFileListUpload(taxIdList);
      mixpanel.track("AddPaymentMethod", { method: "Wired" });
      await addOtherPaymentMethod({
        variables: {
          businessName,
          city,
          country,
          email,
          organizationId,
          rut,
          state,
          taxId,
        },
      });
    },
    [addOtherPaymentMethod, organizationId]
  );

  return (
    <Modal
      maxWidth={"450px"}
      minWidth={350}
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.add.title")}
    >
      <Container>
        <FormikSelect
          field={{
            name: "paymentType",
            onBlur: (): void => undefined,
            onChange: (event: React.ChangeEvent<HTMLInputElement>): void => {
              const { value } = event.target;
              setPaymentType(value);
            },
            value: paymentType,
          }}
          form={{ errors: {}, isSubmitting: false, touched: {} }}
          label={t("organization.tabs.billing.paymentMethods.add.label")}
          name={"paymentType"}
        >
          <option value={""}>{""}</option>
          <option value={"CREDIT_CARD"}>
            {t(
              "organization.tabs.billing.paymentMethods.paymentType.creditCard"
            )}
          </option>
          <option value={"OTHER"}>
            {t(
              "organization.tabs.billing.paymentMethods.paymentType.otherMethod"
            )}
          </option>
        </FormikSelect>
      </Container>
      {paymentType === "" ? undefined : (
        <Container>
          {paymentType === "CREDIT_CARD" ? (
            <Elements stripe={stripePromise}>
              <AddCreditCardModal
                onClose={onClose}
                organizationId={organizationId}
              />
            </Elements>
          ) : (
            <AddOtherMethodModal
              onClose={onClose}
              onSubmit={handleAddOtherMethodSubmit}
            />
          )}
        </Container>
      )}
    </Modal>
  );
};

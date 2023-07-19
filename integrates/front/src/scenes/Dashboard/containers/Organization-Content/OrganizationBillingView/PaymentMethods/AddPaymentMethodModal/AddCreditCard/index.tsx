import { useMutation } from "@apollo/client";
import { CardElement, useElements, useStripe } from "@stripe/react-stripe-js";
import type { StripeElementChangeEvent } from "@stripe/stripe-js/types/stripe-js/elements";
import { Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { Container } from "./styles";

import { GET_ORGANIZATION_BILLING } from "../../../queries";
import { ADD_CREDIT_CARD_PAYMENT_METHOD } from "../queries";
import { Alert } from "components/Alert";
import { Checkbox } from "components/Input";
import { Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IAddCreditCardModalProps {
  organizationId: string;
  onClose: () => void;
}

export const AddCreditCardModal = ({
  organizationId,
  onClose,
}: IAddCreditCardModalProps): JSX.Element => {
  const { t } = useTranslation();

  const stripe = useStripe();
  const elements = useElements();
  const [errorMessage, setErrorMessage] = useState<string | undefined>();
  const [disabled, setDisabled] = useState(true);
  const options = { hidePostalCode: true };

  const [addCreditCardPaymentMethod] = useMutation(
    ADD_CREDIT_CARD_PAYMENT_METHOD,
    {
      onCompleted: (): void => {
        onClose();
        msgSuccess(
          t("organization.tabs.billing.paymentMethods.add.success.body"),
          t("organization.tabs.billing.paymentMethods.add.success.title")
        );
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          if (
            error.message ===
            "Exception - Provided payment method could not be created"
          ) {
            msgError(
              t(
                "organization.tabs.billing.paymentMethods.add.errors.couldNotBeCreated"
              )
            );
          } else {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't create payment method", error);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_ORGANIZATION_BILLING,
          variables: {
            organizationId,
          },
        },
      ],
    }
  );

  const handleChange = useCallback((event: StripeElementChangeEvent): void => {
    setErrorMessage(event.error?.message);
    setDisabled(!event.complete);
  }, []);

  const addCreditCard = useCallback(
    async (values: { makeDefault: boolean }): Promise<void> => {
      if (stripe && elements) {
        const result = await stripe.createPaymentMethod({
          elements,
        });
        setErrorMessage(result.error?.message);
        if (result.error === undefined) {
          mixpanel.track("AddPaymentMethod", { method: "TC" });
          await addCreditCardPaymentMethod({
            variables: {
              makeDefault: values.makeDefault,
              organizationId,
              paymentMethodId: result.paymentMethod.id,
            },
          });
        }
      }
    },
    [addCreditCardPaymentMethod, elements, organizationId, stripe]
  );

  if (!stripe || !elements) {
    return <div />;
  }

  return (
    <Container>
      <Formik
        initialValues={{
          makeDefault: false,
        }}
        name={"addCreditCardPaymentMethod"}
        onSubmit={addCreditCard}
      >
        <Form>
          <Row>
            <Container>
              <CardElement onChange={handleChange} options={options} />
            </Container>
            <Alert show={errorMessage !== undefined} variant={"error"}>
              {errorMessage}
            </Alert>
          </Row>
          <Row>
            <Checkbox
              label={t(
                "organization.tabs.billing.paymentMethods.add.creditCard.default"
              )}
              name={"makeDefault"}
            />
          </Row>
          <ModalConfirm
            disabled={disabled}
            id={"add-credit-card-method-confirm"}
            onCancel={onClose}
            onConfirm={"submit"}
          />
        </Form>
      </Formik>
    </Container>
  );
};

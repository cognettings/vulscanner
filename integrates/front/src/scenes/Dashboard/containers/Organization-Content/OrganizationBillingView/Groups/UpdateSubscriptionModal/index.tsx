import { Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Input, Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import type { IPaymentMethodAttr } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/types";

interface IUpdateSubscriptionProps {
  current: string;
  groupName: string;
  onClose: () => void;
  onSubmit: (values: {
    paymentId: string | null;
    subscription: string;
  }) => Promise<void>;
  paymentId: string | null;
  paymentMethods: IPaymentMethodAttr[];
  permissions: string[];
}

const validations = object().shape({
  paymentId: string().required(),
  subscription: string().required(),
});

export const UpdateSubscriptionModal: React.FC<IUpdateSubscriptionProps> = ({
  current,
  groupName,
  onClose,
  onSubmit,
  paymentId,
  paymentMethods,
  permissions,
}: IUpdateSubscriptionProps): JSX.Element => {
  const { t } = useTranslation();
  const subs = ["FREE", "MACHINE", "SQUAD"];
  const initialValue = subs.includes(current) ? current : "";

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.groups.updateSubscription.title")}
    >
      <Formik
        initialValues={{
          groupName,
          paymentId,
          subscription: initialValue,
        }}
        name={"updateSubscription"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {(): JSX.Element => (
          <Form>
            <div className={"flex flex-wrap w-100"}>
              <Input
                disabled={true}
                label={t("organization.tabs.billing.groups.name")}
                name={"groupName"}
                value={groupName}
              />
            </div>
            <div className={"pt2"}>
              <Select
                label={t("organization.tabs.billing.groups.paymentMethod")}
                name={"paymentId"}
                required={true}
              >
                <option value={""} />
                {paymentMethods.map(
                  (method): JSX.Element => (
                    <option key={method.id} value={method.id}>{`${
                      method.lastFourDigits === ""
                        ? `${method.country}, ${method.businessName}`
                        : `${method.brand}, ${method.lastFourDigits}`
                    }`}</option>
                  )
                )}
              </Select>
            </div>
            <div className={"pt2"}>
              <Select
                disabled={
                  !permissions.includes(
                    "api_mutations_update_subscription_mutate"
                  )
                }
                label={t(
                  "organization.tabs.billing.groups.updateSubscription.subscription"
                )}
                name={"subscription"}
                required={true}
              >
                <option value={""} />
                {subs.map(
                  (sub: string): JSX.Element => (
                    <option key={sub} value={sub}>
                      {t(
                        `organization.tabs.billing.groups.updateSubscription.types.${sub.toLowerCase()}`
                      )}
                    </option>
                  )
                )}
              </Select>
            </div>
            <ModalConfirm disabled={true} onCancel={onClose} />
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

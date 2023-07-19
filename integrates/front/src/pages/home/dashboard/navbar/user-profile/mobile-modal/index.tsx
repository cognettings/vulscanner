/* eslint-disable jsx-a11y/no-autofocus */
import { useMutation, useQuery } from "@apollo/client";
import { Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IPhoneData } from "components/Input/utils";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Can } from "context/authz/Can";
import { PhoneField } from "pages/home/dashboard/navbar/user-profile/mobile-modal/phone-field";
import {
  GET_STAKEHOLDER_PHONE,
  UPDATE_STAKEHOLDER_PHONE_MUTATION,
  VERIFY_STAKEHOLDER_MUTATION,
} from "pages/home/dashboard/navbar/user-profile/mobile-modal/queries";
import type {
  IAdditionFormValues,
  IEditionFormValues,
  IGetStakeholderPhoneAttr,
  IMobileModalProps,
  IPhoneAttr,
  IUpdateStakeholderPhoneResultAttr,
  IVerifyAdditionCodeFormValues,
  IVerifyEditionFormValues,
  IVerifyStakeholderResultAttr,
} from "pages/home/dashboard/navbar/user-profile/mobile-modal/types";
import { VerificationCodeField } from "pages/home/dashboard/navbar/user-profile/mobile-modal/verification-code-field";
import { GET_USER } from "scenes/Dashboard/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const MobileModal: React.FC<IMobileModalProps> = ({ onClose }): JSX.Element => {
  const { t } = useTranslation();
  const [isAdding, setIsAdding] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isOpenEdit, setIsOpenEdit] = useState(false);
  const [isCodeInCurrentMobile, setIsCodeInCurrentMobile] = useState(false);
  const [isCodeInNewMobile, setIsCodeInNewMobile] = useState(false);
  const [currentMobileVerificationCode, setCurrentMobileVerificationCode] =
    useState("");
  const [phoneToAdd, setPhoneToAdd] = useState<IPhoneData | undefined>(
    undefined
  );
  const [phoneToEdit, setPhoneToEdit] = useState<IPhoneData | undefined>(
    undefined
  );

  // GraphQL operations
  const [handleUpdateStakeholderPhone] =
    useMutation<IUpdateStakeholderPhoneResultAttr>(
      UPDATE_STAKEHOLDER_PHONE_MUTATION,
      {
        onCompleted: (data): void => {
          if (data.updateStakeholderPhone.success && isAdding) {
            msgSuccess(
              t("profile.mobileModal.alerts.additionSuccess"),
              t("groupAlerts.titleSuccess")
            );
            setIsAdding(false);
            setIsCodeInNewMobile(false);
            setPhoneToAdd(undefined);
          }
          if (data.updateStakeholderPhone.success && isEditing) {
            msgSuccess(
              t("profile.mobileModal.alerts.editionSuccess"),
              t("groupAlerts.titleSuccess")
            );
            setIsOpenEdit(false);
            setIsEditing(false);
            setIsCodeInCurrentMobile(false);
            setIsCodeInNewMobile(false);
            setPhoneToEdit(undefined);
          }
        },
        onError: (errors): void => {
          errors.graphQLErrors.forEach((error): void => {
            switch (error.message) {
              case "Exception - A mobile number is required with the international format":
                msgError(t("profile.mobileModal.alerts.requiredMobile"));
                break;
              case "Exception - Stakeholder could not be verified":
                msgError(
                  t("profile.mobileModal.alerts.nonVerifiedStakeholder")
                );
                break;
              case "Exception - The verification code is invalid":
                msgError(
                  t("profile.mobileModal.alerts.invalidVerificationCode")
                );
                break;
              default:
                msgError(t("groupAlerts.errorTextsad"));
                Logger.warning(
                  "An error occurred updating stakeholder phone",
                  error
                );
            }
          });
        },
        refetchQueries: [{ query: GET_STAKEHOLDER_PHONE }, { query: GET_USER }],
      }
    );
  const [handleVerifyStakeholder] = useMutation<IVerifyStakeholderResultAttr>(
    VERIFY_STAKEHOLDER_MUTATION,
    {
      onCompleted: (data): void => {
        if (data.verifyStakeholder.success && isAdding) {
          msgSuccess(
            t("profile.mobileModal.alerts.sendNewMobileVerificationSuccess"),
            t("groupAlerts.titleSuccess")
          );
          setIsCodeInNewMobile(true);
        }
        if (data.verifyStakeholder.success && isOpenEdit && !isEditing) {
          msgSuccess(
            t(
              "profile.mobileModal.alerts.sendCurrentMobileVerificationSuccess"
            ),
            t("groupAlerts.titleSuccess")
          );
          setIsCodeInCurrentMobile(true);
        }
        if (data.verifyStakeholder.success && isEditing) {
          msgSuccess(
            t("profile.mobileModal.alerts.sendNewMobileVerificationSuccess"),
            t("groupAlerts.titleSuccess")
          );
          setIsCodeInNewMobile(true);
        }
      },
      onError: (errors): void => {
        errors.graphQLErrors.forEach((error): void => {
          switch (error.message) {
            case "Exception - A mobile number is required with the international format":
            case "Exception - A new phone number is required":
              msgError(t("profile.mobileModal.alerts.requiredMobile"));
              break;
            case "Exception - Stakeholder could not be verified":
              msgError(t("profile.mobileModal.alerts.nonVerifiedStakeholder"));
              break;
            case "Exception - The verification code is invalid":
              msgError(t("profile.mobileModal.alerts.invalidVerificationCode"));
              break;
            case "Exception - The verification code is required":
              msgError(
                t("profile.mobileModal.alerts.requiredVerificationCode")
              );
              break;
            case "Exception - Stakeholder verification could not be started":
              msgError(t("profile.mobileModal.alerts.nonSentVerificationCode"));
              break;
            case "Exception - The new phone number is the current phone number":
              msgError(t("profile.mobileModal.alerts.sameMobile"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred updating stakeholder phone",
                error
              );
          }
        });
      },
    }
  );

  const handleAdd = useCallback(
    (values: IAdditionFormValues): void => {
      setPhoneToAdd(values.phone);
      setIsAdding(true);
      setIsCodeInNewMobile(false);
      void handleVerifyStakeholder({
        variables: {
          newPhone: {
            callingCountryCode: values.phone.callingCountryCode,
            nationalNumber: values.phone.nationalNumber,
          },
        },
      });
    },
    [handleVerifyStakeholder]
  );

  const handleVerifyAdditionCode = useCallback(
    (values: IVerifyAdditionCodeFormValues): void => {
      void handleUpdateStakeholderPhone({
        variables: {
          newPhone: {
            callingCountryCode: phoneToAdd?.callingCountryCode,
            nationalNumber: phoneToAdd?.nationalNumber,
          },
          verificationCode: values.newVerificationCode,
        },
      });
    },
    [handleUpdateStakeholderPhone, phoneToAdd]
  );

  function handleOpenEdit(): void {
    setIsOpenEdit(true);
    setIsCodeInCurrentMobile(false);
    void handleVerifyStakeholder();
  }

  const handleEdit = useCallback(
    (values: IEditionFormValues): void => {
      setPhoneToEdit(values.newPhone);
      setCurrentMobileVerificationCode(values.verificationCode);
      setIsEditing(true);
      setIsCodeInNewMobile(false);
      void handleVerifyStakeholder({
        variables: {
          newPhone: {
            callingCountryCode: values.newPhone.callingCountryCode,
            nationalNumber: values.newPhone.nationalNumber,
          },
          verificationCode: values.verificationCode,
        },
      });
    },
    [handleVerifyStakeholder]
  );

  const handleVerifyEditionCode = useCallback(
    (values: IVerifyEditionFormValues): void => {
      void handleUpdateStakeholderPhone({
        variables: {
          newPhone: {
            callingCountryCode: phoneToEdit?.callingCountryCode,
            nationalNumber: phoneToEdit?.nationalNumber,
          },
          verificationCode: values.newVerificationCode,
        },
      });
    },
    [handleUpdateStakeholderPhone, phoneToEdit]
  );

  const { data } = useQuery<IGetStakeholderPhoneAttr>(GET_STAKEHOLDER_PHONE, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("Couldn't load stakeholder's phone", error);
      });
    },
  });
  const phone = useMemo(
    (): IPhoneAttr | null => (_.isUndefined(data) ? null : data.me.phone),
    [data]
  );

  return (
    <Modal open={true} title={t("profile.mobileModal.title")}>
      {!(isAdding && isCodeInNewMobile) && _.isNull(phone) ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            phone: {
              callingCountryCode: "57",
              countryCode: "co",
              nationalNumber: "",
            },
          }}
          name={"addPhone"}
          onSubmit={handleAdd}
        >
          <Form id={"addPhone"}>
            <Row>
              <Col>
                <PhoneField autoFocus={true} />
              </Col>
            </Row>
            <Can do={"api_mutations_update_stakeholder_phone_mutate"}>
              <ModalConfirm
                onCancel={onClose}
                txtConfirm={t("profile.mobileModal.add")}
              />
            </Can>
          </Form>
        </Formik>
      ) : undefined}
      {isAdding && isCodeInNewMobile && !_.isUndefined(phoneToAdd) ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            newVerificationCode: "",
            phone: phoneToAdd,
          }}
          name={"verifyAdditionCode"}
          onSubmit={handleVerifyAdditionCode}
          validationSchema={object().shape({
            newVerificationCode: string().required(t("validations.required")),
          })}
        >
          <Form id={"verifyAdditionCode"}>
            <Row>
              <Col>
                <PhoneField disabled={true} />
              </Col>
            </Row>
            <Col>
              <VerificationCodeField name={"newVerificationCode"} />
            </Col>
            <ModalConfirm
              onCancel={onClose}
              txtConfirm={t("profile.mobileModal.verify")}
            />
          </Form>
        </Formik>
      ) : undefined}
      {!_.isNull(phone) && !isCodeInNewMobile ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            newPhone: {
              callingCountryCode: phone.callingCountryCode,
              countryCode: phone.countryCode.toLowerCase(),
              nationalNumber: "",
            },
            phone: {
              callingCountryCode: phone.callingCountryCode,
              countryCode: phone.countryCode.toLowerCase(),
              nationalNumber: phone.nationalNumber,
            },
            verificationCode: "",
          }}
          name={"editPhone"}
          onSubmit={handleEdit}
          validationSchema={object().shape({
            verificationCode: string().required(t("validations.required")),
          })}
        >
          <Form id={"editPhone"}>
            <Row>
              <Col>
                <PhoneField disabled={true} />
              </Col>
            </Row>
            {isOpenEdit && isCodeInCurrentMobile ? (
              <React.Fragment>
                <Row>
                  <Col>
                    <VerificationCodeField />
                  </Col>
                </Row>
                <Row>
                  <Col>
                    <PhoneField
                      label={"profile.mobileModal.fields.newPhoneNumber"}
                      name={"newPhone"}
                    />
                  </Col>
                </Row>
              </React.Fragment>
            ) : undefined}
            <Can do={"api_mutations_update_stakeholder_phone_mutate"}>
              <ModalConfirm
                onCancel={onClose}
                onConfirm={
                  isOpenEdit && isCodeInCurrentMobile
                    ? "submit"
                    : handleOpenEdit
                }
                txtConfirm={t("profile.mobileModal.edit")}
              />
            </Can>
          </Form>
        </Formik>
      ) : undefined}
      {isEditing &&
      !_.isNull(phone) &&
      isCodeInNewMobile &&
      !_.isUndefined(phoneToEdit) ? (
        <Formik
          enableReinitialize={true}
          initialValues={{
            newPhone: {
              callingCountryCode: phoneToEdit.callingCountryCode,
              countryCode: phoneToEdit.countryCode.toLowerCase(),
              nationalNumber: phoneToEdit.nationalNumber,
            },
            newVerificationCode: "",
            phone: {
              callingCountryCode: phone.callingCountryCode,
              countryCode: phone.countryCode.toLowerCase(),
              nationalNumber: phone.nationalNumber,
            },
            verificationCode: currentMobileVerificationCode,
          }}
          name={"verifyEditionCode"}
          onSubmit={handleVerifyEditionCode}
          validationSchema={object().shape({
            newVerificationCode: string().required(t("validations.required")),
            verificationCode: string().required(t("validations.required")),
          })}
        >
          <Form id={"verifyEditionCode"}>
            <Row>
              <Col>
                <PhoneField disabled={true} />
              </Col>
            </Row>
            <Row>
              <Col>
                <VerificationCodeField disabled={true} />
              </Col>
            </Row>
            <Row>
              <Col>
                <PhoneField
                  disabled={true}
                  label={"profile.mobileModal.fields.newPhoneNumber"}
                  name={"newPhone"}
                />
              </Col>
            </Row>
            <Row>
              <Col>
                <VerificationCodeField name={"newVerificationCode"} />
              </Col>
            </Row>
            <ModalConfirm
              onCancel={onClose}
              txtConfirm={t("profile.mobileModal.verify")}
            />
          </Form>
        </Formik>
      ) : undefined}
    </Modal>
  );
};

export { MobileModal };

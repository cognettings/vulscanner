/* eslint-disable jsx-a11y/no-noninteractive-element-interactions */
import { Form, Formik } from "formik";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { mixed, object, string } from "yup";

import { Input, InputFile, Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { getCountries } from "utils/countries";
import type { ICountry } from "utils/countries";

interface IUpdateOtherMethodModalProps {
  onClose: () => void;
  onSubmit: (values: {
    businessName: string;
    city: string;
    country: string;
    email: string;
    rutList: FileList | undefined;
    state: string;
    taxIdList: FileList | undefined;
  }) => Promise<void>;
  initialValues: {
    businessName: string;
    city: string;
    country: string;
    email: string;
    rutList: FileList | undefined;
    state: string;
    taxIdList: FileList | undefined;
  };
}

export const UpdateOtherMethodModal: React.FC<IUpdateOtherMethodModalProps> = ({
  onClose,
  onSubmit,
  initialValues,
}: IUpdateOtherMethodModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [countries, setCountries] = useState<ICountry[]>([]);
  const [states, setStates] = useState<string[]>([]);
  const [cities, setCities] = useState<string[]>([]);

  const validations = object().shape({
    businessName: string()
      .required()
      .max(60)
      .matches(
        /^[a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@_$#!,.*\-?"[\]|()/{}>][a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s'~:;%@_$#!,.*\-?"[\]|()/{}>=]+$/u
      ),
    city: string().test(
      "isRequired",
      t("validations.required"),
      (value): boolean => {
        return cities.length === 0 || value !== undefined;
      }
    ),
    country: string().required(),
    email: string().email().when("country", {
      is: "Colombia",
      otherwise: string(),
      then: string().email().required(),
    }),
    rutList: mixed().when("country", {
      is: "Colombia",
      otherwise: mixed(),
      then: mixed().required(),
    }),
    state: string().test(
      "isRequired",
      t("validations.required"),
      (value): boolean => {
        return states.length === 0 || value !== undefined;
      }
    ),
    taxIdList: mixed().when("country", {
      is: "Colombia",
      otherwise: mixed().required(),
      then: mixed(),
    }),
  });

  useEffect((): void => {
    const loadCountries = async (): Promise<void> => {
      setCountries(await getCountries());
    };
    void loadCountries();
  }, [setCountries]);

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.update.modal.update")}
    >
      <Formik
        initialValues={initialValues}
        name={"addOtherMethods"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting, setFieldValue, values }): JSX.Element => {
          function changeCountry(): void {
            setFieldValue("state", "");
            setFieldValue("city", "");
            setCities([]);
            if (values.country !== "") {
              setStates(
                countries
                  .filter(
                    (country): boolean => country.name === values.country
                  )[0]
                  .states.map((state): string => state.name)
              );
            }
          }
          function changeState(): void {
            setFieldValue("city", "");
            if (values.country !== "" && values.state !== "") {
              setCities(
                countries
                  .filter(
                    (country): boolean => country.name === values.country
                  )[0]
                  .states.filter(
                    (state): boolean => state.name === values.state
                  )[0]
                  .cities.map((city): string => city.name)
              );
            }
          }

          return (
            <Form>
              <div>
                <Input
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.otherMethods.businessName"
                  )}
                  name={"businessName"}
                  required={true}
                  type={"text"}
                />
              </div>
              <div
                onClick={changeCountry}
                onKeyDown={changeCountry}
                role={"listitem"}
              >
                <Select
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.otherMethods.country"
                  )}
                  name={"country"}
                  required={true}
                >
                  <option value={""}>{""}</option>
                  {countries.map(
                    (country): JSX.Element => (
                      <option key={country.id} value={country.name}>
                        {country.name}
                      </option>
                    )
                  )}
                </Select>
              </div>
              {states.length > 0 ? (
                <div
                  onClick={changeState}
                  onKeyDown={changeState}
                  role={"listitem"}
                >
                  <Select
                    label={t(
                      "organization.tabs.billing.paymentMethods.add.otherMethods.state"
                    )}
                    name={"state"}
                    required={true}
                  >
                    <option value={""}>{""}</option>
                    {states.map(
                      (state): JSX.Element => (
                        <option key={state} value={state}>
                          {state}
                        </option>
                      )
                    )}
                  </Select>
                </div>
              ) : undefined}
              {cities.length > 0 ? (
                <Select
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.otherMethods.city"
                  )}
                  name={"city"}
                  required={true}
                >
                  <option value={""}>{""}</option>
                  {cities.map(
                    (city): JSX.Element => (
                      <option key={city} value={city}>
                        {city}
                      </option>
                    )
                  )}
                </Select>
              ) : undefined}
              {values.country === "Colombia" ? (
                <React.Fragment>
                  <div>
                    <Input
                      label={t(
                        "organization.tabs.billing.paymentMethods.add.otherMethods.email"
                      )}
                      name={"email"}
                      required={true}
                      type={"text"}
                    />
                  </div>
                  <div>
                    <InputFile
                      accept={
                        "application/pdf,application/zip,image/gif,image/jpg,image/png"
                      }
                      id={"rut"}
                      label={t(
                        "organization.tabs.billing.paymentMethods.add.otherMethods.rut"
                      )}
                      name={"rutList"}
                      required={true}
                    />
                  </div>
                </React.Fragment>
              ) : (
                <div>
                  <InputFile
                    accept={
                      "application/pdf,application/zip,image/gif,image/jpg,image/png"
                    }
                    id={"taxId"}
                    label={t(
                      "organization.tabs.billing.paymentMethods.add.otherMethods.taxId"
                    )}
                    name={"taxIdList"}
                    required={true}
                  />
                </div>
              )}
              <ModalConfirm
                disabled={!dirty || isSubmitting}
                onCancel={onClose}
              />
            </Form>
          );
        }}
      </Formik>
    </Modal>
  );
};

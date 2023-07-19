import { useFormikContext } from "formik";
import type { FC } from "react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IHealthCheckProps } from "./types";

import type { IFormValues } from "../../../../../types";
import { formatStringHealthCheck } from "../../../../../utils";
import { updateHealthCheckConfirm } from "../utils";
import { Alert } from "components/Alert";
import { Checkbox } from "components/Input";
import { RadioGroup } from "components/Input/Fields/RadioGroup";
import { Row } from "components/Layout";
import { Have } from "context/authz/Have";

const HealthCheckSection: FC<IHealthCheckProps> = ({
  form,
  isEditing,
  isSameHealthCheck,
  setIsSameHealthCheck,
}: Readonly<IHealthCheckProps>): JSX.Element => {
  const { t } = useTranslation();
  const { initialValues, setFieldValue, values } =
    useFormikContext<IFormValues>();

  const onChangeHealthCheck = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      const includesHealthCheckValue = event.target.value;
      setFieldValue("healthCheckConfirm", []);
      updateHealthCheckConfirm(
        form,
        initialValues,
        isEditing,
        setIsSameHealthCheck,
        undefined,
        undefined,
        includesHealthCheckValue
      );
    },
    [form, initialValues, isEditing, setFieldValue, setIsSameHealthCheck]
  );

  return (
    <Have I={"has_squad"}>
      <Row id={"git-root-add-health-check"}>
        <div>
          <RadioGroup
            fw={"bold"}
            label={t("group.scope.git.healthCheck.confirm")}
            name={"includesHealthCheck"}
            onChange={onChangeHealthCheck}
            options={[
              {
                header: "Yes",
                value: "yes",
              },
              {
                header: "No",
                value: "no",
              },
            ]}
            required={true}
            tooltip={t("group.scope.git.healthCheck.tooltip")}
            value={formatStringHealthCheck(values.includesHealthCheck)}
          />
        </div>
        {!isSameHealthCheck &&
        (values.includesHealthCheck === "yes" ||
          values.includesHealthCheck === true) ? (
          <Alert>
            <Checkbox
              label={t("group.scope.git.healthCheck.accept")}
              name={"healthCheckConfirm"}
              required={true}
              value={"includeA"}
            />
          </Alert>
        ) : undefined}
        {!isSameHealthCheck &&
        (values.includesHealthCheck === "no" ||
          values.includesHealthCheck === false) ? (
          <Alert>
            <div>
              <Checkbox
                label={t("group.scope.git.healthCheck.rejectA")}
                name={"healthCheckConfirm"}
                required={true}
                value={"rejectA"}
              />
              <Checkbox
                label={t("group.scope.git.healthCheck.rejectB")}
                name={"healthCheckConfirm"}
                required={true}
                value={"rejectB"}
              />
              <Checkbox
                label={t("group.scope.git.healthCheck.rejectC")}
                name={"healthCheckConfirm"}
                required={true}
                value={"rejectC"}
              />
            </div>
          </Alert>
        ) : undefined}
      </Row>
    </Have>
  );
};

export type { IHealthCheckProps };
export { HealthCheckSection };

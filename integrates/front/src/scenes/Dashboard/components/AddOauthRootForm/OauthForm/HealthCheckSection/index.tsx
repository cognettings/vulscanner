import { useFormikContext } from "formik";
import type { FC } from "react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../../types";
import { Alert } from "components/Alert";
import { Container } from "components/Container";
import { Checkbox } from "components/Input";
import { RadioGroup } from "components/Input/Fields/RadioGroup";
import { Row } from "components/Layout";
import { Have } from "context/authz/Have";

const HealthCheckSection: FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { isSubmitting, setFieldValue, values } =
    useFormikContext<IFormValues>();

  const onChangeHealthCheck = useCallback(
    (_: React.ChangeEvent<HTMLInputElement>): void => {
      setFieldValue("healthCheckConfirm", []);
    },
    [setFieldValue]
  );

  return (
    <Have I={"has_squad"}>
      <Container margin={"24px 0 0 0"} scroll={"none"}>
        <Row>
          <div>
            <RadioGroup
              disabled={isSubmitting}
              fw={"bold"}
              label={t("components.oauthRootForm.steps.s3.healthCheck.confirm")}
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
              tooltip={t(
                "components.oauthRootForm.steps.s3.healthCheck.tooltip"
              )}
              value={values.includesHealthCheck}
            />
          </div>
          {values.includesHealthCheck === "yes" ? (
            <Alert>
              <Checkbox
                disabled={isSubmitting}
                label={t(
                  "components.oauthRootForm.steps.s3.healthCheck.accept"
                )}
                name={"healthCheckConfirm"}
                required={true}
                value={"includeA"}
              />
            </Alert>
          ) : undefined}
          {values.includesHealthCheck === "no" ? (
            <Alert>
              <div>
                <Checkbox
                  disabled={isSubmitting}
                  label={t(
                    "components.oauthRootForm.steps.s3.healthCheck.rejectA"
                  )}
                  name={"healthCheckConfirm"}
                  required={true}
                  value={"rejectA"}
                />
                <Checkbox
                  disabled={isSubmitting}
                  label={t(
                    "components.oauthRootForm.steps.s3.healthCheck.rejectB"
                  )}
                  name={"healthCheckConfirm"}
                  required={true}
                  value={"rejectB"}
                />
                <Checkbox
                  disabled={isSubmitting}
                  label={t(
                    "components.oauthRootForm.steps.s3.healthCheck.rejectC"
                  )}
                  name={"healthCheckConfirm"}
                  required={true}
                  value={"rejectC"}
                />
              </div>
            </Alert>
          ) : undefined}
        </Row>
      </Container>
    </Have>
  );
};

export { HealthCheckSection };

import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useFormikContext } from "formik";
import type { FC } from "react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IRootAttr } from "../../../types";
import { QuestionButton } from "../../styles";
import { Alert } from "components/Alert";
import { Container } from "components/Container";
import { InputArray } from "components/Input";
import { RadioGroup } from "components/Input/Fields/RadioGroup";
import { Row } from "components/Layout";
import { Text } from "components/Text";
import { openUrl } from "utils/resourceHelpers";

const Exclusions: FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { setFieldValue, values } = useFormikContext<IRootAttr>();

  const goToDocumentation = useCallback((): void => {
    openUrl(
      "https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitignore.html#_pattern_format"
    );
  }, []);

  const onChangeHasExclusions = useCallback((): void => {
    setFieldValue("exclusions", []);
  }, [setFieldValue]);

  return (
    <Row>
      <RadioGroup
        fw={"bold"}
        label={t("autoenrollment.exclusions.label")}
        name={"hasExclusions"}
        onChange={onChangeHasExclusions}
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
        tooltip={t("autoenrollment.exclusions.tooltip")}
        value={values.hasExclusions}
      />
      {values.hasExclusions === "yes" ? (
        <div>
          <Container margin={"10px 0 10px 0"}>
            <Alert>{t("autoenrollment.exclusions.warning")}</Alert>
          </Container>
          <Container margin={"0 0 10px 0"}>
            <Text bright={7} tone={"dark"}>
              <QuestionButton onClick={goToDocumentation}>
                <FontAwesomeIcon icon={faQuestionCircle} />
              </QuestionButton>
              &nbsp;
              {t("autoenrollment.exclusions.exclude")}
            </Text>
          </Container>
          <InputArray
            addButtonText={t("autoenrollment.exclusions.addExclusion")}
            initEmpty={false}
            initValue={""}
            name={"exclusions"}
            placeholder={t("autoenrollment.exclusions.placeholder")}
          />
        </div>
      ) : undefined}
    </Row>
  );
};

export { Exclusions };

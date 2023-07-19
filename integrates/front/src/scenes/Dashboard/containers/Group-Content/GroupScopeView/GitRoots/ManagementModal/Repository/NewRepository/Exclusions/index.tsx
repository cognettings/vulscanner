import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useFormikContext } from "formik";
import _ from "lodash";
import type { FC } from "react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../../../../../types";
import { QuestionButton } from "../../../../styles";
import { Alert } from "components/Alert";
import { Container } from "components/Container";
import { InputArray } from "components/Input";
import { RadioGroup } from "components/Input/Fields/RadioGroup";
import { Row } from "components/Layout";
import { Text } from "components/Text";
import { Can } from "context/authz/Can";
import { openUrl } from "utils/resourceHelpers";

interface IExclusionsProps {
  isEditing: boolean;
  manyRows: boolean;
}

const Exclusions: FC<IExclusionsProps> = ({
  isEditing,
  manyRows,
}): JSX.Element => {
  const { t } = useTranslation();
  const { initialValues, setFieldValue, values } =
    useFormikContext<IFormValues>();

  const goToDocumentation = useCallback((): void => {
    openUrl(
      "https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitignore.html#_pattern_format"
    );
  }, []);

  const onChangeHasExclusions = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      const hasExclusions = event.target.value;
      if (isEditing && _.isEqual(hasExclusions, initialValues.hasExclusions)) {
        setFieldValue("gitignore", initialValues.gitignore);
      } else {
        setFieldValue("gitignore", []);
      }
    },
    [initialValues, isEditing, setFieldValue]
  );

  if (manyRows) {
    return <div />;
  }

  return (
    <Can do={"update_git_root_filter"}>
      <Row>
        <RadioGroup
          fw={"bold"}
          label={t("group.scope.git.filter.label")}
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
          tooltip={t("group.scope.git.filter.tooltip")}
          value={values.hasExclusions}
        />
        {values.hasExclusions === "yes" ? (
          <div>
            <Container margin={"10px 0 10px 0"}>
              <Alert>{t("group.scope.git.filter.warning")}</Alert>
            </Container>
            <Container margin={"0 0 10px 0"}>
              <Text bright={7} tone={"dark"}>
                <QuestionButton onClick={goToDocumentation}>
                  <FontAwesomeIcon icon={faQuestionCircle} />
                </QuestionButton>
                &nbsp;
                {t("group.scope.git.filter.exclude")}
              </Text>
            </Container>
            <InputArray
              addButtonText={t("group.scope.git.filter.addExclusion")}
              initEmpty={false}
              initValue={""}
              name={"gitignore"}
              placeholder={t("group.scope.git.filter.placeholder")}
            />
          </div>
        ) : undefined}
      </Row>
    </Can>
  );
};

export { Exclusions };

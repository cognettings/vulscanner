/* eslint-disable react/jsx-no-bind */
/* eslint-disable fp/no-mutation */
/* eslint-disable fp/no-mutating-methods */
import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { FieldArray, useFormikContext } from "formik";
import { isUndefined } from "lodash";
import type { FC } from "react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { PathsArray } from "./PathsArray";
import { QuestionButton } from "./styles";
import type { IExclusionsProps } from "./types";

import type { IFormValues } from "../../types";
import { Alert } from "components/Alert";
import { Container } from "components/Container";
import { RadioGroup } from "components/Input/Fields/RadioGroup";
import { Text } from "components/Text";
import { openUrl } from "utils/resourceHelpers";

const ExclusionsSection: FC<IExclusionsProps> = ({
  exclusionsArrayHelpersRef,
  repositories,
}): JSX.Element => {
  const { t } = useTranslation();
  const { isSubmitting, setFieldValue, values } =
    useFormikContext<IFormValues>();

  const goToDocumentation = useCallback((): void => {
    openUrl(
      "https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitignore.html#_pattern_format"
    );
  }, []);

  const onChangeHasExclusions = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      const hasExclusions = event.target.value;

      if (hasExclusions === "yes") {
        setFieldValue("gitignore", []);
        values.urls.map((_): void => {
          return exclusionsArrayHelpersRef.current?.push({ paths: [""] });
        });
      } else {
        setFieldValue("gitignore", []);
        values.urls.map((_): void => {
          return exclusionsArrayHelpersRef.current?.push({ paths: [] });
        });
      }
    },
    [exclusionsArrayHelpersRef, setFieldValue, values.urls]
  );

  return (
    <Container scroll={"none"}>
      <RadioGroup
        disabled={isSubmitting}
        fw={"bold"}
        label={t("components.oauthRootForm.steps.s3.exclusions.label")}
        name={"hasExclusions"}
        onChange={onChangeHasExclusions}
        options={[
          {
            header: t(
              "components.oauthRootForm.steps.s3.exclusions.radio.yes.label"
            ),
            value: t(
              "components.oauthRootForm.steps.s3.exclusions.radio.yes.value"
            ),
          },
          {
            header: t(
              "components.oauthRootForm.steps.s3.exclusions.radio.no.label"
            ),
            value: t(
              "components.oauthRootForm.steps.s3.exclusions.radio.no.value"
            ),
          },
        ]}
        required={true}
        tooltip={t("components.oauthRootForm.steps.s3.exclusions.tooltip")}
        value={values.hasExclusions}
      />
      <FieldArray
        name={"gitignore"}
        render={(arrayHelpers): JSX.Element => {
          exclusionsArrayHelpersRef.current = arrayHelpers;

          return (
            <Container scroll={"none"}>
              {values.hasExclusions === "yes" ? (
                <Container scroll={"none"}>
                  <Container margin={"10px 0 10px 0"}>
                    <Alert>
                      {t(
                        "components.oauthRootForm.steps.s3.exclusions.warning"
                      )}
                    </Alert>
                  </Container>
                  <Container margin={"0 0 10px 0"}>
                    <Text bright={7} tone={"dark"}>
                      <QuestionButton onClick={goToDocumentation}>
                        <FontAwesomeIcon icon={faQuestionCircle} />
                      </QuestionButton>
                      &nbsp;
                      {t(
                        "components.oauthRootForm.steps.s3.exclusions.exclude"
                      )}
                    </Text>
                  </Container>
                  <div>
                    {values.urls.map((url, urlIndex): JSX.Element => {
                      const repo = repositories[url];

                      return isUndefined(values.gitignore[urlIndex].paths) ? (
                        <div key={repo.name} />
                      ) : (
                        <PathsArray
                          key={repo.name}
                          repo={repo}
                          urlIndex={urlIndex}
                        />
                      );
                    })}
                  </div>
                </Container>
              ) : undefined}
            </Container>
          );
        }}
      />
    </Container>
  );
};

export { ExclusionsSection };

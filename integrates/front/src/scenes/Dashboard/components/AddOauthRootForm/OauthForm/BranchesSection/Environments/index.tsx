/* eslint-disable react/jsx-no-bind */
/* eslint-disable fp/no-mutation */
import { FieldArray, useFormikContext } from "formik";
import _ from "lodash";
import React from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import type { IEnvironmentsProps } from "./types";

import type { IFormValues } from "../../../types";
import { Container } from "components/Container";
import { Input, Label } from "components/Input";

const Environments: FC<IEnvironmentsProps> = ({
  envsArrayHelpersRef,
}): JSX.Element => {
  const { t } = useTranslation();

  const { values } = useFormikContext<IFormValues>();

  return (
    <div>
      {_.isEmpty(values.urls) ? undefined : (
        <Container>
          <FieldArray
            name={"environments"}
            render={(arrayHelpers): JSX.Element => {
              envsArrayHelpersRef.current = arrayHelpers;

              return (
                <Container>
                  {values.urls.map((url, index): JSX.Element => {
                    return (
                      <Container
                        align={"center"}
                        display={"flex"}
                        key={url}
                        margin={"8px 8px 0 8px"}
                        minHeight={"43px"}
                        width={"auto"}
                      >
                        <Label
                          fw={"bold"}
                          htmlFor={"environments"}
                          required={true}
                          tooltip={t(
                            "components.oauthRootForm.steps.s1.environment.toolTip"
                          )}
                        >
                          {t(
                            "components.oauthRootForm.steps.s1.environment.text"
                          )}
                        </Label>
                        <Container margin={"0 0 0 8px"} width={"200px"}>
                          <Input
                            name={`environments.${index}`}
                            placeholder={t(
                              "components.oauthRootForm.steps.s1.environment.placeHolder"
                            )}
                          />
                        </Container>
                      </Container>
                    );
                  })}
                </Container>
              );
            }}
          />
        </Container>
      )}
    </div>
  );
};

export { Environments };

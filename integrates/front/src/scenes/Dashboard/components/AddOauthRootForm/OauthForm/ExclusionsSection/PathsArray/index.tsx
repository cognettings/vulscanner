/* eslint-disable fp/no-mutation */
/* eslint-disable react/jsx-no-bind */
/* eslint-disable fp/no-mutating-methods */
/* eslint-disable react/no-array-index-key */
import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FieldArray, useFormikContext } from "formik";
import React from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import type { IPathsArrayProps } from "./types";

import type { IFormValues } from "../../../types";
import { Button } from "components/Button";
import { Container } from "components/Container";
import { Input } from "components/Input";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";

const PathsArray: FC<IPathsArrayProps> = ({ repo, urlIndex }): JSX.Element => {
  const { t } = useTranslation();
  const { isSubmitting, values } = useFormikContext<IFormValues>();

  const gitIgnore = values.gitignore[urlIndex];

  return (
    <FieldArray
      name={`gitignore.${urlIndex}.paths`}
      render={(arrayHelpers): JSX.Element => {
        const addItem = (): (() => void) => (): void => {
          arrayHelpers.push("");
        };

        const removeItem =
          (index: number): (() => void) =>
          (): void => {
            arrayHelpers.remove(index);
          };

        return (
          <Container
            margin={`0 0 ${
              urlIndex + 1 === values.urls.length ? "0" : "24px"
            } 0`}
            scroll={"none"}
          >
            <Row>
              {gitIgnore.paths.map((_, excludeIndex): JSX.Element => {
                return (
                  <Col key={`field${excludeIndex}`} lg={80} md={80} sm={80}>
                    <Row align={"center"}>
                      <Col>
                        <Text
                          disp={"inline-block"}
                          fw={9}
                        >{`${repo.name}/${values.branches[urlIndex]}/`}</Text>
                      </Col>
                      <Col>
                        <Input
                          childRight={
                            gitIgnore.paths.length === 1 ? (
                              <div />
                            ) : (
                              <Button
                                disabled={isSubmitting}
                                icon={faTrashAlt}
                                onClick={removeItem(excludeIndex)}
                                size={"sm"}
                              />
                            )
                          }
                          disabled={isSubmitting}
                          name={`gitignore.${urlIndex}.paths.${excludeIndex}`}
                          placeholder={t(
                            "components.oauthRootForm.steps.s3.exclusions.placeholder"
                          )}
                        />
                      </Col>
                    </Row>
                  </Col>
                );
              })}
              <Col lg={20} md={20} sm={20}>
                <Button icon={faPlus} onClick={addItem()} size={"md"}>
                  {t(
                    "components.oauthRootForm.steps.s3.exclusions.addExclusion"
                  )}
                </Button>
              </Col>
            </Row>
          </Container>
        );
      }}
    />
  );
};

export { PathsArray };

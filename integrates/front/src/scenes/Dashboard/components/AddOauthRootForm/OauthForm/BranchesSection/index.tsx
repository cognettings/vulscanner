/* eslint-disable react/jsx-no-bind */
/* eslint-disable fp/no-mutation */
import { FieldArray, useFormikContext } from "formik";
import type { FC } from "react";
import React from "react";

import { Environments } from "./Environments";
import type { IBranchesSectionProps } from "./types";

import type { IFormValues } from "../../types";
import { Container } from "components/Container";
import { Select } from "components/Input";
import { Text } from "components/Text";

const BranchesSection: FC<IBranchesSectionProps> = ({
  branchesArrayHelpersRef,
  envsArrayHelpersRef,
  repositories,
}): JSX.Element => {
  const { values } = useFormikContext<IFormValues>();

  return (
    <Container
      bgColor={"#FFF"}
      border={"1px solid #F4F4F6"}
      br={"4px"}
      display={"flex"}
      margin={"10px 0 0 0"}
      pb={"24px"}
      pl={"24px"}
      pr={"24px"}
      pt={"24px"}
    >
      <FieldArray
        name={"branches"}
        render={(arrayHelpers): JSX.Element => {
          branchesArrayHelpersRef.current = arrayHelpers;

          return (
            <Container>
              {values.urls.map((url, index): JSX.Element => {
                const repo = repositories[url];

                return (
                  <Container
                    align={"center"}
                    display={"flex"}
                    justify={"space-between"}
                    key={url}
                    margin={"8px 8px 0 8px"}
                    width={"auto"}
                  >
                    <Text disp={"inline-block"} fw={9}>
                      {repo.name}
                    </Text>
                    <Container
                      margin={"0 0 0 8px"}
                      maxWidth={"150px"}
                      minWidth={"150px"}
                    >
                      <Select name={`branches.${index}`}>
                        <option value={""}>{""}</option>
                        {repo.branches.map((branch): JSX.Element => {
                          return (
                            <option key={branch} value={branch}>
                              {branch}
                            </option>
                          );
                        })}
                      </Select>
                    </Container>
                  </Container>
                );
              })}
            </Container>
          );
        }}
      />
      <Environments envsArrayHelpersRef={envsArrayHelpersRef} />
    </Container>
  );
};

export { BranchesSection };

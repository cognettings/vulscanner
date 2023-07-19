/* eslint-disable react/jsx-no-bind */
/* eslint-disable fp/no-mutation */
/* eslint-disable fp/no-mutating-methods */
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
import { useFormikContext } from "formik";
import type { FC } from "react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IRepositoriesSectionProps } from "./types";

import type { IFormValues } from "../../types";
import { Button } from "components/Button";
import { Container } from "components/Container";
import { Checkbox, Input } from "components/Input";

const RepositoriesSection: FC<IRepositoriesSectionProps> = ({
  branchesArrayHelpersRef,
  credentialName,
  envsArrayHelpersRef,
  exclusionsArrayHelpersRef,
  repositories,
}): JSX.Element => {
  const { t } = useTranslation();
  const { setFieldValue, values } = useFormikContext<IFormValues>();

  const cleanEnvironments = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      const repoToRemove = values.urls.findIndex(
        (url): boolean => event.target.value === url
      );
      if (repoToRemove >= 0) {
        envsArrayHelpersRef.current?.remove(repoToRemove);
        branchesArrayHelpersRef.current?.remove(repoToRemove);
        exclusionsArrayHelpersRef.current?.remove(repoToRemove);
      } else {
        exclusionsArrayHelpersRef.current?.push({ paths: [""] });
        envsArrayHelpersRef.current?.push("");
      }

      if (values.urls.length === 0) {
        setFieldValue("hasExclusions", "");
        setFieldValue("includesHealthCheck", "");
      }
    },
    [
      branchesArrayHelpersRef,
      envsArrayHelpersRef,
      exclusionsArrayHelpersRef,
      setFieldValue,
      values,
    ]
  );

  const filteredRepos = Object.values(repositories).filter((repo): boolean => {
    return (
      repo.name === "" ||
      repo.name.toLowerCase().includes(values.reposByName.toLowerCase())
    );
  });

  const selectAll = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      if (event.target.value === "true") {
        setFieldValue("allChecked", false);
        setFieldValue("urls", []);
        setFieldValue("environments", []);
        setFieldValue("branches", []);
        setFieldValue("gitignore", [{ paths: [] }]);
      }

      if (event.target.value === "false") {
        setFieldValue("allChecked", true);
        filteredRepos.forEach((repository, index): void => {
          setFieldValue(`urls.${index}`, repository.url);
        });
      }
    },
    [filteredRepos, setFieldValue]
  );

  return (
    <Container>
      <Container
        bgColor={"#FFF"}
        border={"1px solid #F4F4F6"}
        br={"4px"}
        pb={"24px"}
        pl={"24px"}
        pr={"24px"}
        pt={"24px"}
      >
        <Container margin={"0 0 10px 0"}>
          <Input
            bgColor={"#F4F4F6"}
            childLeft={<Button icon={faMagnifyingGlass} size={"xs"} />}
            name={"reposByName"}
            placeholder={t(
              "components.oauthRootForm.steps.s1.filter.placeHolder"
            )}
            variant={"outline"}
          />
        </Container>
        <Container
          border={"solid 1px #D4D4DB"}
          br={"5px"}
          scroll={"none"}
          width={"100%"}
        >
          <Container
            align={"center"}
            borderBottom={"solid 1px #D4D4DB"}
            display={"flex"}
            height={"50px"}
            pb={"5px"}
            pl={"5px"}
            pr={"5px"}
            pt={"5px"}
          >
            <Checkbox
              fw={"bold"}
              label={credentialName}
              name={"allChecked"}
              onChange={selectAll}
            />
          </Container>
          <Container
            display={"flex"}
            maxHeight={"130px"}
            minHeight={"130px"}
            pb={"5px"}
            pl={"5px"}
            pr={"5px"}
            pt={"5px"}
            wrap={"wrap"}
          >
            {filteredRepos.map(
              (repository): JSX.Element => (
                <Container
                  key={repository.name}
                  maxHeight={"24px"}
                  minHeight={"24px"}
                  width={"30%"}
                >
                  <Checkbox
                    label={`/${repository.name}`}
                    name={"urls"}
                    onChange={cleanEnvironments}
                    value={repository.url}
                  />
                </Container>
              )
            )}
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

export { RepositoriesSection };

import { faPlus } from "@fortawesome/free-solid-svg-icons";
import React from "react";
import { useTranslation } from "react-i18next";

import { RepoIcon } from "./styles";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Dropdown } from "components/Dropdown";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";
import {
  azureIcon,
  bitBucketIcon,
  gitHubIcon,
  gitLabIcon,
  squarePlusIcon,
} from "resources";

interface IRepositoryProps {
  isVisible: boolean;
  onClick: () => void;
  text?: string;
}

interface IRepositoriesDropdownProps {
  availableRepositories: {
    gitLab?: IRepositoryProps;
    gitHub?: IRepositoryProps;
    azure?: IRepositoryProps;
    bitbucket?: IRepositoryProps;
    other?: IRepositoryProps;
    manual?: IRepositoryProps;
  };
  dropDownText: string;
}

const RepositoriesDropdown: React.FC<IRepositoriesDropdownProps> = ({
  availableRepositories,
  dropDownText,
}): JSX.Element => {
  const { t } = useTranslation();

  const { gitLab, gitHub, azure, bitbucket, other, manual } =
    availableRepositories;

  const repositories = [
    {
      icon: gitLabIcon,
      id: t("components.repositoriesDropdown.gitLabButton.id"),
      isVisible: gitLab?.isVisible,
      onClick: gitLab?.onClick,
      text: t("components.repositoriesDropdown.gitLabButton.text"),
    },
    {
      icon: gitHubIcon,
      id: t("components.repositoriesDropdown.gitHubButton.id"),
      isVisible: gitHub?.isVisible,
      onClick: gitHub?.onClick,
      text: t("components.repositoriesDropdown.gitHubButton.text"),
    },
    {
      icon: azureIcon,
      id: t("components.repositoriesDropdown.azureButton.id"),
      isVisible: azure?.isVisible,
      onClick: azure?.onClick,
      text: t("components.repositoriesDropdown.azureButton.text"),
    },
    {
      icon: bitBucketIcon,
      id: t("components.repositoriesDropdown.bitbucketButton.id"),
      isVisible: bitbucket?.isVisible,
      onClick: bitbucket?.onClick,
      text: t("components.repositoriesDropdown.bitbucketButton.text"),
    },
    {
      icon: squarePlusIcon,
      id: t("components.repositoriesDropdown.otherButton.id"),
      isVisible: other?.isVisible,
      onClick: other?.onClick,
      text:
        other?.text ?? t("components.repositoriesDropdown.otherButton.text"),
    },
    {
      id: t("components.repositoriesDropdown.manual.id"),
      isVisible: manual?.isVisible,
      onClick: manual?.onClick,
      text: t("components.repositoriesDropdown.manual.text"),
    },
  ];

  return (
    <Dropdown
      align={"left"}
      border={false}
      button={
        <Button icon={faPlus} iconSide={"right"} variant={"primary"}>
          {dropDownText}
        </Button>
      }
      id={"repositories-dropdown"}
      minWidth={"max-content"}
      pt={"5px"}
      shadow={true}
    >
      <Row align={"center"} justify={"center"}>
        {repositories.map((repo): JSX.Element | undefined => {
          const { icon, id, isVisible, onClick, text } = repo;

          if (
            isVisible === undefined
              ? false
              : isVisible && id !== "manual-repository"
          ) {
            return (
              <Col id={id} key={id}>
                <Button onClick={onClick} size={"xs"}>
                  <Row justify={"center"}>
                    <RepoIcon src={icon} />
                  </Row>
                  <Row>
                    <Text>{text}</Text>
                  </Row>
                </Button>
              </Col>
            );
          }

          if (
            isVisible === undefined
              ? false
              : isVisible && id === "manual-repository"
          ) {
            return (
              <Col id={id} key={id}>
                <Container maxWidth={"80px"}>
                  <Button onClick={onClick} size={"xs"}>
                    <Text>{text}</Text>
                  </Button>
                </Container>
              </Col>
            );
          }

          return undefined;
        })}
      </Row>
    </Dropdown>
  );
};

export { RepositoriesDropdown };

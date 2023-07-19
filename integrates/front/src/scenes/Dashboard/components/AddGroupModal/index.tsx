/* eslint-disable react/forbid-component-props, fp/no-mutating-methods */
import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback } from "react";
import { useTranslation } from "react-i18next";
import LoadingOverlay from "react-loading-overlay-ts";
import { useHistory } from "react-router-dom";
import FadeLoader from "react-spinners/FadeLoader";

import { handleCreateError } from "./helpers";
import { validations } from "./validations";

import { ExternalLink } from "components/ExternalLink";
import { InfoDropdown } from "components/InfoDropdown";
import { Input, Select } from "components/Input";
import { Col } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import { useTour } from "hooks/use-tour";
import { ADD_GROUP_MUTATION } from "scenes/Dashboard/components/AddGroupModal/queries";
import type { IAddGroupModalProps } from "scenes/Dashboard/components/AddGroupModal/types";
import { msgSuccess } from "utils/notifications";

const AddGroupModal: React.FC<IAddGroupModalProps> = (
  props: IAddGroupModalProps
): JSX.Element => {
  const { onClose, organization, runTour } = props;
  const { t } = useTranslation();

  const { push } = useHistory();
  const { setCompleted } = useTour();

  const handleMutationResult = (result: {
    addGroup: { success: boolean };
  }): void => {
    if (result.addGroup.success) {
      onClose();
      msgSuccess(
        t("organization.tabs.groups.newGroup.success"),
        t("organization.tabs.groups.newGroup.titleSuccess")
      );
    }
  };

  const [addGroup, { loading: submitting }] = useMutation(ADD_GROUP_MUTATION, {
    onCompleted: handleMutationResult,
    onError: handleCreateError,
  });

  const finishTour = useCallback((): void => {
    setCompleted("newGroup");
    onClose();
  }, [onClose, setCompleted]);

  const handleSubmit = useCallback(
    async (values: {
      description: string;
      name: string;
      language: string;
      organization: string;
      type: string;
      service: string;
      squad: boolean;
    }): Promise<void> => {
      mixpanel.track("AddGroup");
      await addGroup({
        variables: {
          description: values.description,
          groupName: values.name.toUpperCase(),
          hasMachine:
            values.type === "CONTINUOUS-MACHINE" ||
            values.type === "CONTINUOUS-SQUAD",
          hasSquad: values.type === "CONTINUOUS-SQUAD",
          language: values.language,
          organizationName: values.organization,
          service: values.service,
          subscription: ["CONTINUOUS-MACHINE", "CONTINUOUS-SQUAD"].includes(
            values.type
          )
            ? "CONTINUOUS"
            : "ONESHOT",
        },
      });
      if (runTour) {
        finishTour();
        push(`/orgs/${organization}/groups/${values.name}/scope`);
      }
    },
    [addGroup, organization, push, runTour, finishTour]
  );

  return (
    <Modal
      minWidth={350}
      onClose={onClose}
      open={true}
      title={t("organization.tabs.groups.newGroup.new.group")}
    >
      <Formik
        enableReinitialize={true}
        initialValues={{
          description: "",
          language: "EN",
          name: "",
          organization: organization.toUpperCase(),
          service: "WHITE",
          squad: true,
          type: "CONTINUOUS-MACHINE",
        }}
        name={"newGroup"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        {(): JSX.Element => {
          const radioBtnOptions = [
            {
              text: "Continuous Hacking - Machine plan",
              tip: t("organization.tabs.groups.newGroup.machine.tooltip"),
              value: "CONTINUOUS-MACHINE",
            },
            {
              text: "Continuous Hacking - Squad plan",
              tip: t("organization.tabs.groups.newGroup.squad.tooltip"),
              value: "CONTINUOUS-SQUAD",
            },
            {
              text: "One-shot Hacking",
              tip: t("organization.tabs.groups.newGroup.oneshot.tooltip"),
              value: "ONESHOT",
            },
          ];

          return (
            <Fragment>
              <LoadingOverlay active={submitting} spinner={<FadeLoader />} />
              <Form>
                <Col lg={33} md={33} sm={33}>
                  <Input
                    disabled={true}
                    label={t(
                      "organization.tabs.groups.newGroup.organization.text"
                    )}
                    name={"organization"}
                    tooltip={t(
                      "organization.tabs.groups.newGroup.organization.tooltip"
                    )}
                  />
                </Col>
                <Col lg={33} md={33} paddingTop={25} sm={33}>
                  <Text mb={1}>
                    {t("organization.tabs.groups.newGroup.name")}
                  </Text>
                  <Input id={"add-group-name"} name={"name"} type={"text"} />
                </Col>
                <Col lg={33} md={33} paddingTop={25} sm={33}>
                  <Input
                    id={"add-group-description"}
                    label={t(
                      "organization.tabs.groups.newGroup.description.text"
                    )}
                    name={"description"}
                    tooltip={t(
                      "organization.tabs.groups.newGroup.description.tooltip"
                    )}
                    type={"text"}
                  />
                </Col>
                <Col paddingTop={25}>
                  {t("organization.tabs.groups.newGroup.type.title")}
                  {radioBtnOptions.map((option): JSX.Element => {
                    return (
                      <Col
                        key={`type_${option.value}`}
                        lg={33}
                        md={33}
                        paddingTop={7}
                        sm={33}
                      >
                        <Field
                          name={"type"}
                          type={"radio"}
                          value={option.value}
                        />
                        &nbsp;
                        {option.text}
                        &nbsp; &nbsp;
                        <InfoDropdown size={"small"}>{option.tip}</InfoDropdown>
                      </Col>
                    );
                  })}
                  <Col paddingTop={16}>
                    <ExternalLink href={"https://fluidattacks.com/plans/"}>
                      <Text size={"xs"}>
                        {"Learn more about Continuous Hacking plans"}
                      </Text>
                    </ExternalLink>
                  </Col>
                </Col>
                <Col
                  id={"add-group-testing-type"}
                  lg={33}
                  md={33}
                  paddingTop={25}
                  sm={33}
                >
                  <Select
                    label={t("organization.tabs.groups.newGroup.service.title")}
                    name={"service"}
                  >
                    <option value={"BLACK"}>
                      {t("organization.tabs.groups.newGroup.service.black")}
                    </option>
                    <option value={"WHITE"}>
                      {t("organization.tabs.groups.newGroup.service.white")}
                    </option>
                  </Select>
                </Col>
                <Col
                  id={"add-group-report-language"}
                  lg={33}
                  md={33}
                  paddingTop={25}
                  sm={33}
                >
                  <Tooltip
                    hide={runTour}
                    id={"organization.tabs.groups.newGroup.language.tooltip"}
                    place={"top"}
                    tip={t(
                      "organization.tabs.groups.newGroup.language.tooltip"
                    )}
                  >
                    <Select
                      label={t(
                        "organization.tabs.groups.newGroup.language.text"
                      )}
                      name={"language"}
                    >
                      <option value={"EN"}>
                        {t("organization.tabs.groups.newGroup.language.EN")}
                      </option>
                      <option value={"ES"}>
                        {t("organization.tabs.groups.newGroup.language.ES")}
                      </option>
                    </Select>
                  </Tooltip>
                </Col>
                <ModalConfirm
                  disabled={submitting}
                  id={"add-group-confirm"}
                  onCancel={onClose}
                />
              </Form>
            </Fragment>
          );
        }}
      </Formik>
    </Modal>
  );
};

export { AddGroupModal };

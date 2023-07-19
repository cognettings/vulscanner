import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import { useFormikContext } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useMemo } from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import { GET_FILES } from "./queries";
import type { IFile, IGetFilesQuery } from "./types";

import type { IFormProps } from "../types";
import { Input, Label, Select } from "components/Input";
import { Col } from "components/Layout";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const EnvironmentUrl: FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { values } = useFormikContext<IFormProps>();
  const { cloudName, groupName, urlType } = values;

  const { data } = useQuery<IGetFilesQuery>(GET_FILES, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group files", error);
      });
    },
    variables: { groupName },
  });

  const filesDataset = useMemo(
    (): IFile[] =>
      _.isUndefined(data) || _.isEmpty(data) || _.isNull(data.resources.files)
        ? []
        : (data.resources.files as IFile[]),
    [data]
  );

  const getLabelContent = (): string => {
    if (urlType === "APK") {
      return t("group.scope.git.addEnvironment.apk");
    }

    return t("group.scope.git.addEnvironment.url");
  };

  const UrlInput: JSX.Element =
    urlType === "APK" ? (
      <Select name={"url"}>
        <option value={""}>{""}</option>
        {filesDataset.map(
          (file): JSX.Element => (
            <option key={file.fileName} value={file.fileName}>
              {file.fileName}
            </option>
          )
        )}
      </Select>
    ) : (
      <Input
        fw={"bold"}
        label={"Type your environment URL"}
        name={"url"}
        tooltip={t("group.scope.git.addEnvironment.urlTooltip")}
      />
    );

  if (cloudName === "AWS" && urlType === "CLOUD") {
    return (
      <Col>
        <Label required={true}>
          {t("group.scope.git.addEnvironment.awsAccountId")}
        </Label>
        {<Input name={"url"} />}
        <Label required={false}>
          {t("group.scope.git.addEnvironment.awsAccessId")}
        </Label>
        {<Input name={"accessKeyId"} />}
        <Label required={false}>
          {t("group.scope.git.addEnvironment.awsSecretId")}
        </Label>
        {<Input name={"secretAccessKey"} />}
      </Col>
    );
  }

  return (
    <Col>
      <Label required={true}>{getLabelContent()}</Label>
      {UrlInput}
    </Col>
  );
};

export { EnvironmentUrl };

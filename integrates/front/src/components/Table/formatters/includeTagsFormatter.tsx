import React from "react";

import { LittleFlag } from "./styles";

import { Container } from "components/Container";
import { Text } from "components/Text";
import { translate } from "utils/translations/translate";

export function includeTagsFormatter({
  text,
  newTag = false,
  reviewTag = false,
}: {
  text: string;
  newTag?: boolean;
  reviewTag?: boolean;
}): JSX.Element {
  return (
    <Container display={"inline-block"}>
      <Container align={"center"} display={"flex"}>
        <Text disp={"inline-block"}>{text}</Text>
        {newTag ? (
          <LittleFlag>
            {translate.t("table.formatters.includeTags.new")}
          </LittleFlag>
        ) : undefined}
        {reviewTag ? (
          <LittleFlag bgColor={"#d88218"}>
            {translate.t("table.formatters.includeTags.review")}
          </LittleFlag>
        ) : undefined}
      </Container>
    </Container>
  );
}

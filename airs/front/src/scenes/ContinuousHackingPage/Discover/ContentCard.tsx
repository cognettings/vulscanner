import React from "react";

import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";

interface IContentCardProps {
  title: string;
  paragraph: string;
  mt: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;
  mb: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;
  icon: string;
  subtitle: string;
}

const ContentCard: React.FC<IContentCardProps> = ({
  title,
  paragraph,
  mt,
  mb,
  icon,
  subtitle,
}: IContentCardProps): JSX.Element => {
  return (
    <Container mb={mb} mh={2} mt={mt}>
      <Title color={"#25252d"} level={1} mb={4} mt={4}>
        {title}
      </Title>
      <Text color={"#65657b"}>{paragraph}</Text>
      <Container align={"center"} display={"flex"} mt={3}>
        <CloudImage alt={icon} src={icon} />
        <Text color={"#65657b"} ml={3} size={"big"} weight={"bold"}>
          {subtitle}
        </Text>
      </Container>
    </Container>
  );
};

export { ContentCard };

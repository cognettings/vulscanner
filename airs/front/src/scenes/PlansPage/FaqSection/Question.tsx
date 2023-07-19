import React, { useCallback, useState } from "react";
import { FaMinus, FaPlus } from "react-icons/fa";

import { Container } from "../../../components/Container";
import { Text } from "../../../components/Typography";

interface IQuestion {
  question: string;
  answer: string;
}

const PlansQuestion: React.FC<IQuestion> = ({
  question,
  answer,
}): JSX.Element => {
  const [description, setDescription] = useState("none");
  const [icon, setIcon] = useState("plus");

  const showDescription = useCallback((): void => {
    if (description === "none") {
      setDescription("block");
    } else {
      setDescription("none");
    }
    if (icon === "plus") {
      setIcon("minus");
    } else {
      setIcon("plus");
    }
  }, [description, icon]);

  return (
    <Container borderBottomColor={"#dddde3"} onClick={showDescription}>
      <Container
        align={"center"}
        display={"flex"}
        justify={"between"}
        maxWidth={"1200px"}
        pv={3}
        width={"100%"}
        wrap={"wrap"}
      >
        <Container ph={3} pv={1} width={"80%"}>
          <Text color={"#2e2e38"} size={"medium"} weight={"semibold"}>
            {question}
          </Text>
        </Container>
        <Container display={"flex"} justify={"end"} mr={0} width={"20%"}>
          {icon === "plus" ? <FaPlus /> : <FaMinus />}
        </Container>
      </Container>
      <Container
        borderTopColor={"#dddde3"}
        display={description === "none" ? "none" : "block"}
        justify={"start"}
        ph={3}
        pv={2}
      >
        <Text color={"#535365"}>{answer}</Text>
      </Container>
    </Container>
  );
};

export { PlansQuestion };

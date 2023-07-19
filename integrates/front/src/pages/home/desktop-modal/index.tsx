import React from "react";

import { Container } from "components/Container";
import { Text } from "components/Text";
import { loginLogo, onlyDesktop } from "resources/index";

interface IDesktopModalProps {
  message: string;
  emphasis: string;
}

const DesktopModal: React.FC<IDesktopModalProps> = ({
  message,
  emphasis,
}): JSX.Element => {
  return (
    <Container
      bgColor={"#f4f4f6"}
      display={"flex"}
      height={"100%"}
      width={"100%"}
      wrap={"wrap"}
    >
      <Container
        align={"center"}
        display={"flex"}
        justify={"center"}
        pt={"120px"}
        width={"100%"}
        wrap={"wrap"}
      >
        <Container
          bgImage={`url(${loginLogo})`}
          bgImagePos={"100% 100%"}
          height={"65px"}
          width={"145px"}
        />
        <Text lineHeight={"1.4"} mt={4} size={"medium"} ta={"center"}>
          {message}
          <Text disp={"inline"} fw={9} size={"medium"} tone={"dark"}>
            {emphasis}
          </Text>
        </Text>
        <Container
          align={"center"}
          display={"flex"}
          justify={"center"}
          position={"absolute"}
          positionBottom={"0"}
          scroll={"none"}
        >
          <img alt={"Desktop"} src={onlyDesktop} />
        </Container>
      </Container>
    </Container>
  );
};

export { DesktopModal };

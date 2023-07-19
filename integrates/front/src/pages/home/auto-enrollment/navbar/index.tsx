import React from "react";
import type { FC } from "react";
import { Link } from "react-router-dom";

import { ProgressBar } from "./styles";

import { Container } from "components/Container";
import { Text } from "components/Text";

interface INavBarProps {
  progressWidth: number;
  userName: string;
}

const NavBar: FC<INavBarProps> = ({ progressWidth, userName }): JSX.Element => {
  return (
    <Container
      position={"sticky"}
      positionTop={"0"}
      scroll={"none"}
      width={"100%"}
      zIndex={"100"}
    >
      <Container
        bgColor={"#fff"}
        borderTop={"solid 1px #e9e9ed"}
        maxHeight={"350px"}
        pb={"10px"}
        pl={"16px"}
        pr={"16px"}
        pt={"10px"}
        scroll={"none"}
        width={"100%"}
      >
        <Container
          align={"center"}
          display={"flex"}
          justify={"space-between"}
          margin={"auto"}
          maxWidth={"1366px"}
        >
          <Link to={"/home"}>
            <Container display={"block"} width={"120px"}>
              <img
                alt={"fluid-logo"}
                src={
                  "https://res.cloudinary.com/fluid-attacks/image/upload/v1676333780/airs/menu/Logo.png"
                }
              />
            </Container>
          </Link>
          <Container align={"center"} display={"flex"} justify={"center"}>
            <Container
              align={"center"}
              bgColor={"#eaecf0"}
              br={"100%"}
              display={"flex"}
              height={"25px"}
              justify={"center"}
              maxWidth={"25px"}
              minWidth={"25px"}
              scroll={"none"}
            >
              <Text
                disp={"contents"}
                size={"small"}
                ta={"center"}
                tone={"dark"}
              >
                {userName[0]}
              </Text>
            </Container>
            <Text ml={2}>{`Hi ${userName.split(" ")[0]}!`}</Text>
          </Container>
        </Container>
      </Container>
      <Container bgColor={"#e9e9ed"} height={"4px"} width={"100%"}>
        <ProgressBar width={`${progressWidth}%`} />
      </Container>
    </Container>
  );
};

export { NavBar };

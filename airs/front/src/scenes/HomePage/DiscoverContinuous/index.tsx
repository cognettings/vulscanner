/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/
import React, { useCallback, useRef, useState } from "react";
import YouTube from "react-youtube";

import {
  HomeImageContainer,
  HomeVideoContainer,
  PlayButtonContainer,
  PlayImageContainer,
} from "./StyledComponents";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { SimpleCard } from "../../../components/SimpleCard";
import { Title } from "../../../components/Typography";
import { i18next, translate } from "../../../utils/translations/translate";

const DiscoverContinuous: React.FC = (): JSX.Element => {
  const [play, setPlay] = useState(false);

  const [overButton, setOverButton] = useState(false);

  const playerRef = useRef<any>();

  const onPlayOver = useCallback((): void => {
    setOverButton(true);
  }, []);

  const onPlayLeave = useCallback((): void => {
    setOverButton(false);
  }, []);

  const activateVideo = useCallback((): void => {
    setPlay(!play);
    playerRef.current.internalPlayer.playVideo();
  }, [play]);

  const hideVideo = useCallback((): void => {
    setPlay(!play);
  }, [play]);

  const opts = {
    playerVars: {
      VideoPlaybackQuality: "large",
      controls: 0,
      origin: "https://fluidattacks.com",
    },
  };
  const videoId = i18next.language === "en" ? "GWcmso_NcK8" : "Hjy2vh9dNzI";

  return (
    <Container bgColor={"#ffffff"}>
      <Container
        align={"center"}
        bgColor={"#ffffff"}
        center={true}
        display={"flex"}
        justify={"center"}
        maxWidth={"1440px"}
        pv={5}
        wrap={"wrap"}
      >
        <Title
          color={"#bf0b1a"}
          level={3}
          mb={4}
          size={"small"}
          textAlign={"center"}
        >
          {translate.t("home.discoverContinuous.subtitle")}
        </Title>
        <Container maxWidth={"951px"} ph={4}>
          <Title
            color={"#2e2e38"}
            level={1}
            mb={4}
            size={"medium"}
            textAlign={"center"}
          >
            {translate.t("home.discoverContinuous.title")}
          </Title>
        </Container>
        <HomeVideoContainer isVisible={play}>
          <YouTube
            onEnd={hideVideo}
            opts={opts}
            ref={playerRef}
            videoId={videoId}
          />
        </HomeVideoContainer>
        <HomeImageContainer isVisible={play}>
          <PlayImageContainer>
            <PlayButtonContainer
              onClick={activateVideo}
              onMouseLeave={onPlayLeave}
              onMouseOver={onPlayOver}
            >
              <CloudImage
                alt={"play button"}
                src={`/home/${overButton ? "red-play" : "black-play"}`}
              />
            </PlayButtonContainer>
            <CloudImage alt={"intro image"} src={"/home/video-image-2"} />
          </PlayImageContainer>
        </HomeImageContainer>
        <Container center={true} maxWidth={"1250px"} ph={4}>
          <Grid columns={3} columnsMd={3} columnsSm={1} gap={"1rem"}>
            <SimpleCard
              bgColor={"#f4f4f6"}
              bgGradient={"#ffffff, #f4f4f6"}
              description={translate.t(
                "home.discoverContinuous.card1.subtitle"
              )}
              descriptionColor={"#535365"}
              image={"airs/home/DiscoverContinuous/card1.png"}
              title={translate.t("home.discoverContinuous.card1.title")}
              titleColor={"#2e2e38"}
            />
            <SimpleCard
              bgColor={"#f4f4f6"}
              bgGradient={"#ffffff, #f4f4f6"}
              description={translate.t(
                "home.discoverContinuous.card2.subtitle"
              )}
              descriptionColor={"#535365"}
              image={"airs/home/DiscoverContinuous/card2.png"}
              title={translate.t("home.discoverContinuous.card2.title")}
              titleColor={"#2e2e38"}
            />
            <SimpleCard
              bgColor={"#f4f4f6"}
              bgGradient={"#ffffff, #f4f4f6"}
              description={translate.t(
                "home.discoverContinuous.card3.subtitle"
              )}
              descriptionColor={"#535365"}
              image={"airs/home/DiscoverContinuous/card3.png"}
              title={translate.t("home.discoverContinuous.card3.title")}
              titleColor={"#2e2e38"}
            />
          </Grid>
        </Container>
        <Container display={"flex"} justify={"center"} maxWidth={"900px"}>
          <AirsLink href={"/services/continuous-hacking/"}>
            <Button size={"md"} variant={"primary"}>
              {translate.t("home.discoverContinuous.button")}
            </Button>
          </AirsLink>
        </Container>
      </Container>
    </Container>
  );
};

export { DiscoverContinuous };

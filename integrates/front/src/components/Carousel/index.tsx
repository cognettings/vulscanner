import React, { Fragment } from "react";

import { Buttons } from "./styles";

import { useCarousel } from "../../hooks";
import { Button } from "components/Button";

interface ICarouselProps {
  contents: JSX.Element[];
  initSelection?: number;
  tabs: string[];
}

const Carousel: React.FC<ICarouselProps> = ({
  contents,
  tabs,
}: Readonly<ICarouselProps>): JSX.Element => {
  const timePerProgress = 70;
  const numberOfCycles = tabs.length;
  const { cycle } = useCarousel(timePerProgress, numberOfCycles);

  return (
    <Fragment>
      {contents[cycle]}
      <Buttons selection={cycle}>
        {tabs.map(
          (tabName, index): JSX.Element => (
            <Button
              key={tabName === "" ? index : tabName}
              size={"xxs"}
              variant={"carousel"}
            >
              {tabName}
            </Button>
          )
        )}
      </Buttons>
    </Fragment>
  );
};

export type { ICarouselProps };
export { Carousel };

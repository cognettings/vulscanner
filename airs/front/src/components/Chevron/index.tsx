import React from "react";
import { BsChevronDown, BsChevronUp } from "react-icons/bs";

type TDirection = "down" | "up";

interface IChevronProps {
  direction: TDirection;
}

interface IChevronStates {
  company: TDirection;
  platform: TDirection;
  resources: TDirection;
  services: TDirection;
}

const Chevron: React.FC<IChevronProps> = ({
  direction,
}: IChevronProps): JSX.Element => {
  if (direction === "down") {
    return (
      <div style={{ marginLeft: "4px" }}>
        <BsChevronDown size={12} />
      </div>
    );
  }

  return (
    <div style={{ marginLeft: "4px" }}>
      <BsChevronUp size={12} />
    </div>
  );
};

export type { TDirection, IChevronStates };
export { Chevron };

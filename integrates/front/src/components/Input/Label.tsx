import { faAsterisk, faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC, ReactNode } from "react";
import React from "react";

import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";

interface ILabelProps {
  children?: ReactNode;
  fw?: "bold" | "regular";
  htmlFor?: string;
  required?: boolean;
  tooltip?: string;
}

const Label: FC<ILabelProps> = ({
  children,
  fw = "regular",
  htmlFor,
  required = false,
  tooltip,
}: Readonly<ILabelProps>): JSX.Element => (
  <label className={"flex mb1"} htmlFor={htmlFor}>
    <Text disp={"inline"} fw={fw === "regular" ? 4 : 8} mr={1}>
      {children}
    </Text>
    {required ? (
      <Text bright={0} disp={"inline"} fontSize={"10px"} mr={1} tone={"red"}>
        <FontAwesomeIcon icon={faAsterisk} />
      </Text>
    ) : undefined}
    {tooltip === undefined || htmlFor === undefined ? undefined : (
      <Tooltip
        disp={"flex"}
        id={`${htmlFor}-tooltip`}
        place={"bottom"}
        tip={tooltip}
      >
        <Text disp={"inline"} fontSize={"10px"}>
          <FontAwesomeIcon color={"#b0b0bf"} icon={faCircleInfo} />
        </Text>
      </Tooltip>
    )}
  </label>
);

export type { ILabelProps };
export { Label };

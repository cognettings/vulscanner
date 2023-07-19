/* eslint-disable react/jsx-no-bind */
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";

import { TableLink } from "components/Table/styles";
import { Tooltip } from "components/Tooltip";

export function formatLinkHandler(
  link: string,
  text: string,
  showInfo?: boolean,
  tip?: string
): JSX.Element {
  const handleClick = (event: React.MouseEvent<HTMLDivElement>): void => {
    event.stopPropagation();
  };

  const linkComponent = (
    // eslint-disable-next-line jsx-a11y/click-events-have-key-events
    <div onClick={handleClick} role={"button"} tabIndex={0}>
      <TableLink to={link}>{_.capitalize(text)}</TableLink>
    </div>
  );
  if (showInfo ?? false) {
    return (
      <div>
        {linkComponent}
        &nbsp;
        <Tooltip
          disp={"inline"}
          effect={"solid"}
          id={`${_.camelCase(text)}Tooltip`}
          place={"top"}
          tip={tip}
        >
          <sup>
            <FontAwesomeIcon color={"#5c5c70"} icon={faInfoCircle} />
          </sup>
        </Tooltip>
      </div>
    );
  }

  return linkComponent;
}

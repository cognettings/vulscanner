import React, { useCallback } from "react";

import { StyledMenuItem } from "../styles";

interface IMenuItemsProps {
  eventKey: string;
  itemContent: React.ReactNode;
  onClick: (eventKey: string) => void;
}

const MenuItem: React.FC<IMenuItemsProps> = ({
  itemContent,
  eventKey,
  onClick,
}): JSX.Element => {
  const handleClick = useCallback((): void => {
    onClick(eventKey);
  }, [eventKey, onClick]);

  return <StyledMenuItem onClick={handleClick}>{itemContent}</StyledMenuItem>;
};

export { MenuItem };

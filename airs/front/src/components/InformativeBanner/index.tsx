/* eslint react/forbid-component-props: 0 */
import React, { useCallback, useState } from "react";

import { InformativeBannerItems } from "./InformativeBannerItems";
import { InformativeBannerContainer } from "./styles/styledComponents";

interface IProps {
  bgColor: string;
  buttonText: string;
  title: string;
  url: string;
}

const InformativeBanner: React.FC<IProps> = ({
  bgColor,
  buttonText,
  title,
  url,
}: IProps): JSX.Element => {
  const [isClose, setIsClose] = useState(false);

  const handleClose = useCallback((): void => {
    setIsClose(!isClose);
  }, [isClose]);

  return (
    <InformativeBannerContainer bgColor={bgColor} isClose={isClose}>
      <InformativeBannerItems
        buttonText={buttonText}
        close={handleClose}
        title={title}
        url={url}
      />
    </InformativeBannerContainer>
  );
};

export { InformativeBanner };

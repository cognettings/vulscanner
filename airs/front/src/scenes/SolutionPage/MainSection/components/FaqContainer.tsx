import React from "react";

import { Container } from "../../../../components/Container";
import type { IContainerProps } from "../../../../components/Container/types";

const FaqContainer: React.FC<IContainerProps> = ({ children }): JSX.Element => (
  <Container center={true} maxWidth={"1200px"} pb={5} ph={4}>
    {children}
  </Container>
);

export { FaqContainer };

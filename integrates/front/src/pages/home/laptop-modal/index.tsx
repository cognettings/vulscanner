import React, { useCallback } from "react";

import { Container } from "components/Container";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { laptop } from "resources/index";
import { openUrl } from "utils/resourceHelpers";

interface ILaptopModalProps {
  title: string;
  message: string;
  button: string;
  url: string;
}

const LaptopModal: React.FC<ILaptopModalProps> = ({
  button,
  message,
  title,
  url,
}: ILaptopModalProps): JSX.Element => {
  const handleClick = useCallback((): void => {
    openUrl(url);
  }, [url]);

  return (
    <Modal open={true}>
      <Text fw={7} lineHeight={"1.4"} mb={3} size={"medium"}>
        {title}
      </Text>
      <Container display={"flex"} justify={"center"} scroll={"none"}>
        <img alt={"Laptop"} src={laptop} />
      </Container>
      <Text lineHeight={"1.4"} mb={3} mt={3} size={"medium"}>
        {message}
      </Text>
      <ModalConfirm onConfirm={handleClick} txtConfirm={button} />
    </Modal>
  );
};

export { LaptopModal };

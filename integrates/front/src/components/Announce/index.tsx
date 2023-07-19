import React from "react";

import { Container } from "./styles";

import { Logo } from "components/Logo";

interface IAnnounceProps {
  link?: string;
  linkText?: string;
  message: string;
}

const Announce: React.FC<IAnnounceProps> = ({
  link,
  linkText,
  message,
}: Readonly<IAnnounceProps>): JSX.Element => {
  if (link !== undefined && linkText !== undefined) {
    const messages: string[] = message.split(linkText);

    return (
      <Container>
        <Logo height={50} width={50} />
        <p>
          {messages[0]}
          <a href={link} rel={"noreferrer"} target={"_blank"}>
            {linkText ? linkText : "Visit Docs"}
          </a>
          <br />
          {messages[1]}
        </p>
      </Container>
    );
  }

  return (
    <Container>
      <Logo height={50} width={50} />
      <p>{message}</p>
    </Container>
  );
};

export type { IAnnounceProps };
export { Announce };

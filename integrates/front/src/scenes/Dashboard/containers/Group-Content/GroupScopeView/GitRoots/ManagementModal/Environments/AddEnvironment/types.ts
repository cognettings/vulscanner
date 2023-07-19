interface IAddEnvironmentProps {
  groupName: string;
  rootId: string;
  closeFunction: () => void;
}

interface IFormProps {
  cloudName: string | undefined;
  groupName: string;
  url: string;
  type: string;
  rootId: string;
  urlType: string;
}

export type { IAddEnvironmentProps, IFormProps };

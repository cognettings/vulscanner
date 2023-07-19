interface ICheckAccessProps {
  credExists: boolean;
  setIsGitAccessible: React.Dispatch<React.SetStateAction<boolean>>;
  setShowGitAlert: React.Dispatch<React.SetStateAction<boolean>>;
  setValidateGitMsg: React.Dispatch<
    React.SetStateAction<{
      message: string;
      type: string;
    }>
  >;
}

export type { ICheckAccessProps };

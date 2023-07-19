interface IInvalidateAccessTokenAttr {
  invalidateAccessToken: {
    success: boolean;
  };
}

interface IGetAccessTokenAttr {
  me: {
    accessTokens: IAccessTokens[];
  };
}

interface ITokensModalProps {
  open: boolean;
  onClose: () => void;
}

interface IAddAccessTokenAttr {
  addAccessToken: {
    sessionJwt: string;
    success: boolean;
  };
}

interface IAccessTokens {
  id: string;
  name: string;
  issuedAt: number;
  lastUse: Date | null;
  action: string | undefined;
}

export type {
  IAddAccessTokenAttr,
  IAccessTokens,
  IInvalidateAccessTokenAttr,
  ITokensModalProps,
  IGetAccessTokenAttr,
};

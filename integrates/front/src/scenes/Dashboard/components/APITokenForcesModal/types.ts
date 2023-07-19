interface IUpdateForcesTokenAttr {
  updateForcesAccessToken: {
    sessionJwt: string;
    success: boolean;
  };
}

interface IGetForcesTokenAttr {
  group: {
    forcesExpDate: string | undefined;
    forcesToken: string | undefined;
  };
}

export type { IUpdateForcesTokenAttr, IGetForcesTokenAttr };

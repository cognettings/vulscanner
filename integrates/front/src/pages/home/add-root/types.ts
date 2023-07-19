interface ICurrentUser {
  me: {
    organizations: {
      groups: {
        name: string;
      }[];
      id: string;
      name: string;
    }[];
  };
}

export type { ICurrentUser };

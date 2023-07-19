interface IFile {
  description: string;
  fileName: string;
  uploadDate: string;
}

interface IGroupFileAttr {
  description: string;
  uploader: string;
  uploadDate: string | null;
  fileName: string;
}

interface IGetFilesQuery {
  resources: {
    files: IGroupFileAttr[] | null;
  };
}

export type { IFile, IGetFilesQuery };

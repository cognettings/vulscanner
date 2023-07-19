interface IEvidenceFields {
  date: string | null;
  description: string | null;
  isDraft: boolean | null;
  url: string | null;
}

interface IGetFindingEvidences {
  finding: {
    evidence: {
      animation: IEvidenceFields;
      evidence1: IEvidenceFields;
      evidence2: IEvidenceFields;
      evidence3: IEvidenceFields;
      evidence4: IEvidenceFields;
      evidence5: IEvidenceFields;
      exploitation: IEvidenceFields;
    };
    id: string;
  };
}

interface IEvidenceItem {
  date: string;
  description: string;
  isDraft: boolean;
  url: string;
}

export type { IGetFindingEvidences, IEvidenceItem };

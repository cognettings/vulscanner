import _ from "lodash";

import type { IEvidenceItem, IGetFindingEvidences } from "./types";

const formatEvidenceImages = (
  evidences: IGetFindingEvidences["finding"]["evidence"]
): Record<string, IEvidenceItem> => {
  const formatted = Object.entries(evidences)
    .map(([key, value]): [string, IEvidenceItem] => {
      return [
        key,
        {
          date: value.date ?? "",
          description: value.description ?? "",
          isDraft: value.isDraft ?? false,
          url: value.url ?? "",
        },
      ];
    })
    .filter(([key]): boolean => key !== "__typename");

  return Object.fromEntries(formatted);
};

const formatEvidenceList = (
  evidenceImages: Record<string, IEvidenceItem>,
  isEditing: boolean,
  meetingMode: boolean
): string[] => {
  const keys = _.uniq([
    "animation",
    "exploitation",
    ...Object.keys(evidenceImages),
  ]);

  return keys.filter((name): boolean => {
    const evidence = evidenceImages[name];

    if (evidence.isDraft && meetingMode) {
      return false;
    }

    if (_.isEmpty(evidence.url)) {
      return isEditing;
    }

    return true;
  });
};

export { formatEvidenceImages, formatEvidenceList };

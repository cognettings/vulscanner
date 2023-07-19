import _ from "lodash";
import React from "react";

import { Label } from "./styles";

export const Detail: React.FC<{
  editableField: JSX.Element | undefined;
  isEditing: boolean;
  label: JSX.Element | string | undefined;
  field: JSX.Element | string | null;
}> = ({
  isEditing,
  editableField,
  label,
  field,
}: {
  editableField: JSX.Element | undefined;
  isEditing: boolean;
  label: JSX.Element | string | undefined;
  field: JSX.Element | string | null;
}): JSX.Element => {
  return (
    <React.StrictMode>
      <div className={" justify-start items-end ma0 pv1"} data-private={true}>
        {_.isUndefined(label) ? undefined : (
          <div style={{ minWidth: "85px" }}>
            <Label>{label}</Label>&nbsp;
          </div>
        )}
        <div>{isEditing ? editableField : field}</div>
      </div>
    </React.StrictMode>
  );
};

import React from "react";

import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  groupLevelPermissions,
} from "context/authz/config";
import { GroupRoute } from "scenes/Dashboard/containers/Group-Content/GroupRoute";

const Group: React.FC = (): JSX.Element => {
  return (
    <authzGroupContext.Provider value={groupAttributes}>
      <authzPermissionsContext.Provider value={groupLevelPermissions}>
        <GroupRoute />
      </authzPermissionsContext.Provider>
    </authzGroupContext.Provider>
  );
};

export { Group };

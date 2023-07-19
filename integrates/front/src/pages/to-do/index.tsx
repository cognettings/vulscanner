import React from "react";

import {
  authzPermissionsContext,
  groupLevelPermissions,
} from "context/authz/config";
import { TasksContent } from "scenes/Dashboard/containers/Tasks-Content";

const ToDo: React.FC = (): JSX.Element => {
  return (
    <authzPermissionsContext.Provider value={groupLevelPermissions}>
      <TasksContent />
    </authzPermissionsContext.Provider>
  );
};

export { ToDo };

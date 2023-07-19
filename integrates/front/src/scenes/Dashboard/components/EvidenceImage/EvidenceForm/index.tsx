import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IEvidenceImageProps } from "..";
import { DisplayImage } from "../DisplayImage";
import { Button } from "components/Button";
import { useConfirmDialog } from "components/confirm-dialog";
import { Editable, InputFile, TextArea } from "components/Input";
import { Tooltip } from "components/Tooltip";
import {
  composeValidators,
  isValidEvidenceDescription,
  maxLength,
  validTextField,
} from "utils/validations";

const MAX_DESCRIPTION_LENGTH = 5000;
const maxDescriptionLength = maxLength(MAX_DESCRIPTION_LENGTH);

const EvidenceForm: React.FC<Readonly<IEvidenceImageProps>> = ({
  acceptedMimes,
  content,
  description,
  isDescriptionEditable,
  isRemovable = false,
  name,
  onDelete,
  validate,
}): JSX.Element => {
  const { t } = useTranslation();

  const { initialValues, setFieldTouched, setFieldValue, values } =
    useFormikContext<Record<string, unknown>>();

  const validEvidenceDescription = isValidEvidenceDescription(
    (initialValues[name] as { url: string }).url,
    (values[name] as { file: FileList | undefined }).file
  );

  const shouldRenderPreview = content !== "file";

  const getFileNameExtension = (filename: string): string => {
    const splittedName = filename.split(".");
    const extension =
      splittedName.length > 1 ? (_.last(splittedName) as string) : "";

    return extension.toLowerCase();
  };

  const { confirm, ConfirmDialog } = useConfirmDialog();
  const handleChange = useCallback(
    async (event: React.ChangeEvent<HTMLInputElement>): Promise<void> => {
      const files = event.target.value as unknown as FileList | undefined;

      if (files) {
        const preview = {
          name: files[0].name,
          url: URL.createObjectURL(files[0]),
        };

        const confirmResult = await confirm({
          message: (
            <React.Fragment>
              <label>
                {t("searchFindings.tabEvidence.fields.modal.message")}
              </label>
              <DisplayImage
                content={preview.url}
                extension={getFileNameExtension(preview.name)}
                name={name}
              />
            </React.Fragment>
          ),
          title: t("searchFindings.tabEvidence.fields.modal.title"),
        });

        if (confirmResult) {
          setFieldTouched(`${name}.file`, true);
        } else {
          setFieldValue(`${name}.file`, undefined);
        }
      }
    },
    [confirm, name, setFieldTouched, setFieldValue, t]
  );

  return (
    <React.Fragment>
      <InputFile
        accept={acceptedMimes}
        id={name}
        name={`${name}.file`}
        onChange={shouldRenderPreview ? handleChange : undefined}
        validate={validate}
      />
      <Editable
        currentValue={description}
        isEditing={isDescriptionEditable}
        label={""}
      >
        <TextArea
          label={"Description"}
          name={`${name}.description`}
          tooltip={t("searchFindings.tabEvidence.descriptionTooltip")}
          validate={composeValidators([
            maxDescriptionLength,
            validEvidenceDescription,
            validTextField,
          ])}
        />
      </Editable>
      {isRemovable ? (
        <Tooltip
          id={t("searchFindings.tabEvidence.removeTooltip.id")}
          tip={t("searchFindings.tabEvidence.removeTooltip")}
        >
          <Button onClick={onDelete} variant={"secondary"}>
            <FontAwesomeIcon icon={faTrashAlt} />
            &nbsp;{t("searchFindings.tabEvidence.remove")}
          </Button>
        </Tooltip>
      ) : undefined}
      <ConfirmDialog />
    </React.Fragment>
  );
};

export { EvidenceForm };

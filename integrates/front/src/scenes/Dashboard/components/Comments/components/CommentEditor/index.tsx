import { Form, Formik } from "formik";
import type { FormikProps } from "formik";
import _ from "lodash";
import React, { useCallback, useContext, useRef, useState } from "react";
import { useHotkeys } from "react-hotkeys-hook";
import { useTranslation } from "react-i18next";
import type { TestContext, ValidationError } from "yup";
import { object, string } from "yup";

import { Button } from "components/Button";
import { TextArea } from "components/Input";
import { commentContext } from "scenes/Dashboard/components/Comments/context";
import type { ICommentContext } from "scenes/Dashboard/components/Comments/types";

interface ICommentEditorProps {
  id: number;
  onPost: (editorText: string) => void;
}

const MAX_LENGTH: number = 20000;
const CommentEditor: React.FC<ICommentEditorProps> = ({
  id,
  onPost,
}: ICommentEditorProps): JSX.Element => {
  const { t } = useTranslation();
  const [editorText, setEditorText] = useState("");
  const { replying, setReplying }: ICommentContext = useContext(commentContext);
  const formRef = useRef<FormikProps<{ "comment-editor": string }>>(null);

  const onChange = useCallback(
    (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
      setEditorText(event.target.value);
      if (!_.isUndefined(setReplying)) {
        setReplying(id);
      }
    },
    [id, setReplying]
  );

  const onFocus = useCallback((): void => {
    if (!_.isUndefined(setReplying)) {
      setReplying(id);
    }
  }, [id, setReplying]);

  const clickHandler = useCallback((): void => {
    if (replying !== id) {
      setEditorText("");

      return;
    }
    const trimmedText = _.trim(editorText);
    if (trimmedText !== "") {
      onPost(trimmedText);
      setEditorText("");
    }
  }, [editorText, id, onPost, replying]);

  const onSubmit = useCallback((): void => {
    if (formRef.current !== null) {
      formRef.current.handleSubmit();
    }
  }, [formRef]);

  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  useHotkeys("ctrl+enter", onSubmit, { enableOnTags: ["TEXTAREA"] });

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{ "comment-editor": editorText }}
      innerRef={formRef}
      name={"addConsult"}
      onSubmit={clickHandler}
      validationSchema={object().shape({
        "comment-editor": string()
          .max(MAX_LENGTH, t("validations.maxLength", { count: MAX_LENGTH }))
          .test({
            exclusive: false,
            name: "invalidTextBeginning",
            test: (
              value: string | undefined,
              thisContext: TestContext
            ): ValidationError | boolean => {
              if (value === undefined) {
                return false;
              }
              const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);

              return _.isNull(beginTextMatch)
                ? true
                : thisContext.createError({
                    message: t("validations.invalidTextBeginning", {
                      chars: `'${beginTextMatch[0]}'`,
                    }),
                  });
            },
          })
          .test({
            exclusive: false,
            name: "invalidTextField",
            test: (
              value: string | undefined,
              thisContext: TestContext
            ): ValidationError | boolean => {
              if (value === undefined) {
                return false;
              }
              const textMatch: RegExpMatchArray | null =
                /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s(){}[\],./:;@&_$%'#*=¿?¡!+-]/u.exec(
                  value
                );

              return _.isNull(textMatch)
                ? true
                : thisContext.createError({
                    message: t("validations.invalidTextField", {
                      chars: `'${textMatch[0]}'`,
                    }),
                  });
            },
          }),
      })}
    >
      <Form>
        <TextArea
          name={"comment-editor"}
          onChange={onChange}
          onFocus={onFocus}
          placeholder={t("comments.editorPlaceholder")}
          rows={3}
        />
        {editorText !== "" && (
          <div className={"pv2"}>
            <Button type={"submit"} variant={"primary"}>
              {t("comments.send")}
            </Button>
          </div>
        )}
      </Form>
    </Formik>
  );
};

export { CommentEditor };

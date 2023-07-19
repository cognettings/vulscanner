import React, { useCallback, useRef, useState } from "react";

import { Modal, ModalConfirm } from "components/Modal";

interface IConfirmDialogProps {
  message?: React.ReactNode;
  title: string;
}

const useConfirmDialog = (): {
  confirm: (props: IConfirmDialogProps) => Promise<boolean>;
  ConfirmDialog: React.FC;
} => {
  const [open, setOpen] = useState(false);
  const [dialogProps, setDialogProps] = useState<IConfirmDialogProps>();
  const resolveConfirm = useRef<((result: boolean) => void) | null>(null);

  const confirm = useCallback(
    async (props: IConfirmDialogProps): Promise<boolean> => {
      setDialogProps(props);
      setOpen(true);

      return new Promise<boolean>((resolve): void => {
        // Needed to implement the deferred promise pattern
        // eslint-disable-next-line fp/no-mutation
        resolveConfirm.current = resolve;
      });
    },
    []
  );

  const handleConfirm = useCallback((): void => {
    setOpen(false);
    setDialogProps(undefined);
    resolveConfirm.current?.(true);
  }, []);

  const handleCancel = useCallback((): void => {
    setOpen(false);
    setDialogProps(undefined);
    resolveConfirm.current?.(false);
  }, []);

  const ConfirmDialog: React.FC = (): JSX.Element => {
    return (
      <Modal open={open} title={dialogProps?.title}>
        {dialogProps?.message}
        <ModalConfirm onCancel={handleCancel} onConfirm={handleConfirm} />
      </Modal>
    );
  };

  return { ConfirmDialog, confirm };
};

export { useConfirmDialog };

import {
  faAngleLeft,
  faAngleRight,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";
import ImageViewer from "react-simple-image-viewer";

interface IEvidenceLightboxProps {
  evidenceImages: string[];
  currentImage: number;
  onClose: (index: number, isOpen: boolean) => void;
}

const EvidenceLightbox: React.FC<IEvidenceLightboxProps> = ({
  currentImage,
  evidenceImages,
  onClose,
}): JSX.Element => {
  const handleOnClose = useCallback((): void => {
    onClose(0, false);
  }, [onClose]);

  return currentImage >= 0 ? (
    <div aria-label={"ImageViewer"} role={"dialog"}>
      <ImageViewer
        backgroundStyle={{
          backgroundColor: "rgba(0,0,0,0.9)",
          zIndex: "100",
        }}
        closeComponent={<FontAwesomeIcon icon={faXmark} />}
        closeOnClickOutside={true}
        currentIndex={currentImage}
        disableScroll={true}
        leftArrowComponent={<FontAwesomeIcon icon={faAngleLeft} />}
        onClose={handleOnClose}
        rightArrowComponent={<FontAwesomeIcon icon={faAngleRight} />}
        src={evidenceImages.map((url): string => `${location.href}/${url}`)}
      />
    </div>
  ) : (
    <React.StrictMode />
  );
};

export { EvidenceLightbox };

"use client";;
import { useState } from "react";

export const useCopyToClipboard = ({
  copiedDuration = 3000
} = {}) => {
  const [isCopied, setIsCopied] = useState(false);

  const copyToClipboard = (value) => {
    if (!value || typeof navigator === "undefined" || !navigator.clipboard) {
      return;
    }

    navigator.clipboard.writeText(value).then(() => {
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), copiedDuration);
    }, () => {});
  };

  return { isCopied, copyToClipboard };
};

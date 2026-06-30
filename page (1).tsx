"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { UploadCloud, FileVideo, CheckCircle2, XCircle } from "lucide-react";

const MAX_SIZE_MB = 500;
const ACCEPTED = { "video/mp4": [".mp4"], "video/quicktime": [".mov"], "video/x-msvideo": [".avi"], "video/x-matroska": [".mkv"] };

type UploadState = "idle" | "uploading" | "success" | "error";

export default function VideoUploader({ onUploaded }: { onUploaded?: (projectId: string) => void }) {
  const [progress, setProgress] = useState(0);
  const [state, setState] = useState<UploadState>("idle");
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");

  const onDrop = useCallback(async (accepted: File[], rejected: any[]) => {
    if (rejected.length) {
      setError("Unsupported file type or file too large.");
      setState("error");
      return;
    }
    const file = accepted[0];
    if (!file) return;

    if (file.size / (1024 * 1024) > MAX_SIZE_MB) {
      setError(`File exceeds ${MAX_SIZE_MB}MB limit.`);
      setState("error");
      return;
    }

    setFileName(file.name);
    setState("uploading");
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/upload/video`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          onUploadProgress: (evt) => {
            if (evt.total) setProgress(Math.round((evt.loaded * 100) / evt.total));
          },
        }
      );
      setState("success");
      onUploaded?.(res.data.project_id);
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Upload failed. Please try again.");
      setState("error");
    }
  }, [onUploaded]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED,
    maxFiles: 1,
    maxSize: MAX_SIZE_MB * 1024 * 1024,
  });

  return (
    <div
      {...getRootProps()}
      className={`glass-card p-10 text-center cursor-pointer transition-all border-2 border-dashed
        ${isDragActive ? "border-primary-light bg-primary/10" : "border-white/15 hover:border-white/30"}`}
    >
      <input {...getInputProps()} />

      {state === "idle" && (
        <div className="flex flex-col items-center gap-3">
          <UploadCloud size={40} className="text-primary-light" />
          <p className="font-semibold">Drag & drop your video here</p>
          <p className="text-sm text-white/50">MP4, MOV, AVI, MKV — up to {MAX_SIZE_MB}MB</p>
          <span className="btn-ghost mt-2 text-sm py-2 px-4">Browse Files</span>
        </div>
      )}

      {state === "uploading" && (
        <div className="flex flex-col items-center gap-3">
          <FileVideo size={36} className="text-accent animate-pulse" />
          <p className="font-medium truncate max-w-xs">{fileName}</p>
          <div className="w-full max-w-sm h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary to-accent transition-all duration-200"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-white/50">{progress}% uploaded</p>
        </div>
      )}

      {state === "success" && (
        <div className="flex flex-col items-center gap-3 text-green-400">
          <CheckCircle2 size={40} />
          <p className="font-medium">Upload complete! Transcription in progress…</p>
        </div>
      )}

      {state === "error" && (
        <div className="flex flex-col items-center gap-3 text-red-400">
          <XCircle size={40} />
          <p className="font-medium">{error}</p>
          <span className="text-sm text-white/50">Click to try again</span>
        </div>
      )}
    </div>
  );
}

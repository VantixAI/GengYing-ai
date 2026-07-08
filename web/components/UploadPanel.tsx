"use client";

import { ChangeEvent, useState } from "react";
import { uploadMeme } from "@/lib/api";

export function UploadPanel() {
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  async function selectFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setMessage("");
    try {
      await uploadMeme(file);
      setMessage("上传成功。运行索引脚本后即可被搜索到。");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "上传失败");
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  return (
    <div className="rounded-3xl border-2 border-dashed border-ink bg-white/70 p-6 text-center">
      <p className="mb-1 font-bold">养一座自己的梗图库</p>
      <p className="mb-4 text-sm text-neutral-600">支持 JPG、PNG、WEBP 和 GIF，单张不超过 10 MB</p>
      <label className="inline-block cursor-pointer rounded-xl border-2 border-ink bg-lime px-4 py-2 font-semibold transition hover:-translate-y-0.5">
        {uploading ? "上传中…" : "上传表情包"}
        <input type="file" accept="image/jpeg,image/png,image/webp,image/gif" onChange={selectFile} disabled={uploading} className="sr-only" />
      </label>
      {message && <p className="mt-3 text-sm">{message}</p>}
    </div>
  );
}


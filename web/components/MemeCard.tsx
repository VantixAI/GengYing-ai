"use client";

import type { MemeResult } from "@/types/meme";
import { recordClick } from "@/lib/api";

interface MemeCardProps {
  meme: MemeResult;
  query: string;
}

export function MemeCard({ meme, query }: MemeCardProps) {
  async function copyCaption(caption: string) {
    await navigator.clipboard.writeText(caption);
    void recordClick(meme.id, query);
  }

  async function download() {
    void recordClick(meme.id, query);
    const response = await fetch(meme.url);
    const blob = await response.blob();
    const objectUrl = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = meme.filename;
    link.click();
    URL.revokeObjectURL(objectUrl);
  }

  async function copyImage() {
    const response = await fetch(meme.url);
    const source = await response.blob();
    const bitmap = await createImageBitmap(source);
    const canvas = document.createElement("canvas");
    canvas.width = bitmap.width;
    canvas.height = bitmap.height;
    canvas.getContext("2d")?.drawImage(bitmap, 0, 0);
    const png = await new Promise<Blob>((resolve, reject) =>
      canvas.toBlob((blob) => blob ? resolve(blob) : reject(new Error("图片转换失败")), "image/png"),
    );
    await navigator.clipboard.write([new ClipboardItem({ "image/png": png })]);
    void recordClick(meme.id, query);
  }

  return (
    <article className="overflow-hidden rounded-3xl border-2 border-ink bg-white shadow-card">
      <div className="aspect-square bg-neutral-100">
        {/* Plain img supports local, remote and uploaded GIF files without optimization issues. */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={meme.url} alt={meme.captions[0] ?? "搜索到的表情包"} className="h-full w-full object-cover" />
      </div>
      <div className="space-y-3 p-4">
        <div className="flex items-center justify-between gap-2 text-xs text-neutral-500">
          <span>匹配度 {(meme.score * 100).toFixed(0)}%</span>
          <div className="flex gap-3">
            <button onClick={copyImage} className="font-semibold text-ink hover:text-coral">复制图片</button>
            <button onClick={download} className="font-semibold text-ink hover:text-coral">下载 ↓</button>
          </div>
        </div>
        <div className="space-y-2">
          {meme.captions.map((caption) => (
            <button
              key={caption}
              onClick={() => copyCaption(caption)}
              className="w-full rounded-xl bg-neutral-100 px-3 py-2 text-left text-sm transition hover:bg-lime"
              title="点击复制文案"
            >
              {caption}
            </button>
          ))}
        </div>
      </div>
    </article>
  );
}

"use client";

import { useState } from "react";
import { MemeCard } from "@/components/MemeCard";
import { SearchBox } from "@/components/SearchBox";
import { UploadPanel } from "@/components/UploadPanel";
import { searchMemes } from "@/lib/api";
import type { MemeResult } from "@/types/meme";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<MemeResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch(value: string) {
    setLoading(true);
    setError("");
    setQuery(value);
    try {
      const data = await searchMemes(value);
      setResults(data.results);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "搜索失败");
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen px-5 py-8 sm:px-8">
      <nav className="mx-auto flex max-w-6xl items-center justify-between">
        <div className="text-xl font-black tracking-tight">梗应 AI</div>
        <span className="rounded-full border border-ink px-3 py-1 text-xs">懂梗，也懂你</span>
      </nav>

      <section className="mx-auto max-w-5xl pb-12 pt-20 text-center sm:pt-28">
        <div className="mb-5 inline-block -rotate-2 rounded-lg bg-lime px-3 py-1 text-sm font-bold">这句话，该配什么图？</div>
        <h1 className="mb-5 text-5xl font-black leading-tight tracking-tight sm:text-7xl">说人话，找梗图。</h1>
        <p className="mx-auto mb-9 max-w-xl text-neutral-600">输入此刻的心情或处境，AI 从语义和情绪里找出最会说话的那张图。</p>
        <SearchBox loading={loading} onSearch={handleSearch} />
        {error && <p className="mt-4 text-sm font-medium text-red-600">{error}</p>}
      </section>

      {results.length > 0 && (
        <section className="mx-auto mb-20 max-w-6xl">
          <div className="mb-6 flex items-end justify-between gap-4">
            <div>
              <p className="text-sm text-neutral-500">为“{query}”找到</p>
              <h2 className="text-2xl font-black">这几张很有戏</h2>
            </div>
            <span className="text-sm text-neutral-500">点文案即可复制</span>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {results.map((meme) => <MemeCard key={meme.id} meme={meme} query={query} />)}
          </div>
        </section>
      )}

      <section className="mx-auto max-w-3xl pb-20">
        <UploadPanel />
      </section>
    </main>
  );
}


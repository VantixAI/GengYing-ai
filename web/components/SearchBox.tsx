"use client";

import { FormEvent, useState } from "react";

interface SearchBoxProps {
  loading: boolean;
  onSearch: (query: string) => void;
}

export function SearchBox({ loading, onSearch }: SearchBoxProps) {
  const [query, setQuery] = useState("老板又让我周末加班，但我不敢拒绝");

  function submit(event: FormEvent) {
    event.preventDefault();
    const value = query.trim();
    if (value) onSearch(value);
  }

  return (
    <form onSubmit={submit} className="mx-auto flex max-w-3xl flex-col gap-3 sm:flex-row">
      <label htmlFor="query" className="sr-only">输入一句话</label>
      <input
        id="query"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="今天发生了什么？"
        className="min-w-0 flex-1 rounded-2xl border-2 border-ink bg-white px-5 py-4 text-base outline-none transition focus:-translate-y-0.5 focus:shadow-card"
      />
      <button
        type="submit"
        disabled={loading}
        className="rounded-2xl border-2 border-ink bg-ink px-7 py-4 font-bold text-white transition hover:-translate-y-0.5 hover:bg-coral disabled:cursor-wait disabled:opacity-60"
      >
        {loading ? "正在懂你的梗…" : "给我配图"}
      </button>
    </form>
  );
}


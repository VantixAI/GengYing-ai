import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#171717",
        cream: "#fffaf0",
        lime: "#c7f464",
        coral: "#ff735c",
      },
      boxShadow: {
        card: "0 10px 0 rgba(23, 23, 23, 0.12)",
      },
    },
  },
  plugins: [],
};

export default config;


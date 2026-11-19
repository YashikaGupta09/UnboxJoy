/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        lilac: "#F4F0FB",
        ink: "#1E1B3A",
        saffron: "#F2A93B",
        rose: "#E8607A",
        mist: "#DCD5EE",
      },
      fontFamily: {
        display: ['"Bricolage Grotesque"', "system-ui", "sans-serif"],
        body: ["Figtree", "system-ui", "sans-serif"],
      },
      keyframes: {
        swap: {
          "0%": { opacity: 0, transform: "translateX(16px)" },
          "100%": { opacity: 1, transform: "translateX(0)" },
        },
      },
      animation: { swap: "swap 280ms ease-out" },
    },
  },
  plugins: [],
};

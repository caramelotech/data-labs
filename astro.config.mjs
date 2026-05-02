import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

export default defineConfig({
  site: "https://caramelotech.com.br",
  base: "/data-labs",
  integrations: [
    starlight({
      title: "Caramelo Tech",
      customCss: ["./src/styles/custom.css"],
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/caramelotech",
        },
        {
          icon: "linkedin",
          label: "LinkedIn",
          href: "https://www.linkedin.com/company/caramelotech/",
        },
        {
          icon: "instagram",
          label: "Instagram",
          href: "https://www.instagram.com/caramelo_tech/",
        },
      ],
      sidebar: [
        {
          label: "Fundamentos",
          autogenerate: { directory: "fundamentos" },
        },
      ],
      defaultLocale: "root",
      locales: {
        root: { label: "Português", lang: "pt-BR" },
      },
    }),
  ],
});

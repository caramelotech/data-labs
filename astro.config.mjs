import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://caramelotech.github.io',
  base: '/caramelo-labs',
  integrations: [
    starlight({
      title: 'Caramelo Labs',
      customCss: ['./src/styles/custom.css'],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/caramelotech/caramelo-labs',
        },
      ],
      defaultLocale: 'root',
      locales: {
        root: { label: 'Português', lang: 'pt-BR' },
      },
    }),
  ],
});

// The OpenDFX website (M9). The pages come from book/ through tools/build_site.py,
// which `npm run build` and `npm run dev` run first. See site/README.md.
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import sidebar from './src/generated/sidebar.json' with { type: 'json' };
import labelTaskCheckboxes from './src/plugins/label-task-checkboxes.mjs';

export default defineConfig({
  site: 'https://opendfx.org',
  trailingSlash: 'always',
  markdown: { rehypePlugins: [labelTaskCheckboxes] },
  integrations: [
    starlight({
      title: 'OpenDFX for Printed Circuit Boards',
      description:
        'Practical advice for designing printed circuit boards that are easy to make, assemble and test.',
      lastUpdated: false,
      // The logo (M44): public/favicon.svg, favicon.ico and apple-touch-icon.png, made by tools/logo/build_brand.py.
      favicon: '/favicon.svg',
      head: [
        { tag: 'link', attrs: { rel: 'icon', href: '/favicon.ico', sizes: '48x48' } },
        { tag: 'link', attrs: { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' } },
        // The link preview (Q237): the picture shown when a page is shared, from tools/logo/build_brand.py.
        { tag: 'meta', attrs: { property: 'og:image', content: 'https://opendfx.org/og-image.png' } },
        { tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } },
        { tag: 'meta', attrs: { property: 'og:image:height', content: '630' } },
        { tag: 'meta', attrs: { property: 'og:image:alt', content: 'The OpenDFX logo beside the title OpenDFX for Printed Circuit Boards, with the address opendfx.org.' } },
        { tag: 'meta', attrs: { name: 'twitter:image', content: 'https://opendfx.org/og-image.png' } },
      ],
      editLink: { baseUrl: 'https://github.com/OpenDFX/OpenDFX/edit/main/' },
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/OpenDFX/OpenDFX' }],
      customCss: ['./src/styles/opendfx.css'],
      components: { Footer: './src/components/Footer.astro', SiteTitle: './src/components/SiteTitle.astro' },
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 2 },
      sidebar: [
        { label: 'Home', link: '/' },
        { label: 'Preface', link: '/preface/' },
        ...sidebar,
        { label: 'KiCad design rules', link: '/kicad/' },
        { label: 'Set up your AI tool', link: '/ai/' },
        { label: 'About the book', link: '/about/' },
        { label: 'How to cite', link: '/cite/' },
        { label: 'Change log', link: '/changelog/' },
        { label: 'Logo and press kit', link: '/brand/' },
      ],
      // The PDF and EPUB are built by tools/build_books.py and copied into dist/ by the workflow after the site is built.
      plugins: [starlightLinksValidator({ errorOnLocalLinks: false, exclude: ['/PCB-*/', '/opendfx-pcb.pdf', '/opendfx-pcb.epub'] })],
    }),
  ],
});

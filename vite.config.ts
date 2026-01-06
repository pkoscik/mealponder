import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

const proxyConfig = {
	'/api': {
		target: process.env.BACKEND_URL || 'http://localhost:8000',
		changeOrigin: true,
		rewrite: (path) => path.replace(/^\/api/, '')
	},
	'/uploads': {
		target: process.env.BACKEND_URL || 'http://localhost:8000',
		changeOrigin: true
	}
};

export default defineConfig({
	plugins: [sveltekit(), tailwindcss()],
	server: {
		proxy: proxyConfig
	},
	preview: {
		proxy: proxyConfig
	}
});
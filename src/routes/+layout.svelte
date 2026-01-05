<script lang="ts">
	import '../app.css';
	import { Tooltip } from 'bits-ui';
	import favicon from '$lib/assets/favicon.svg';
	import LinkSimple from 'phosphor-svelte/lib/LinkSimple';
	import GithubLogo from 'phosphor-svelte/lib/GithubLogo';
	import Question from 'phosphor-svelte/lib/Question';

	let { children } = $props();
</script>

<svelte:head>
	<title>mealponder</title>
	<link rel="icon" href={favicon} />
</svelte:head>

<Tooltip.Provider>
	<div class="h-screen flex flex-col font-sans overflow-hidden bg-background">
		<header
			class="bg-background-alt px-6 py-3 flex items-center justify-between shrink-0 z-40 border-b border-border"
		>
			<a href="/" class="flex items-center gap-2 hover:opacity-80 transition-opacity">
				<img src={favicon} alt="mealponder" class="size-6" />
				<span class="font-bold text-lg tracking-tight text-foreground">mealponder</span>
			</a>

			<Tooltip.Root delayDuration={0}>
				<Tooltip.Trigger
					class="p-2 rounded-full hover:bg-gray-100 text-gray-500 hover:text-black transition-colors cursor-pointer"
				>
					<LinkSimple class="size-5" />
				</Tooltip.Trigger>

				<Tooltip.Content
					class="py-2 px-3 bg-black text-white text-xs rounded-lg shadow-xl z-50 min-w-[120px]"
					sideOffset={8}
				>
					<div class="flex flex-col gap-2">
						<a
							href="https://github.com/pkoscik/mealponder"
							target="_blank"
							rel="noreferrer"
							class="flex items-center gap-2 hover:text-gray-300 transition-colors"
						>
							<GithubLogo class="size-4" />
							<span>GitHub</span>
						</a>
						<div class="h-[1px] bg-white/20 w-full"></div>
						<a href="/help" class="flex items-center gap-2 hover:text-gray-300 transition-colors">
							<Question class="size-4" />
							<span>Help</span>
						</a>
					</div>
					<Tooltip.Arrow class="border-t-black" />
				</Tooltip.Content>
			</Tooltip.Root>
		</header>

		<main class="flex-1 overflow-y-auto relative flex flex-col">
			{@render children()}
		</main>

		<footer class="bg-background-alt py-4 text-center shrink-0 border-t border-border z-40">
			<p class="text-xs text-muted-foreground">
				&copy; {new Date().getFullYear()}. Built with Svelte & bits-ui.
			</p>
		</footer>
	</div>
</Tooltip.Provider>

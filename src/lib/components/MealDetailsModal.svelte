<script>
	import { fade, scale } from 'svelte/transition';
	import { marked } from 'marked';
	import StarRating from './StarRating.svelte';
	import CornersOut from 'phosphor-svelte/lib/CornersOut';
	import X from 'phosphor-svelte/lib/X';

	let { meal, isOpen, onClose } = $props();

	let isImageFullscreen = $state(false);

	let htmlContent = $derived.by(() => {
		if (!meal?.description) return '<em>No description provided.</em>';
		try {
			return marked.parse(meal.description);
		} catch (e) {
			return meal.description.replace(/\n/g, '<br>');
		}
	});

	function toggleFullscreen(e) {
		e?.stopPropagation();
		isImageFullscreen = !isImageFullscreen;
	}
</script>

{#if isOpen && meal}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<div
		class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
		onclick={onClose}
		transition:fade={{ duration: 200 }}
	>
		<div
			class="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden relative"
			onclick={(e) => e.stopPropagation()}
			transition:scale={{ duration: 200, start: 0.95 }}
		>
			<div class="h-48 w-full bg-gray-100 relative shrink-0 group">
				{#if meal.assets?.[0]}
					<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
					<img
						src={meal.assets[0]}
						alt={meal.name}
						class="w-full h-full object-cover cursor-pointer"
						onclick={toggleFullscreen}
					/>

					<button
						onclick={toggleFullscreen}
						class="absolute top-4 left-4 bg-black/50 hover:bg-black/70 text-white rounded-full p-2 w-8 h-8 flex items-center justify-center transition-colors backdrop-blur-sm opacity-0 group-hover:opacity-100"
						title="View Fullscreen"
					>
						<CornersOut size={16} />
					</button>
				{/if}

				<button
					onclick={onClose}
					class="absolute top-4 right-4 bg-black/50 hover:bg-black/70 text-white rounded-full p-1 w-8 h-8 flex items-center justify-center transition-colors backdrop-blur-sm"
				>
					&times;
				</button>
			</div>

			<div class="p-6 overflow-y-auto">
				<div class="flex items-center justify-between mb-2">
					<h2 class="text-2xl font-bold">{meal.name}</h2>
					{#if meal.rating > 0}
						<StarRating value={meal.rating} readonly size="md" />
					{/if}
				</div>

				<div class="flex gap-2 mb-6 flex-wrap">
					{#each meal.tags as tag}
						<span class="bg-gray-100 px-3 py-1 rounded-full text-sm text-gray-700 font-medium"
							>{tag}</span
						>
					{/each}
				</div>

				<div class="prose prose-sm max-w-none text-gray-700 leading-relaxed">
					{@html htmlContent}
				</div>
			</div>
		</div>
	</div>

	{#if isImageFullscreen && meal.assets?.[0]}
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div
			class="fixed inset-0 z-[60] bg-black/95 flex items-center justify-center p-4 cursor-zoom-out"
			onclick={toggleFullscreen}
			transition:fade={{ duration: 200 }}
		>
			<img
				src={meal.assets[0]}
				alt={meal.name}
				class="max-w-full max-h-full object-contain rounded-sm shadow-2xl"
			/>

			<button
				class="absolute top-5 right-5 text-white/70 hover:text-white transition-colors"
				onclick={toggleFullscreen}
			>
				<X size={24} />
			</button>
		</div>
	{/if}
{/if}

<style>
	/* HACK(pkoscik): Tailwind's preflight nukes
	 * markdown-derived formatting. Manually restore
	 * 'standard' CSS for these elements
	 */
	:global(.prose :is(ul, ol)) {
		padding-left: 1.625rem;
		margin-block: 1rem;
	}
	:global(.prose ul) {
		list-style: disc;
	}
	:global(.prose ol) {
		list-style: decimal;
	}
	:global(.prose li) {
		margin-block: 0.25rem;
	}
	:global(.prose :is(ul, ol) :is(ul, ol)) {
		margin-block: 0.5rem;
	}

	:global(.prose :is(h1, h2, h3)) {
		font-weight: 600;
		color: #374151;
		margin-bottom: 0.5rem;
	}
	:global(.prose :is(h2, h3)) {
		line-height: 1.75rem;
	}

	:global(.prose h1) {
		font-size: 1.5rem;
		line-height: 2rem;
		font-weight: 700;
		color: #111827;
		margin-top: 1.5rem;
		margin-bottom: 0.75rem;
	}
	:global(.prose h2) {
		font-size: 1.25rem;
		margin-top: 1.25rem;
	}
	:global(.prose h3) {
		font-size: 1.125rem;
		margin-top: 1rem;
	}
</style>

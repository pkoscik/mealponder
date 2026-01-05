<script>
	import MealDetailsModal from './MealDetailsModal.svelte';
	import StarRating from './StarRating.svelte';
	import Image from 'phosphor-svelte/lib/Image';

	let { meal } = $props();
	let isDetailsOpen = $state(false);

	function openModal() {
		isDetailsOpen = true;
	}

	function getCleanDescription(text) {
		if (!text) return '';
		return text.replace(/[#*`_]/g, '').trim();
	}
</script>

<div
	class="group relative border rounded-[15px] p-2 bg-white cursor-pointer hover:border-gray-300 transition-all hover:shadow-sm flex gap-3 min-h-[7rem] overflow-hidden"
	onclick={openModal}
	onkeydown={(e) => e.key === 'Enter' && openModal()}
	role="button"
	tabindex="0"
>
	<div class="shrink-0 w-20 h-20 rounded-lg overflow-hidden bg-gray-50 relative shadow-inner">
		{#if meal.assets?.[0]}
			<img
				src={meal.assets[0]}
				alt={meal.name}
				class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
			/>
		{:else}
			<div class="w-full h-full flex items-center justify-center">
				<Image size={20} weight="regular" />
			</div>
		{/if}
	</div>

	<div class="flex flex-col flex-1 min-w-0 justify-between py-0.5">
		<div>
			<h3 class="font-semibold text-gray-900 truncate text-sm mb-0.5 pr-8">{meal.name}</h3>

			<p class="text-[11px] text-gray-500 line-clamp-2 leading-relaxed font-medium">
				{getCleanDescription(meal.description) || 'No description available.'}
			</p>
		</div>

		<div class="flex items-end justify-between gap-2 mt-1">
			<div class="flex gap-1 flex-wrap items-center">
				{#each meal.tags as tag}
					<span
						class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-gray-50 text-gray-600 border border-gray-100 uppercase tracking-wide"
					>
						{tag}
					</span>
				{/each}
			</div>

			{#if meal.rating > 0}
				<div class="shrink-0">
					<StarRating value={meal.rating} readonly size="sm" />
				</div>
			{/if}
		</div>
	</div>
</div>

<MealDetailsModal isOpen={isDetailsOpen} onClose={() => (isDetailsOpen = false)} {meal} />

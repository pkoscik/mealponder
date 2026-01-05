<script>
	import { RatingGroup } from 'bits-ui';
	import Star from 'phosphor-svelte/lib/Star';
	import StarHalf from 'phosphor-svelte/lib/StarHalf';

	let { value = $bindable(0), readonly = false, size = 'sm' } = $props();

	const sizeClass = size === 'sm' ? 'size-4' : 'size-6';
</script>

<RatingGroup.Root bind:value max={5} allowHalf={true} {readonly} class="flex gap-0.5">
	{#snippet children({ items })}
		{#each items as item (item.index)}
			<RatingGroup.Item
				index={item.index}
				class="{readonly
					? 'cursor-default'
					: 'cursor-pointer'} text-gray-300 data-[state=active]:text-yellow-400 data-[state=partial]:text-yellow-400 transition-colors"
			>
				{#if item.state === 'inactive'}
					<Star class={sizeClass} weight="regular" />
				{:else if item.state === 'active'}
					<Star class={sizeClass} weight="fill" />
				{:else if item.state === 'partial'}
					<StarHalf class={sizeClass} weight="fill" />
				{/if}
			</RatingGroup.Item>
		{/each}
	{/snippet}
</RatingGroup.Root>

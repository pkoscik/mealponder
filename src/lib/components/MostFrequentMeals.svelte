<script>
	import { api } from '$lib/api';
	import { RadioGroup, Label, Pagination } from 'bits-ui';
	import Meal from './Meal.svelte';
	import CaretLeft from 'phosphor-svelte/lib/CaretLeft';
	import CaretRight from 'phosphor-svelte/lib/CaretRight';

	let { updateTrigger = 0 } = $props();

	let duration = $state('365');
	let frequentMeals = $state([]);
	let isRefreshing = $state(false);

	let page = $state(1);
	const perPage = 3;

	const options = [
		{ value: '7', label: '7 Days' },
		{ value: '30', label: '30 Days' },
		{ value: '365', label: 'Year' }
	];

	$effect(() => {
		duration;
		updateTrigger;

		async function fetchFrequent() {
			isRefreshing = true;
			try {
				const data = await api.getFrequentMeals(duration);
				frequentMeals = data || [];
				if (frequentMeals.length < (page - 1) * perPage) {
					page = 1;
				}
			} catch (e) {
				console.error('Error fetching analytics', e);
			} finally {
				isRefreshing = false;
			}
		}
		fetchFrequent();
	});

	let paginatedItems = $derived(frequentMeals.slice((page - 1) * perPage, page * perPage));
</script>

<div
	class="border-dark-10 bg-background-alt shadow-card rounded-[15px] border p-[22px] flex flex-col gap-4"
>
	<div class="flex items-center justify-between mb-2">
		<h3 class="font-medium">Top Meals</h3>

		<RadioGroup.Root bind:value={duration} class="flex items-center gap-3">
			{#each options as opt}
				<div class="flex items-center gap-2">
					<RadioGroup.Item
						value={opt.value}
						id="r-{opt.value}"
						class="size-4 rounded-full border border-border-input hover:border-dark-40
                               data-[state=checked]:border-black data-[state=checked]:border-4 
                               bg-transparent"
					/>
					<Label.Root for="r-{opt.value}" class="text-xs font-medium text-gray-600 cursor-pointer">
						{opt.label}
					</Label.Root>
				</div>
			{/each}
		</RadioGroup.Root>
	</div>

	<div class="min-h-[220px] relative">
		{#if frequentMeals.length === 0 && isRefreshing}
			<div class="absolute inset-0 flex items-center justify-center text-gray-400 text-sm">
				Calculating...
			</div>
		{:else if frequentMeals.length === 0}
			<div class="absolute inset-0 flex items-center justify-center text-gray-400 text-sm">
				No data for this period.
			</div>
		{:else}
			<div class="flex flex-col gap-3" class:opacity-50={isRefreshing}>
				{#each paginatedItems as item (item.meal.id)}
					<div class="relative">
						<Meal meal={item.meal} />
						<span
							class="absolute -top-2 -right-2 bg-black text-white text-[10px] font-bold px-2 py-1 rounded-full shadow-sm"
						>
							x{item.count}
						</span>
					</div>
				{/each}
			</div>
		{/if}
	</div>

	{#if frequentMeals.length > perPage}
		<div class="mt-auto border-t pt-3">
			<Pagination.Root count={frequentMeals.length} {perPage} bind:page siblingCount={0}>
				{#snippet children({ pages, range })}
					<div class="flex items-center justify-between">
						<Pagination.PrevButton
							class="hover:bg-gray-100 disabled:text-gray-300 inline-flex size-8 items-center justify-center rounded-[9px] bg-transparent active:scale-[0.98] disabled:cursor-not-allowed"
						>
							<CaretLeft size={16} />
						</Pagination.PrevButton>

						<div class="flex items-center gap-1">
							{#each pages as page (page.key)}
								{#if page.type === 'page'}
									<Pagination.Page
										{page}
										class="hover:bg-gray-100 data-[selected]:bg-black data-[selected]:text-white inline-flex size-8 items-center justify-center rounded-[9px] bg-transparent text-[13px] font-medium"
									>
										{page.value}
									</Pagination.Page>
								{/if}
							{/each}
						</div>

						<Pagination.NextButton
							class="hover:bg-gray-100 disabled:text-gray-300 inline-flex size-8 items-center justify-center rounded-[9px] bg-transparent active:scale-[0.98] disabled:cursor-not-allowed"
						>
							<CaretRight size={16} />
						</Pagination.NextButton>
					</div>
				{/snippet}
			</Pagination.Root>
		</div>
	{/if}
</div>

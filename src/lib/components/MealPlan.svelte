<script>
	import { api } from '$lib/api';
	import Meal from './Meal.svelte';
	import Trash from 'phosphor-svelte/lib/Trash';

	let { date, onUpdate, updateTrigger = 0 } = $props();

	let plannedMeals = $state([]);
	let isRefreshing = $state(false);

	$effect(() => {
		date;
		updateTrigger;
		if (!date) return;

		async function fetchPlan() {
			isRefreshing = true;
			try {
				const meals = await api.getPlanForDate(date);
				plannedMeals = meals || [];
			} catch (e) {
				console.error('Error fetching plan:', e);
				plannedMeals = [];
			} finally {
				isRefreshing = false;
			}
		}
		fetchPlan();
	});

	async function removeMeal(mealId) {
		if (!date) return;

		const prev = [...plannedMeals];
		plannedMeals = plannedMeals.filter((m) => m.id !== mealId);

		try {
			await api.removeMealFromPlan(date, mealId);
			if (onUpdate) onUpdate();
		} catch (e) {
			alert('Could not remove meal.');
			plannedMeals = prev;
		}
	}
</script>

<div
	class="border-dark-10 bg-background-alt shadow-card rounded-[15px] border p-[22px] flex flex-col gap-4"
>
	<h3 class="font-medium mb-2 flex items-baseline justify-between">
		{#if date}
			Meal plan for {date}
			{#if plannedMeals.length > 0}
				<span class="text-gray-400 text-sm font-normal">{plannedMeals.length}</span>
			{/if}
		{:else}
			Select a date
		{/if}
	</h3>

	<div class="min-h-[200px] relative">
		{#if isRefreshing && plannedMeals.length === 0}
			<div
				class="absolute inset-0 flex items-center justify-center text-gray-400 text-sm z-10 bg-background-alt/80"
			>
				Loading...
			</div>
		{/if}

		{#if plannedMeals.length === 0 && !isRefreshing}
			<div class="absolute inset-0 flex items-center justify-center">
				<div class="text-center">
					<p class="text-gray-500 text-sm">No meals planned.</p>
					<p class="text-gray-400 text-xs mt-1">Select a date and add meals.</p>
				</div>
			</div>
		{/if}

		<div class="flex flex-col gap-3" class:opacity-50={isRefreshing}>
			{#each plannedMeals as meal (meal.id)}
				<div class="relative group">
					<Meal {meal} />

					<button
						onclick={(e) => {
							e.stopPropagation();
							removeMeal(meal.id);
						}}
						class="absolute top-2 right-2 p-1.5 bg-white/80 hover:bg-red-50 text-gray-400 hover:text-red-500 rounded-md opacity-0 group-hover:opacity-100 shadow-sm border border-transparent hover:border-red-100 cursor-pointer z-10"
						title="Remove meal"
					>
						<Trash size={14} />
					</button>
				</div>
			{/each}
		</div>
	</div>
</div>

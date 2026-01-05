<script>
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import { Pagination } from 'bits-ui';
	import Meal from '$lib/components/Meal.svelte';
	import AddMealModal from '$lib/components/AddMealModal.svelte';
	import DotsThreeVertical from 'phosphor-svelte/lib/DotsThreeVertical';
	import CaretLeft from 'phosphor-svelte/lib/CaretLeft';
	import CaretRight from 'phosphor-svelte/lib/CaretRight';
	import Plus from 'phosphor-svelte/lib/Plus';
	import PencilSimple from 'phosphor-svelte/lib/PencilSimple';
	import Trash from 'phosphor-svelte/lib/Trash';

	let { onAdd, onMealUpdated } = $props();

	let search = $state('');
	let page = $state(1);
	const perPage = 5;

	let allMeals = $state([]);
	let loading = $state(true);
	let isEditorOpen = $state(false);
	let editingMeal = $state(null);
	let activeMobileId = $state(null);

	async function fetchMeals() {
		loading = true;
		try {
			allMeals = await api.getMeals();
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	}

	onMount(fetchMeals);

	let filteredMeals = $derived(
		allMeals.filter((meal) => {
			const s = search.trim().toLowerCase();
			if (s === '') return true;
			if (s.startsWith('#')) {
				const tagQuery = s.slice(1);
				if (tagQuery === '') return true;
				return meal.tags.some((tag) => tag.toLowerCase().includes(tagQuery));
			}
			return meal.name && meal.name.toLowerCase().includes(s);
		})
	);

	let paginatedMeals = $derived(filteredMeals.slice((page - 1) * perPage, page * perPage));

	$effect(() => {
		search;
		page = 1;
	});

	function handleSave(savedMeal) {
		const index = allMeals.findIndex((m) => m.id === savedMeal.id);
		if (index !== -1) {
			allMeals[index] = savedMeal;
		} else {
			allMeals = [...allMeals, savedMeal];
		}
		if (onMealUpdated) onMealUpdated();
	}

	function openAdd() {
		editingMeal = null;
		isEditorOpen = true;
	}

	function openEdit(meal) {
		editingMeal = meal;
		isEditorOpen = true;
		activeMobileId = null;
	}

	async function deleteMeal(meal) {
		if (!confirm(`Are you sure you want to delete "${meal.name}"?`)) return;

		try {
			const success = await api.deleteMeal(meal.id);
			if (success) {
				allMeals = allMeals.filter((m) => m.id !== meal.id);
				if (onMealUpdated) onMealUpdated();
			} else {
				alert('Failed to delete meal');
			}
		} catch (e) {
			console.error(e);
			alert('Error connecting to server');
		}
		activeMobileId = null;
	}

	function toggleMobileMenu(e, id) {
		e.stopPropagation();
		activeMobileId = activeMobileId === id ? null : id;
	}
</script>

<AddMealModal
	isOpen={isEditorOpen}
	meal={editingMeal}
	onClose={() => (isEditorOpen = false)}
	onSave={handleSave}
/>

<svelte:window onclick={() => (activeMobileId = null)} />

<div
	class="border-dark-10 bg-background-alt shadow-card rounded-[15px] border p-[22px] flex flex-col gap-4"
>
	<div class="flex gap-2">
		<input
			type="text"
			placeholder="Search meals..."
			bind:value={search}
			class="p-2 border rounded flex-1 min-w-0"
		/>
		<button
			onclick={openAdd}
			class="bg-black text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors whitespace-nowrap flex items-center gap-2"
		>
			<Plus size={16} weight="bold" /> Add Meal
		</button>
	</div>

	<div class="flex flex-col gap-4 min-h-[300px]">
		{#if loading}
			<p class="text-gray-500">Loading meals...</p>
		{:else}
			{#each paginatedMeals as meal (meal.id)}
				<div class="relative group">
					<Meal {meal} />

					<button
						onclick={(e) => toggleMobileMenu(e, meal.id)}
						class="absolute top-2 right-2 p-1.5 rounded-full bg-white/90 text-gray-500 shadow-sm border border-gray-100 md:hidden z-20"
						class:opacity-0={activeMobileId === meal.id}
						class:pointer-events-none={activeMobileId === meal.id}
					>
						<DotsThreeVertical weight="bold" class="size-5" />
					</button>

					<div
						class="absolute top-2 right-2 flex gap-1 transition-all z-30 opacity-0 md:group-hover:opacity-100"
						class:opacity-100={activeMobileId === meal.id}
						class:pointer-events-none={activeMobileId !== meal.id &&
							typeof window !== 'undefined' &&
							window.innerWidth < 768}
					>
						<button
							onclick={(e) => {
								e.stopPropagation();
								deleteMeal(meal);
							}}
							class="p-2 bg-white hover:bg-red-50 text-gray-400 hover:text-red-600 rounded-md shadow-sm border border-transparent hover:border-red-100 cursor-pointer"
							title="Delete meal"
						>
							<Trash size={16} />
						</button>

						<button
							onclick={(e) => {
								e.stopPropagation();
								openEdit(meal);
							}}
							class="p-2 bg-white hover:bg-blue-50 text-gray-400 hover:text-blue-600 rounded-md shadow-sm border border-transparent hover:border-blue-100 cursor-pointer"
							title="Edit meal"
						>
							<PencilSimple size={16} />
						</button>
						<button
							onclick={(e) => {
								e.stopPropagation();
								onAdd && onAdd(meal);
								activeMobileId = null;
							}}
							class="p-2 bg-white hover:bg-green-50 text-gray-400 hover:text-green-600 rounded-md shadow-sm border border-transparent hover:border-green-100 cursor-pointer"
							title="Add to plan"
						>
							<Plus size={16} strokeWidth={2.5} />
						</button>
					</div>
				</div>
			{/each}
			{#if filteredMeals.length === 0}
				<p class="text-muted-foreground text-sm">No meals found.</p>
			{/if}
		{/if}
	</div>

	{#if filteredMeals.length > perPage}
		<div class="mt-auto border-t pt-4">
			<Pagination.Root count={filteredMeals.length} {perPage} bind:page siblingCount={1}>
				{#snippet children({ pages, range })}
					<div class="flex items-center justify-between">
						<Pagination.PrevButton
							class="hover:bg-gray-100 disabled:text-gray-300 inline-flex size-9 items-center justify-center rounded-[9px] bg-transparent active:scale-[0.98] disabled:cursor-not-allowed"
						>
							<CaretLeft size={20} />
						</Pagination.PrevButton>
						<div class="flex items-center gap-1">
							{#each pages as page (page.key)}
								{#if page.type === 'page'}
									<Pagination.Page
										{page}
										class="hover:bg-gray-100 data-[selected]:bg-black data-[selected]:text-white inline-flex size-9 items-center justify-center rounded-[9px] bg-transparent text-[15px] font-medium"
									>
										{page.value}
									</Pagination.Page>
								{:else}
									<div class="text-gray-500 px-2">...</div>
								{/if}
							{/each}
						</div>
						<Pagination.NextButton
							class="hover:bg-gray-100 disabled:text-gray-300 inline-flex size-9 items-center justify-center rounded-[9px] bg-transparent active:scale-[0.98] disabled:cursor-not-allowed"
						>
							<CaretRight size={20} />
						</Pagination.NextButton>
					</div>
				{/snippet}
			</Pagination.Root>
		</div>
	{/if}
</div>

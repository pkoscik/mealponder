<script>
	import { api } from '$lib/api';
	import { getLocalTimeZone, today } from '@internationalized/date';
	import Calendar from '$lib/components/Calendar.svelte';
	import MostFrequentMeals from '$lib/components/MostFrequentMeals.svelte';
	import MealPlan from '$lib/components/MealPlan.svelte';
	import MealList from '$lib/components/MealList.svelte';

	const currentDate = today(getLocalTimeZone());
	let value = $state(currentDate);
	let dateStr = $derived(value ? value.toString() : '');

	let updateTrigger = $state(0);

	async function handleAddMeal(meal) {
		if (!dateStr) {
			alert('Please select a date first.');
			return;
		}
		try {
			const success = await api.addMealToPlan(dateStr, meal);
			if (success) {
				updateTrigger++;
			} else {
				alert('Failed to add meal');
			}
		} catch (e) {
			console.error(e);
			alert('Failed to add meal');
		}
	}

	function refreshData() {
		updateTrigger++;
	}
</script>

<div class="layout">
	<div class="column">
		<div class="calendar-wrapper">
			<Calendar bind:value {updateTrigger} />
		</div>
		<MostFrequentMeals {updateTrigger} />
	</div>

	<div class="column">
		<MealPlan date={dateStr} {updateTrigger} onUpdate={() => updateTrigger++} />
	</div>

	<div class="column">
		<MealList onAdd={handleAddMeal} onMealUpdated={refreshData} />
	</div>
</div>

<style>
	.layout {
		display: flex;
		justify-content: center;
		gap: 1.5rem;
		width: 100%;
		height: 100%;
		padding: 2rem 1rem;
		box-sizing: border-box;
		overflow-x: auto;
	}

	.column {
		width: 350px;
		flex-shrink: 0;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.calendar-wrapper {
		width: 100%;
	}

	@media (max-width: 1100px) {
		.layout {
			flex-direction: column;
			align-items: center;
			height: auto; /* let it grow on mobile (scroll down) */
		}
		.column {
			width: 100%;
			max-width: 400px;
		}
	}
</style>

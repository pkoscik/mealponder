<script>
	import { api } from '$lib/api';
	import { Calendar } from 'bits-ui';
	import CaretLeft from 'phosphor-svelte/lib/CaretLeft';
	import CaretRight from 'phosphor-svelte/lib/CaretRight';

	let { value = $bindable(), updateTrigger = 0 } = $props();

	let mealCounts = $state({});

	$effect(() => {
		// XXX(pkoscik):
		// Re-fetch meals upon the update trigger.
		// This can be (and is :p) used to keep the state between components in sync.
		updateTrigger;
		fetchMealCounts();
	});

	async function fetchMealCounts() {
		try {
			const data = await api.getAllPlans();
			const counts = {};
			for (const [date, meals] of Object.entries(data)) {
				if (Array.isArray(meals)) {
					counts[date] = meals.length;
				}
			}
			mealCounts = counts;
		} catch (e) {
			console.error('Failed to fetch meal counts for calendar:', e);
		}
	}

	function getMealCount(date) {
		return mealCounts[date.toString()] || 0;
	}
</script>

<Calendar.Root
	class="border-dark-10 bg-background-alt shadow-card rounded-[15px] border p-[22px]"
	locale="en-PL"
	weekdayFormat="short"
	fixedWeeks={true}
	type="single"
	bind:value
>
	{#snippet children({ months, weekdays })}
		<Calendar.Header class="flex items-center justify-between">
			<Calendar.PrevButton
				class="rounded-9px bg-background-alt hover:bg-muted inline-flex size-10 items-center justify-center active:scale-[0.98] active:transition-all"
			>
				<CaretLeft class="size-6" />
			</Calendar.PrevButton>
			<Calendar.Heading class="text-[15px] font-medium" />
			<Calendar.NextButton
				class="rounded-9px bg-background-alt hover:bg-muted inline-flex size-10 items-center justify-center active:scale-[0.98] active:transition-all"
			>
				<CaretRight class="size-6" />
			</Calendar.NextButton>
		</Calendar.Header>

		<div class="months-container">
			{#each months as month, i (i)}
				<Calendar.Grid class="calendar-grid">
					<Calendar.GridHead>
						<Calendar.GridRow class="grid grid-cols-7 gap-1">
							{#each weekdays as day, i (i)}
								<Calendar.HeadCell class="text-muted-foreground font-normal! text-xs text-center">
									<div>{day.slice(0, 2)}</div>
								</Calendar.HeadCell>
							{/each}
						</Calendar.GridRow>
					</Calendar.GridHead>

					<Calendar.GridBody>
						{#each month.weeks as weekDates, i (i)}
							<Calendar.GridRow class="grid grid-cols-7 gap-1">
								{#each weekDates as date, i (i)}
									<Calendar.Cell {date} month={month.value}>
										<Calendar.Day
											class="rounded-9px text-foreground hover:border-foreground 
                             data-selected:bg-foreground data-selected:text-background 
                             data-disabled:text-foreground/30 data-unavailable:text-muted-foreground 
                             data-disabled:pointer-events-none data-outside-month:pointer-events-none 
                             data-selected:font-medium data-unavailable:line-through group relative inline-flex size-10 items-center justify-center whitespace-nowrap border border-transparent bg-transparent p-0 text-sm font-normal text-center"
										>
											<div
												class="bg-foreground group-data-selected:bg-background group-data-today:block absolute top-[5px] hidden size-1 rounded-full"
											></div>

											{date.day}

											{@const count = getMealCount(date)}
											{#if count > 0}
												<div
													class="absolute bottom-[5px] size-1 rounded-full {count === 1
														? 'bg-yellow-200'
														: 'bg-green-300'}"
												></div>
											{/if}
										</Calendar.Day>
									</Calendar.Cell>
								{/each}
							</Calendar.GridRow>
						{/each}
					</Calendar.GridBody>
				</Calendar.Grid>
			{/each}
		</div>
	{/snippet}
</Calendar.Root>

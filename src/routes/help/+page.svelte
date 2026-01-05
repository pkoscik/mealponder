<script>
	import { Separator } from 'bits-ui';
	import CalendarBlank from 'phosphor-svelte/lib/CalendarBlank';
	import ForkKnife from 'phosphor-svelte/lib/ForkKnife';
	import ChartBar from 'phosphor-svelte/lib/ChartBar';
</script>

<div class="max-w-3xl mx-auto w-full p-6 md:p-12">
	<div class="space-y-2 mb-8">
		<h1 class="text-3xl font-bold tracking-tight text-gray-900">Help & Guide</h1>
		<p class="text-gray-500 text-lg">
			Everything you need to know to manage your meals effectively.
		</p>
	</div>

	<div class="grid gap-8">
		<section class="space-y-4">
			<div class="flex items-center gap-3 text-xl font-semibold text-gray-800">
				<div class="p-2 bg-blue-50 text-blue-600 rounded-lg">
					<ForkKnife size={24} weight="duotone" />
				</div>
				<h2>Managing Meals</h2>
			</div>
			<Separator.Root class="h-[1px] bg-gray-200 w-full" />
			<div class="prose prose-gray max-w-none text-gray-600 space-y-2">
				<p>
					The <strong>Meal List</strong> is your central database of recipes and dishes.
				</p>
				<ul class="list-disc pl-5 space-y-1">
					<li>
						<strong>Add a Meal:</strong> Click the
						<span class="bg-black text-white text-xs px-1.5 py-0.5 rounded">Add Meal</span> button. You
						can provide a name, description (with Markdown support), tags, rating, and even upload a photo.
					</li>
					<li>
						<strong>Edit/Delete:</strong> Hover over any meal card (or tap the menu dots on mobile) to
						reveal the Edit (pencil) and Delete (trash) buttons.
					</li>
					<li>
						<strong>Search:</strong> Use the search bar to filter meals by name. You can also search
						by tags using the <code>#</code> prefix (e.g., <code>#dinner</code>).
					</li>
				</ul>
			</div>
		</section>

		<section class="space-y-4">
			<div class="flex items-center gap-3 text-xl font-semibold text-gray-800">
				<div class="p-2 bg-green-50 text-green-600 rounded-lg">
					<CalendarBlank size={24} weight="duotone" />
				</div>
				<h2>Planning Your Schedule</h2>
			</div>
			<Separator.Root class="h-[1px] bg-gray-200 w-full" />
			<div class="prose prose-gray max-w-none text-gray-600 space-y-2">
				<p>Plan your week by assigning meals to specific dates.</p>
				<ol class="list-decimal pl-5 space-y-1">
					<li>
						<strong>Select a Date:</strong> Click any day on the <strong>Calendar</strong>. The
						"Meals for [Date]" section will update.
					</li>
					<li>
						<strong>Add to Plan:</strong> Find a meal in your list and click the green
						<span class="text-green-600 font-bold">+</span> button. It will instantly appear in your plan
						for the selected day.
					</li>
					<li>
						<strong>Indicators:</strong> The calendar displays colored dots to help you see your
						schedule at a glance:
						<ul class="list-disc pl-5 mt-1">
							<li>
								<span class="inline-block w-2 h-2 rounded-full bg-yellow-200"></span>
								<strong>Yellow:</strong> 1 meal planned.
							</li>
							<li>
								<span class="inline-block w-2 h-2 rounded-full bg-green-300"></span>
								<strong>Green:</strong> 2 or more meals planned.
							</li>
						</ul>
					</li>
				</ol>
			</div>
		</section>

		<section class="space-y-4">
			<div class="flex items-center gap-3 text-xl font-semibold text-gray-800">
				<div class="p-2 bg-purple-50 text-purple-600 rounded-lg">
					<ChartBar size={24} weight="duotone" />
				</div>
				<h2>Analytics</h2>
			</div>
			<Separator.Root class="h-[1px] bg-gray-200 w-full" />
			<div class="prose prose-gray max-w-none text-gray-600">
				<p>
					Curious about your eating habits? The <strong>Top Meals</strong> section tracks which dishes
					you schedule most often. You can toggle the timeframe between 7 days, 30 days, or the entire
					year to see your favorites over time.
				</p>
			</div>
		</section>
	</div>

	<div
		class="mt-12 p-4 bg-gray-50 rounded-xl border border-gray-100 text-center text-sm text-gray-500"
	>
		Need more help? Check out the project on <a
			href="https://github.com/pkoscik/mealponder"
			class="text-black underline hover:no-underline">GitHub</a
		>.
	</div>
</div>

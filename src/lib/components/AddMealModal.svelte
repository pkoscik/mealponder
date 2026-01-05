<script>
	import { api } from '$lib/api';
	import { fade, scale } from 'svelte/transition';
	import StarRating from './StarRating.svelte';

	// XXX(pkoscik): `meal` can be passed to open the 'edit' mode
	let { isOpen, onClose, onSave, meal = null } = $props();

	let name = $state('');
	let description = $state('');
	let tags = $state('');
	let rating = $state(0);
	let fileInput = $state(null);
	let isSubmitting = $state(false);

	// Watch for changes in 'meal' or 'isOpen' to reset/populate form state
	$effect(() => {
		if (isOpen) {
			if (meal) {
				// Edit => pre-fill form data
				name = meal.name;
				description = meal.description || '';
				tags = meal.tags.join(', ');
				rating = meal.rating || 0;
			} else {
				// Add => reset
				resetForm();
			}
		}
	});

	async function handleSubmit(e) {
		e.preventDefault();
		isSubmitting = true;

		const mealData = {
			id: meal ? meal.id : undefined,
			name,
			description,
			tags,
			rating
		};

		const file = fileInput && fileInput.files[0] ? fileInput.files[0] : null;

		try {
			const savedMeal = await api.saveMeal(mealData, file);
			if (savedMeal) {
				onSave(savedMeal);
				onClose();
			} else {
				alert('Failed to save meal');
			}
		} catch (error) {
			console.error(error);
			alert('Error connecting to server');
		} finally {
			isSubmitting = false;
		}
	}

	function resetForm() {
		name = '';
		description = '';
		tags = '';
		rating = 0;
		if (fileInput) fileInput.value = '';
	}
</script>

{#if isOpen}
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div
		class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
		onclick={onClose}
		transition:fade={{ duration: 200 }}
	>
		<div
			class="bg-white rounded-xl shadow-xl w-full max-w-lg overflow-hidden"
			onclick={(e) => e.stopPropagation()}
			transition:scale={{ duration: 200, start: 0.95 }}
		>
			<div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
				<h2 class="text-lg font-semibold">{meal ? 'Edit Meal' : 'Add New Meal'}</h2>
				<button onclick={onClose} class="text-gray-400 hover:text-gray-600">&times;</button>
			</div>

			<form onsubmit={handleSubmit} class="p-6 space-y-4">
				<div>
					<!-- svelte-ignore a11y_label_has_associated_control -->
					<label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
					<input
						type="text"
						bind:value={name}
						required
						class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-black outline-none"
					/>
				</div>

				<div>
					<!-- svelte-ignore a11y_label_has_associated_control -->
					<label class="block text-sm font-medium text-gray-700 mb-1">Rating</label>
					<StarRating bind:value={rating} size="md" />
				</div>

				<div>
					<!-- svelte-ignore a11y_label_has_associated_control -->
					<label class="block text-sm font-medium text-gray-700 mb-1">Description (Markdown)</label>
					<textarea
						bind:value={description}
						rows="3"
						class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-black outline-none font-mono text-sm"
					></textarea>
				</div>

				<div>
					<!-- svelte-ignore a11y_label_has_associated_control -->
					<label class="block text-sm font-medium text-gray-700 mb-1">Tags</label>
					<input
						type="text"
						bind:value={tags}
						class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-black outline-none"
						placeholder="healthy, dinner"
					/>
				</div>

				<div>
					<!-- svelte-ignore a11y_label_has_associated_control -->
					<label class="block text-sm font-medium text-gray-700 mb-1">
						{meal ? 'Change Photo (optional)' : 'Photo'}
					</label>
					<input
						type="file"
						bind:this={fileInput}
						accept="image/*"
						class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-gray-100 hover:file:bg-gray-200"
					/>
				</div>

				<div class="pt-2 flex justify-end gap-3">
					<button
						type="button"
						onclick={onClose}
						class="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-lg"
						>Cancel</button
					>
					<button
						type="submit"
						disabled={isSubmitting}
						class="px-4 py-2 text-sm font-medium text-white bg-black rounded-lg hover:bg-gray-800 disabled:opacity-50"
					>
						{isSubmitting ? 'Saving...' : meal ? 'Save Changes' : 'Add Meal'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

const API_BASE = '/api';

export const api = {
	// meals
	async getMeals() {
		const res = await fetch(`${API_BASE}/meals`);
		if (!res.ok) throw new Error('API Error');
		return await res.json();
	},

	async saveMeal(mealData: any, file?: File) {
		const isEdit = !!mealData.id;
		const formData = new FormData();
		formData.append('name', mealData.name);
		formData.append('description', mealData.description);
		formData.append('tags', mealData.tags);
		formData.append('rating', mealData.rating.toString());
		if (file) formData.append('file', file);

		const url = isEdit ? `${API_BASE}/meals/${mealData.id}` : `${API_BASE}/meals`;
		const method = isEdit ? 'PUT' : 'POST';

		const res = await fetch(url, { method, body: formData });
		if (!res.ok) throw new Error('API Error');
		return await res.json();
	},

	async deleteMeal(id: string) {
		const res = await fetch(`${API_BASE}/meals/${id}`, { method: 'DELETE' });
		if (!res.ok) throw new Error('API Error');
		return true;
	},

	// plans
	async getAllPlans() {
		const res = await fetch(`${API_BASE}/plans`);
		if (!res.ok) throw new Error('API Error');
		return await res.json();
	},

	async getPlanForDate(date: string) {
		const res = await fetch(`${API_BASE}/plans/${date}`);
		if (!res.ok) throw new Error('API Error');
		return await res.json();
	},

	async addMealToPlan(date: string, meal: any) {
		const res = await fetch(`${API_BASE}/plans/${date}`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(meal)
		});
		if (!res.ok) throw new Error('API Error');
		return true;
	},

	async removeMealFromPlan(date: string, mealId: string) {
		const res = await fetch(`${API_BASE}/plans/${date}/${mealId}`, { method: 'DELETE' });
		if (!res.ok) throw new Error('API Error');
		return true;
	},

	// analytics
	async getFrequentMeals(days: string) {
		const res = await fetch(`${API_BASE}/analytics/frequent-meals?days=${days}`);
		if (!res.ok) throw new Error('API Error');
		return await res.json();
	}
};

<script setup>
import { ref, watch } from 'vue'

const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)
const shortlist = ref([])

// Mock database of restaurants
const mockDatabase = [
  { id: 'r1', name: 'Shake Shack', type: 'Burger', rating: 4.5 },
  { id: 'r2', name: 'Sweetgreen', type: 'Salads', rating: 4.8 },
  { id: 'r3', name: 'Chipotle', type: 'Mexican', rating: 4.2 },
  { id: 'r4', name: 'KazuNori', type: 'Sushi', rating: 4.9 },
  { id: 'r5', name: 'Cava', type: 'Mediterranean', rating: 4.6 },
  { id: 'r6', name: 'Dig Inn', type: 'American', rating: 4.3 },
  { id: 'r7', name: 'Noodle Bar', type: 'Asian', rating: 4.7 }
]

let debounceTimer = null

watch(searchQuery, (newQuery) => {
  if (debounceTimer) clearTimeout(debounceTimer)

  if (!newQuery.trim()) {
    searchResults.value = []
    isSearching.value = false
    return
  }

  isSearching.value = true

  debounceTimer = setTimeout(() => {
    const query = newQuery.toLowerCase()
    searchResults.value = mockDatabase.filter(
      (r) => r.name.toLowerCase().includes(query) || r.type.toLowerCase().includes(query)
    )
    isSearching.value = false
  }, 300)
})

const addToShortlist = (restaurant) => {
  if (shortlist.value.length >= 3) return
  if (shortlist.value.find((r) => r.id === restaurant.id)) return // Prevent duplicates

  shortlist.value.push(restaurant)
  searchQuery.value = '' // clear search after selecting
  searchResults.value = []
}

const removeFromShortlist = (id) => {
  shortlist.value = shortlist.value.filter((r) => r.id !== id)
}
</script>

<template>
  <div class="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold text-slate-800">Nominate Restaurants</h2>
        <p class="text-sm text-slate-500 mt-1">
          Search and shortlist up to 3 options for the group to vote on.
        </p>
      </div>
      <div class="bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded-full text-sm">
        {{ shortlist.length }} / 3
      </div>
    </div>

    <!-- Search Bar -->
    <div class="relative">
      <div class="relative">
        <svg
          class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search restaurants (e.g. Burger, Sushi, Cava)..."
          class="w-full pl-11 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500/50 focus:border-orange-500 transition-all font-medium text-slate-700 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="shortlist.length >= 3"
        />
        <!-- Loading Indicator -->
        <svg
          v-if="isSearching"
          class="absolute right-4 top-1/2 -translate-y-1/2 animate-spin h-5 w-5 text-orange-500"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      </div>

      <!-- Dropdown Results -->
      <div
        v-if="searchResults.length > 0 && searchQuery"
        class="absolute z-20 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-xl max-h-60 overflow-y-auto overflow-x-hidden divide-y divide-slate-100"
      >
        <button
          v-for="restaurant in searchResults"
          :key="restaurant.id"
          @click="addToShortlist(restaurant)"
          class="w-full flex items-center justify-between p-4 hover:bg-orange-50 transition-colors text-left group"
        >
          <div>
            <p class="font-bold text-slate-800 group-hover:text-orange-700 transition-colors">
              {{ restaurant.name }}
            </p>
            <p class="text-xs text-slate-500 mt-0.5">{{ restaurant.type }}</p>
          </div>
          <div
            class="flex items-center gap-1 text-amber-500 text-sm font-bold bg-amber-50 px-2 py-1 rounded-md"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="currentColor"
              stroke="none"
            >
              <polygon
                points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
              ></polygon>
            </svg>
            {{ restaurant.rating }}
          </div>
        </button>
      </div>

      <!-- No Results -->
      <div
        v-else-if="!isSearching && searchQuery && searchResults.length === 0"
        class="absolute z-10 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-lg p-6 text-center text-slate-500 font-medium"
      >
        No restaurants found matching "{{ searchQuery }}"
      </div>
    </div>

    <!-- Shortlist -->
    <div v-if="shortlist.length > 0" class="flex flex-col gap-3">
      <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">
        Your Nominations
      </h3>
      <div
        v-for="item in shortlist"
        :key="item.id"
        class="flex items-center justify-between bg-gradient-to-r from-orange-50 to-rose-50 border border-orange-100/50 p-4 rounded-xl shadow-sm hover:shadow transition-shadow"
      >
        <div class="flex items-center gap-4">
          <div
            class="w-12 h-12 rounded-full bg-white flex items-center justify-center text-orange-500 shadow-sm border border-orange-100 shrink-0"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path>
              <path d="M7 2v20"></path>
              <path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path>
            </svg>
          </div>
          <div>
            <p class="font-bold text-slate-800 text-lg">{{ item.name }}</p>
            <p class="text-sm text-slate-500 font-medium">{{ item.type }}</p>
          </div>
        </div>
        <button
          @click="removeFromShortlist(item.id)"
          class="p-2.5 text-slate-400 hover:text-rose-600 hover:bg-rose-100 rounded-full transition-colors active:scale-95"
          title="Remove"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <div
      v-else
      class="text-center py-8 border-2 border-dashed border-slate-200 bg-slate-50/50 rounded-xl text-slate-500 font-medium"
    >
      <p>Search for a restaurant above to add it to your nominations.</p>
    </div>

    <div
      v-if="shortlist.length >= 3"
      class="p-4 bg-emerald-50 border border-emerald-100 text-emerald-700 text-sm font-bold rounded-xl text-center flex items-center justify-center gap-2 shadow-sm"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
      Maximum nominations reached
    </div>
  </div>
</template>

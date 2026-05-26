<script setup>
import { useLunchStore } from './stores/lunch'
import { storeToRefs } from 'pinia'

const lunchStore = useLunchStore()
const { currentUserStatus, availableCoworkers, currentGroupId } = storeToRefs(lunchStore)
const { setStatus, createGroup } = lunchStore
</script>

<template>
  <div class="min-h-screen flex flex-col bg-slate-50">
    <!-- Top Navigation Bar -->
    <header
      class="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-md border-b border-slate-200 shadow-sm"
    >
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span
            class="text-2xl font-black bg-gradient-to-r from-orange-500 to-rose-500 bg-clip-text text-transparent"
          >
            Ranchi
          </span>
        </div>
        <div class="flex items-center gap-4">
          <div
            class="hidden sm:flex items-center gap-2 text-sm font-medium text-slate-600 bg-slate-100 px-3 py-1.5 rounded-full"
          >
            <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
            Online
          </div>
          <button class="p-2 text-slate-500 hover:text-slate-900 transition-colors">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content Shell -->
    <main class="flex-1 w-full max-w-7xl mx-auto p-4 flex flex-col gap-6">
      <!-- Welcome & Status Widget -->
      <section
        class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
      >
        <div>
          <h1 class="text-xl font-bold text-slate-800">Ready for Lunch?</h1>
          <p class="text-slate-500 mt-1">
            Your current status: <strong class="text-orange-600">{{ currentUserStatus }}</strong>
          </p>
        </div>
        <div class="flex gap-2">
          <button
            @click="setStatus('Looking for group')"
            class="px-4 py-2 bg-orange-100 hover:bg-orange-200 text-orange-700 font-semibold rounded-lg transition-colors text-sm"
          >
            Looking
          </button>
          <button
            @click="setStatus('Skip me')"
            class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-lg transition-colors text-sm"
          >
            Skip Today
          </button>
        </div>
      </section>

      <!-- Active Group Widget -->
      <section
        v-if="currentGroupId"
        class="bg-gradient-to-br from-orange-500 to-rose-500 rounded-2xl p-6 text-white shadow-md"
      >
        <h2 class="text-lg font-bold flex items-center gap-2">
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
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          Active Group
        </h2>
        <p class="mt-2 text-orange-100 opacity-90 text-sm">
          You are currently in group
          <span class="font-mono bg-black/20 px-2 py-0.5 rounded">{{ currentGroupId }}</span>
        </p>
      </section>

      <!-- Create Group Prompt (if no group) -->
      <section
        v-else
        class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col items-center text-center py-12"
      >
        <div
          class="w-16 h-16 bg-orange-100 text-orange-500 rounded-full flex items-center justify-center mb-4"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </div>
        <h3 class="text-lg font-bold text-slate-800">No active group</h3>
        <p class="text-slate-500 mt-1 max-w-sm">
          Start a new lunch group and invite available coworkers to vote on a restaurant.
        </p>
        <button
          @click="createGroup"
          class="mt-6 px-6 py-3 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-xl transition-all shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
        >
          Start a Group
        </button>
      </section>

      <!-- Coworkers List -->
      <section class="mt-4">
        <h3 class="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4 px-2">
          Available Coworkers
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="coworker in availableCoworkers"
            :key="coworker.id"
            class="bg-white p-4 rounded-xl border border-slate-100 flex items-center gap-4 hover:shadow-md transition-shadow cursor-pointer"
          >
            <div
              class="w-10 h-10 rounded-full bg-gradient-to-tr from-slate-200 to-slate-300 flex items-center justify-center text-slate-500 font-bold"
            >
              {{ coworker.name.charAt(0) }}
            </div>
            <div>
              <p class="font-medium text-slate-800">{{ coworker.name }}</p>
              <p
                class="text-xs font-medium mt-0.5"
                :class="
                  coworker.status === 'Looking for group' ? 'text-emerald-500' : 'text-slate-400'
                "
              >
                {{ coworker.status }}
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

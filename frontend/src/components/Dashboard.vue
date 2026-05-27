<script setup>
import { useLunchStore } from '../stores/lunch'
import { storeToRefs } from 'pinia'

const store = useLunchStore()
const { currentUserStatus, availableCoworkers, currentGroupId, isStatusLoading, isGroupLoading } =
  storeToRefs(store)
const { setStatus, createGroup } = store

const statuses = [
  {
    id: 'Looking',
    label: 'Looking for a Group',
    icon: '🔍',
    color: 'from-orange-400 to-orange-500',
    bg: 'bg-orange-50',
    text: 'text-orange-700',
    activeClass: 'ring-2 ring-orange-500 shadow-orange-200'
  },
  {
    id: 'Solo',
    label: 'Eating Solo',
    icon: '🎧',
    color: 'from-blue-400 to-blue-500',
    bg: 'bg-blue-50',
    text: 'text-blue-700',
    activeClass: 'ring-2 ring-blue-500 shadow-blue-200'
  },
  {
    id: 'Bring Own',
    label: 'Brought My Own',
    icon: '🍱',
    color: 'from-emerald-400 to-emerald-500',
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    activeClass: 'ring-2 ring-emerald-500 shadow-emerald-200'
  }
]
</script>

<template>
  <div class="flex flex-col gap-8 w-full max-w-4xl mx-auto">
    <!-- Status Section -->
    <section>
      <h2 class="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
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
          class="text-slate-400"
        >
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
        </svg>
        Today's Lunch Status
      </h2>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <button
          v-for="status in statuses"
          :key="status.id"
          @click="setStatus(status.id)"
          :disabled="isStatusLoading"
          class="relative overflow-hidden group flex flex-col items-center p-6 rounded-2xl border transition-all duration-300 shadow-sm"
          :class="[
            currentUserStatus === status.id
              ? `${status.activeClass} border-transparent ${status.bg}`
              : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-md',
            isStatusLoading && currentUserStatus !== status.id
              ? 'opacity-50 cursor-not-allowed'
              : ''
          ]"
        >
          <!-- Active Color Bar -->
          <div
            v-if="currentUserStatus === status.id"
            class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r"
            :class="status.color"
          ></div>

          <span
            class="text-3xl mb-3 drop-shadow-sm transition-transform duration-300 group-hover:scale-110"
            >{{ status.icon }}</span
          >
          <span
            class="font-semibold text-sm"
            :class="currentUserStatus === status.id ? status.text : 'text-slate-600'"
          >
            {{ status.label }}
          </span>

          <!-- Abstract Loading State -->
          <div
            v-if="isStatusLoading && currentUserStatus !== status.id"
            class="absolute inset-0 bg-white/40 flex items-center justify-center"
          ></div>
        </button>
      </div>
    </section>

    <!-- Group Action Section -->
    <section
      v-if="currentUserStatus === 'Looking'"
      class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-8 text-white shadow-xl relative overflow-hidden"
    >
      <div
        class="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-white opacity-5 rounded-full blur-3xl"
      ></div>

      <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <h2 class="text-2xl font-bold tracking-tight">Time to eat?</h2>
          <p class="text-slate-300 mt-2 max-w-md">
            Start a new lunch group and invite your coworkers to vote on a restaurant for today.
          </p>
        </div>

        <div
          v-if="currentGroupId"
          class="bg-white/10 px-6 py-4 rounded-2xl backdrop-blur-md border border-white/20 flex flex-col items-center"
        >
          <span class="text-xs uppercase tracking-wider text-slate-300 font-semibold"
            >Active Group</span
          >
          <span class="text-xl font-mono mt-1 text-emerald-400">{{ currentGroupId }}</span>
        </div>

        <button
          v-else
          @click="createGroup"
          :disabled="isGroupLoading"
          class="shrink-0 flex items-center justify-center gap-2 bg-gradient-to-r from-orange-500 to-rose-500 hover:from-orange-400 hover:to-rose-400 text-white font-bold py-3 px-8 rounded-xl transition-all shadow-lg shadow-orange-500/30 active:scale-95 disabled:opacity-70 disabled:cursor-wait"
        >
          <!-- Loading Spinner -->
          <svg
            v-if="isGroupLoading"
            class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
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
          <svg
            v-else
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
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          {{ isGroupLoading ? 'Creating...' : 'Create Group' }}
        </button>
      </div>
    </section>

    <!-- Coworkers Looking -->
    <section v-if="currentUserStatus === 'Looking' || currentUserStatus === 'Unknown'">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-slate-800 flex items-center gap-2">
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
            class="text-slate-400"
          >
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          Coworkers Looking
        </h2>
        <span class="bg-slate-100 text-slate-600 text-xs font-bold px-2 py-1 rounded-full">
          {{ availableCoworkers.filter((c) => c.status === 'Looking').length }} Online
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <template v-for="coworker in availableCoworkers" :key="coworker.id">
          <div
            v-if="coworker.status === 'Looking'"
            class="group bg-white p-4 rounded-2xl border border-slate-200 flex items-center gap-4 hover:border-orange-300 hover:shadow-md transition-all cursor-pointer"
          >
            <div
              class="relative w-12 h-12 rounded-full bg-gradient-to-tr from-slate-100 to-slate-200 flex items-center justify-center text-slate-600 font-bold border border-slate-300 group-hover:border-orange-200 transition-colors"
            >
              {{ coworker.name.charAt(0) }}
              <div
                class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-emerald-400 border-2 border-white rounded-full"
              ></div>
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-semibold text-slate-800 truncate">{{ coworker.name }}</p>
              <p class="text-xs font-medium text-emerald-500 mt-0.5 flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block"></span>
                Ready for Lunch
              </p>
            </div>
          </div>
        </template>
      </div>
    </section>
  </div>
</template>

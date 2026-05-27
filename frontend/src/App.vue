<script setup>
import Dashboard from './components/Dashboard.vue'
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
    <main class="flex-1 w-full max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 flex flex-col gap-6">
      <Dashboard />
    </main>
  </div>
</template>

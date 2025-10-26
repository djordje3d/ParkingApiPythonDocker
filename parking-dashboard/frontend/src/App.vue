<template>
  <div class="max-w-7xl mx-auto space-y-10">
    <h1 class="text-4xl font-bold text-center">Garage Dashboard - Vue - instalisani</h1>

    <!-- Simulacija dugme + status -->
    <div class="text-center space-y-4">
      <button
        @click="triggerSimulation"
        class="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-6 rounded shadow"
      >
        🔄 Simulate Entry/Exit
      </button>
      <div v-if="statusMessage" :class="statusClass" class="font-semibold text-lg">
        {{ statusMessage }}
      </div>
    </div>

    <!-- Grid za Occupancy & Revenue -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="bg-white rounded-2xl shadow-md p-6 flex flex-col items-center">
        <h2 class="text-xl font-semibold mb-4">📊 Occupancy</h2>
        <canvas ref="occCanvas" class="w-full max-h-[400px]"></canvas>
      </div>

      <div class="bg-white rounded-2xl shadow-md p-6 flex flex-col items-center">
        <h2 class="text-xl font-semibold mb-4">💰 Revenue</h2>
        <canvas ref="revCanvas" class="w-full max-h-[400px]"></canvas>
      </div>
    </div>

    <!-- Vehicle types -->
    <div class="bg-white rounded-2xl shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4 text-center">🚗 Types Vehicles</h2>
      <canvas ref="typeCanvas" class="w-full max-h-[400px]"></canvas>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-2xl shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4 text-center">📋 Active Vehicles</h2>
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-blue-500 text-white">
            <th class="py-2 px-4 text-left">Type</th>
            <th class="py-2 px-4 text-left">Registration</th>
            <th class="py-2 px-4 text-left">Entry Time</th>
            <th class="py-2 px-4 text-left">Barcode</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in vehicles" :key="v.barcode" class="border-b last:border-0">
            <td class="py-2 px-4">{{ v.type }}</td>
            <td class="py-2 px-4">{{ v.registration }}</td>
            <td class="py-2 px-4">{{ v.entry_time }}</td>
            <td class="py-2 px-4">{{ v.barcode }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

// 🎯 API base
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";


// 📦 Reactive state
const vehicles = ref([])
const charts = ref({ occ: null, rev: null, type: null })
const statusMessage = ref('')
const statusClass = ref('')

// 🎨 Canvas refs
const occCanvas = ref(null)
const revCanvas = ref(null)
const typeCanvas = ref(null)

// 🌐 Fetch helper
// async function fetchJSON(path) {
//   const res = await fetch(API_BASE + '/api' + path)
//   return res.ok ? res.json() : {}
// }

async function fetchJSON(path) {
  try {
    const res = await fetch(API_BASE + '/api' + path)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return await res.json()
  } catch (err) {
    console.error(`❌ Failed to fetch ${path}:`, err)
    return {}
  }
}


// 📊 Load dashboard
async function loadDashboard() {
  const free = await fetchJSON('/spaces/free')
  const occ = await fetchJSON('/occupancy')
  const occupied = occ.capacity - free.free_spaces

  const list = await fetchJSON('/vehicles/active')
  vehicles.value = list

  const rev = await fetchJSON('/revenue/today')

  await nextTick()
  renderOccupancy(occupied, free.free_spaces, occ.capacity)
  renderType(list)
  renderRevenue(rev.total_revenue || 0)
}

// 🔁 Simulate entry/exit
async function triggerSimulation() {
  statusMessage.value = ''
  try {
    const res = await fetch(API_BASE + '/api/simulate', { method: 'POST' })
    const data = await res.json()

    if (data.error) {
      statusMessage.value = '❌ ' + data.error
      statusClass.value = 'text-red-600'
    } else {
      statusMessage.value = '✅ Simulation started successfully!'
      statusClass.value = 'text-green-600'
      loadDashboard()
    }
  } catch (err) {
    statusMessage.value = '❌ Server communication error.'
    statusClass.value = 'text-red-600'
  }
}

// 📈 Chart rendering
function renderOccupancy(occupied, free, capacity) {
  if (occupied >= capacity) {
    statusMessage.value = '⚠️ Parking is full. No free spots.'
    statusClass.value = 'text-red-600'
  }
  if (charts.value.occ) charts.value.occ.destroy()
  charts.value.occ = new Chart(occCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['Occupied', 'Free'],
      datasets: [{ data: [occupied, free], backgroundColor: ['#f44336', '#4caf50'] }]
    }
  })
}

function renderRevenue(amount) {
  if (charts.value.rev) charts.value.rev.destroy()
  charts.value.rev = new Chart(revCanvas.value, {
    type: 'bar',
    data: {
      labels: ['Today'],
      datasets: [{ label: 'RSD', data: [amount], backgroundColor: '#ff9800' }]
    },
    options: { scales: { y: { beginAtZero: true } } }
  })
}

function renderType(list) {
  if (charts.value.type) charts.value.type.destroy()
  const counts = list.reduce((acc, v) => {
    acc[v.type] = (acc[v.type] || 0) + 1
    return acc
  }, {})
  charts.value.type = new Chart(typeCanvas.value, {
    type: 'bar',
    data: {
      labels: Object.keys(counts),
      datasets: [{ label: 'Count', data: Object.values(counts), backgroundColor: '#2196f3' }]
    },
    options: { scales: { y: { beginAtZero: true } } }
  })
}

onMounted(loadDashboard)
</script>


<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>

<template>
  <div class="dashboard-container">
    <div class="header">
      <h1>Doctor Dashboard</h1>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <div v-if="loading" class="loading">Loading dashboard data...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>

    <div v-else class="dashboard-stats">
      <div class="stat-card">
        <h3>Today's Appointments</h3>
        <p class="stat-number">{{ stats.todayAppointments }}</p>
      </div>

      <div class="stat-card">
        <h3>Pending Treatments</h3>
        <p class="stat-number">{{ stats.pendingTreatments }}</p>
      </div>

      <div class="stat-card">
        <h3>Completed Cases</h3>
        <p class="stat-number">{{ stats.completedCases }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { clearToken, getUserRole } from '../utils/tokenManager';

export default {
  name: 'DoctorDashboard',
  data() {
    return {
      stats: {
        todayAppointments: 5,
        pendingTreatments: 3,
        completedCases: 12,
      },
      loading: false,
      error: null,
    };
  },
  mounted() {
    if (getUserRole() !== 'Doctor') {
      this.error = 'Unauthorized: Doctor access required';
      this.$router.push('/login');
    }
  },
  methods: {
    logout() {
      clearToken();
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #007bff;
}

h1 {
  color: #333;
  margin: 0;
}

.logout-btn {
  padding: 10px 20px;
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #b71c1c;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-card h3 {
  color: #666;
  margin-top: 0;
  font-size: 14px;
  text-transform: uppercase;
}

.stat-number {
  color: #007bff;
  font-size: 36px;
  font-weight: bold;
  margin: 10px 0 0 0;
}
</style>
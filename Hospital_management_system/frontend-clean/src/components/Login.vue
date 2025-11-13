<template>
  <div>
    
    <nav class="navbar navbar-expand-lg bg-white shadow-sm px-5 py-3">
  <div class="container-fluid">
    <a class="navbar-brand text-success fw-bold fs-4" href="#">TryggHelse</a>
    <ul class="navbar-nav ms-auto d-flex align-items-center gap-4">
      <li class="nav-item"><a class="nav-link text-dark fw-medium" href="#">Products</a></li>
      <li class="nav-item"><a class="nav-link text-dark fw-medium" href="#">Resources</a></li>
      <li class="nav-item"><a class="nav-link text-dark fw-medium" href="#">Company</a></li>
      <li class="nav-item"><a class="nav-link text-dark fw-medium" href="#">Login</a></li>
      <li class="nav-item">
        <a class="btn btn-success px-4 py-2 fw-semibold rounded-pill" href="#">Book a Demo</a>
      </li>
    </ul>
  </div>
</nav>
    <!-- Login Page -->
    <div class="login-page">
      <div class="login-card shadow-lg">
        <div class="card-row">
          <!-- Left Panel -->
          <div class="left-panel">
            <div class="left-inner">
              <h2>Patient Login</h2>
              <ul class="features-list">
                <li>Anytime, Anywhere, Any Device</li>
                <li>Go Paperless</li>
                <li>Secure Backup</li>
                <li>Multi Location Support</li>
                <li>Quick Insight On Key Performance</li>
              </ul>
            </div>
          </div>

          <!-- Right Panel -->
          <div class="right-panel">
            <div class="right-inner">
              <h3 class="title">Sign In</h3>
              <form @submit.prevent="handleLogin">
                <div class="form-group">
                  <label class="form-label">Email or User Id</label>
                  <input type="text" v-model="email" class="form-control" placeholder="Email or User Id" required />
                </div>

                <div class="form-group">
                  <label class="form-label">Password</label>
                  <div class="password-row">
                    <input :type="showPassword ? 'text' : 'password'" v-model="password" class="form-control" placeholder="Password" required />
                    <button type="button" class="show-btn" @click="showPassword = !showPassword">{{ showPassword ? 'Hide' : 'Show' }}</button>
                  </div>
                </div>

                <div class="d-flex justify-content-end mb-3">
                  <a href="#" class="forgot">Forgot Password?</a>
                </div>

                <button type="submit" class="btn login-btn w-100" :disabled="loading">{{ loading ? 'Logging in...' : 'Login' }}</button>

                <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
                <div v-if="success" class="alert alert-success mt-3">Login successful! Redirecting...</div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { saveToken } from '../utils/tokenManager';

export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      showPassword: false,
      loading: false,
      error: null,
      success: false
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;
      this.success = false;

      try {
        const response = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.email, password: this.password })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.msg || 'Login failed');
        }

        const data = await response.json();
        saveToken(data);
        this.success = true;

        setTimeout(() => {
          if (data.role === 'Admin') {
            this.$router.push('/admin/dashboard');
          } else if (data.role === 'Doctor') {
            this.$router.push('/doctor/dashboard');
          } else if (data.role === 'Patient') {
            this.$router.push('/patient/dashboard');
          }
        }, 1000);
      } catch (err) {
        this.error = err.message || 'An error occurred during login';
        console.error('Login error:', err);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>

.navbar {
  border-bottom: 1px solid #eee;
}

.navbar-nav .nav-link {
  font-size: 15px;
  transition: color 0.2s ease;
}

.navbar-nav .nav-link:hover {
  color: #0aa64a !important;
}

.btn-success {
  background-color: #0aa64a;
  border: none;
  font-size: 14px;
}

.btn-success:hover {
  background-color: #089e45;
}


.navbar-brand {
  font-size: 24px;
}

.navbar {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 28px;
}

.navbar-nav {
  display: flex;
  gap: 22px;
  margin: 0;
  padding: 0;
  list-style: none;
  align-items: center;
}

.navbar-nav .nav-item { list-style: none; }

.btn-book {
  background: #0aa64a;
  color: #fff;
  border-radius: 20px;
  padding: 8px 14px;
  font-weight: 600;
  text-decoration: none;
}

.nav-link {
  font-weight: 500;
  color: #333 !important;
  margin-right: 15px;
}

.nav-link:hover {
  color: #0aa64a !important;
}

.btn-success {
  font-weight: 600;
  border-radius: 6px;
}

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f2f5;
  padding: 3rem 1rem;
}

.login-card {
  width: 100%;
  max-width: 1000px;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 18px 50px rgba(0,0,0,0.25);
}

.card-row {
  display: flex;
  flex-direction: row;
  min-height: 420px;
}

.left-panel {
  flex: 0 0 45%;
  background-color: #0aa64a;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.left-inner {
  padding: 40px;
}

.left-inner h2 {
  font-size: 30px;
  margin-bottom: 18px;
  font-weight: 700;
}

.features-list {
  list-style: none;
  padding: 0;
}

.features-list li {
  margin-bottom: 14px;
  font-size: 15px;
  display: flex;
  align-items: center;
}

.features-list li::before {
  content: "\2713";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  margin-right: 12px;
  border-radius: 50%;
  background: rgba(255,255,255,0.18);
  color: #fff;
  font-weight: 800;
}

.right-panel {
  flex: 1 1 55%;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.right-inner {
  width: 100%;
  max-width: 420px;
  padding: 36px;
}

.title {
  text-align: center;
  font-size: 34px;
  margin-bottom: 20px;
  color: #222;
}

.form-label {
  font-weight: 600;
  color: #666;
}

.form-control {
  width: 100%;
  padding: 12px 14px;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
  margin-top: 8px;
  background: #f5f6f7;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.03);
}

.password-row {
  position: relative;
}

.password-row .show-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: #007bff;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
}

.forgot {
  color: #f58220;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
}

.login-btn {
  background: linear-gradient(180deg,#ff8a00,#f58220);
  border: none;
  color: white;
  padding: 14px 18px;
  border-radius: 26px;
  font-weight: 800;
  font-size: 16px;
  box-shadow: 0 8px 26px rgba(245,130,32,0.28);
}

.alert {
  margin-top: 14px;
}

@media (max-width: 767px) {
  .card-row { flex-direction: column; }
  .left-panel { flex: none; padding: 20px; }
  .left-inner { padding: 20px; }
  .right-inner { padding: 20px; }
  .card-row { min-height: auto; }
}
</style>


<template>
  <div class="register-container">
    <div class="register-card">
      <div class="card-header">
        <svg class="logo" width="40" height="40" viewBox="0 0 32 32" fill="none">
          <circle cx="16" cy="16" r="16" fill="#0194F3"/>
          <path d="M16 8L22 14L16 20L10 14L16 8Z" fill="white"/>
        </svg>
        <h1>Create Account</h1>
        <p>Join Traveloka to book flights and manage your journeys</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-grid">
          <!-- Username -->
          <div class="form-group">
            <label for="username">Username</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              placeholder="e.g. travel_lover" 
              required 
              class="form-input"
            />
          </div>

          <!-- Email -->
          <div class="form-group">
            <label for="email">Email Address</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="e.g. explorer@travel.com" 
              required 
              class="form-input"
            />
          </div>

          <!-- Password -->
          <div class="form-group">
            <label for="password">Password</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              placeholder="Create a strong password" 
              required 
              class="form-input"
            />
          </div>

          <!-- Phone Number -->
          <div class="form-group">
            <label for="phone">Phone Number (Số điện thoại)</label>
            <input 
              type="tel" 
              id="phone" 
              v-model="phone" 
              placeholder="e.g. 0123456789" 
              required 
              class="form-input"
            />
          </div>

          <!-- Region/Province -->
          <div class="form-group">
            <label for="region">Region/Province (Vùng miền)</label>
            <input 
              type="text" 
              id="region" 
              v-model="region" 
              placeholder="e.g. Ho Chi Minh City" 
              required 
              class="form-input"
            />
          </div>

          <!-- National ID / CCCD -->
          <div class="form-group">
            <label for="nationalId">National ID / CCCD (Căn cước công dân)</label>
            <input 
              type="text" 
              id="nationalId" 
              v-model="nationalId" 
              placeholder="e.g. 079090123456" 
              required 
              class="form-input"
            />
          </div>

          <!-- Avatar Image Upload -->
          <div class="form-group full-width avatar-form-group">
            <label for="avatar">Avatar Image</label>
            <div class="avatar-upload-wrapper">
              <input 
                type="file" 
                id="avatar" 
                ref="fileInput"
                accept="image/*"
                @change="handleAvatarUpload" 
                style="display: none;"
              />
              <div class="avatar-upload-zone" @click="fileInput.click()">
                <img v-if="avatarUrl" :src="avatarUrl" class="preview-img" alt="Avatar Preview" />
                <div v-else class="upload-placeholder">
                  <span class="upload-icon">📷</span>
                  <span class="upload-text">Upload your profile pic</span>
                </div>
              </div>
            </div>
          </div>

          <button type="submit" class="submit-btn full-width" :disabled="loading">
            {{ loading ? 'Creating Account...' : 'Register' }}
          </button>
        </div>
      </form>

      <div class="card-footer">
        <p>Already have an account? <router-link to="/signin" class="signin-link">Sign In here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { API_URL } from '@/utils/apiClient';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const phone = ref('');
const region = ref('');
const nationalId = ref('');
const avatarUrl = ref('');
const fileInput = ref(null);
const loading = ref(false);

const handleAvatarUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      avatarUrl.value = reader.result;
    };
    reader.readAsDataURL(file);
  }
};

const handleRegister = async () => {
  loading.value = true;
  try {
    const response = await fetch(`${API_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        username: username.value,
        phone: phone.value,
        region: region.value,
        national_id: nationalId.value,
        avatar_url: avatarUrl.value
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const message = errorData.detail || 'Registration failed. Please check the information and try again.';
      throw new Error(message);
    }

    alert("Registration successful! A verification link has been sent to your email. Please confirm your email before signing in.");
    router.push('/signin');
  } catch (error) {
    console.error('Registration error:', error);
    alert(error.message || 'An unexpected network error occurred.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped lang="scss">
@import '@/assets/scss/variables.scss';

.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
  padding: $spacing-xl $spacing-md;
  background-color: $sky-blue-bg;
}

.register-card {
  background: $white;
  padding: $spacing-2xl $spacing-xl;
  border-radius: $border-radius-lg;
  box-shadow: $shadow-xl;
  width: 100%;
  max-width: 650px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.4s ease-out;
}

.card-header {
  text-align: center;
  margin-bottom: $spacing-xl;

  .logo {
    margin-bottom: $spacing-sm;
  }

  h1 {
    font-size: $font-size-2xl;
    color: $dark-text;
    margin-bottom: $spacing-xs;
    font-weight: $font-weight-bold;
  }

  p {
    color: $gray-text;
    font-size: $font-size-sm;
  }
}

.register-form {
  display: flex;
  flex-direction: column;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem 1.5rem;
}

.full-width {
  grid-column: span 2;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;

  label {
    font-size: $font-size-sm;
    font-weight: $font-weight-semibold;
    color: $dark-text;
  }
}

.form-input {
  width: 100%;
  padding: $spacing-md;
  border: 1px solid $light-gray;
  border-radius: $border-radius-md;
  font-size: $font-size-base;
  outline: none;
  transition: all $transition-fast;

  &:focus {
    border-color: $traveloka-blue;
    box-shadow: 0 0 0 3px rgba(1, 148, 243, 0.15);
  }
}

.avatar-form-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
}

.avatar-upload-wrapper {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  width: 100%;
}

.avatar-upload-zone {
  width: 180px;
  height: 180px;
  margin: 0 auto;
  border: 2px dashed $light-gray;
  background: #f8fafc;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;

  &:hover {
    border-color: $traveloka-blue;
    background: rgba(1, 148, 243, 0.05);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(1, 148, 243, 0.1);
  }
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-xs;
  color: $gray-text;
  font-size: $font-size-xs;
  text-align: center;
  padding: $spacing-sm;

  .upload-icon {
    font-size: 3rem;
  }
}

.submit-btn {
  background-color: $traveloka-orange;
  color: $white;
  padding: $spacing-md;
  font-size: $font-size-base;
  font-weight: $font-weight-bold;
  border: none;
  border-radius: $border-radius-md;
  cursor: pointer;
  transition: all $transition-base;
  margin-top: $spacing-sm;

  &:hover:not(:disabled) {
    background-color: darken($traveloka-orange, 8%);
    transform: translateY(-1px);
    box-shadow: $shadow-md;
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  &:active {
    transform: translateY(0);
  }
}

.card-footer {
  text-align: center;
  margin-top: $spacing-xl;
  font-size: $font-size-sm;
  color: $gray-text;

  .signin-link {
    color: $traveloka-blue;
    text-decoration: none;
    font-weight: $font-weight-semibold;

    &:hover {
      text-decoration: underline;
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 576px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: $spacing-md 0;
  }

  .full-width {
    grid-column: span 1;
  }
}
</style>

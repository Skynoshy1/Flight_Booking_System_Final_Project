<template>
  <div class="signin-container">
    <div class="signin-card">
      <div class="card-header">
        <svg class="logo" width="40" height="40" viewBox="0 0 32 32" fill="none">
          <circle cx="16" cy="16" r="16" fill="#0194F3"/>
          <path d="M16 8L22 14L16 20L10 14L16 8Z" fill="white"/>
        </svg>
        <h1>Sign In to Traveloka</h1>
        <p>Book flights, view history, and manage your trips</p>
      </div>

      <form @submit.prevent="handleSignIn" class="signin-form">
        <div class="form-group">
          <label for="identifier">Email or Mobile Number</label>
          <input 
            type="text" 
            id="identifier" 
            v-model="identifier" 
            placeholder="e.g. explorer@travel.com or 0123456789" 
            required 
            class="form-input"
            @keyup.enter="handleSignIn"
          />
        </div>

        <div class="form-group">
          <div class="label-row">
            <label for="password">Password</label>
            <a href="#" class="forgot-link" @click.prevent="showPlaceholderAlert('Forgot Password')">Forgot Password?</a>
          </div>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Enter your password" 
            required 
            class="form-input"
            @keyup.enter="handleSignIn"
          />
        </div>

        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
        <button type="submit" class="submit-btn">
          Sign In
        </button>
      </form>

      <div class="card-footer">
        <p>Don't have an account? <router-link to="/register" class="register-link">Register here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const identifier = ref('');
const password = ref('');
const errorMessage = ref('');

const handleSignIn = async () => {
  errorMessage.value = '';
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/auth/signin', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: identifier.value,
        password: password.value
      })
    });

    if (!response.ok) {
      errorMessage.value = "You must register first";
      return;
    }

    const result = await response.json();
    localStorage.setItem('user', JSON.stringify(result));
    
    // Dispatch custom storage event for Navbar to update immediately
    window.dispatchEvent(new Event('storage'));
    
    if (result.role === 'admin') {
      router.push('/admin');
    } else {
      router.push('/');
    }
  } catch (error) {
    console.error('Sign in error:', error);
    errorMessage.value = "You must register first";
  }
};
</script>

<style scoped lang="scss">
@import '@/assets/scss/variables.scss';

.signin-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
  padding: $spacing-xl $spacing-md;
  background-color: $sky-blue-bg;
}

.signin-card {
  background: $white;
  padding: $spacing-2xl $spacing-xl;
  border-radius: $border-radius-lg;
  box-shadow: $shadow-xl;
  width: 100%;
  max-width: 440px;
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

.signin-form {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
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

  .label-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .forgot-link {
    font-size: $font-size-xs;
    color: $traveloka-blue;
    text-decoration: none;
    font-weight: $font-weight-medium;

    &:hover {
      text-decoration: underline;
    }
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

  &:hover {
    background-color: darken($traveloka-orange, 8%);
    transform: translateY(-1px);
    box-shadow: $shadow-md;
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

  .register-link {
    color: $traveloka-blue;
    text-decoration: none;
    font-weight: $font-weight-semibold;

    &:hover {
      text-decoration: underline;
    }
  }
}

.error-text {
  color: #ef4444;
  font-size: 0.875rem;
  font-weight: 600;
  text-align: left;
  margin-bottom: $spacing-xs;
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
</style>

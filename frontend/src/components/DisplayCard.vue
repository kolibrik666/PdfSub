<template>
  <div class="container">
    <form @submit.prevent="handleSubmit">
      <div class="imgcontainer">
        <img
            src="https://cdn-icons-png.flaticon.com/512/6596/6596121.png"
            alt="Avatar"
            class="avatar"
        />
      </div>

      <div v-if="isSignUp">
        <div class="input-group">
          <label for="name"><b>Name</b></label>
          <input type="text" v-model="form.name" placeholder="Enter Name" required />
        </div>
        <div class="input-group">
          <label for="surname"><b>Surname</b></label>
          <input type="text" v-model="form.surname" placeholder="Enter Surname" required />
        </div>
      </div>

      <div class="input-group">
        <label for="email"><b>Email</b></label>
        <input type="email" v-model="form.email" placeholder="Enter Email" required />
      </div>

      <div class="input-group">
        <label for="password"><b>Password</b></label>
        <input
            type="password"
            v-model="form.password"
            placeholder="Enter Password"
            required
        />
      </div>

      <div v-if="isSignUp">
        <div class="input-group">
          <label for="password2"><b>Repeat Password</b></label>
          <input
              type="password"
              v-model="form.password2"
              placeholder="Repeat Password"
              required
          />
        </div>
      </div>

      <button type="submit">{{ buttonText }}</button>

      <button
          type="button"
          @click="redirectToOtherForm"
          v-if="isSignUp"
          class="cancelbtn"
      >
        Already have an account? Login
      </button>
      <button
          type="button"
          @click="redirectToOtherForm"
          v-if="!isSignUp"
          class="cancelbtn"
      >
        Don't have an account? Sign Up
      </button>
    </form>
  </div>
</template>
<script>
import api from '../services/api';
import { EventBus } from '../services/eventBus';

export default {
  props: {
    isSignUp: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      form: {
        name: "",
        surname: "",
        username: "",
        email: "",
        password: "",
        password2: "",
      },
    };
  },
  computed: {
    buttonText() {
      return this.isSignUp ? "Register" : "Login";
    },
  },
  methods: {
    handleSubmit() {
      if (this.isSignUp) {
        if (this.form.password !== this.form.password2) {
          alert("Passwords do not match");
          return;
        }
        api.register({
          email: this.form.email,
          password: this.form.password,
          name: this.form.name,
          surname: this.form.surname
        })
            .then(() => {
              console.log("Registered with", this.form);
              alert("Registration successful");
              this.$router.push('/login');
            })
            .catch(error => {
              console.error("Registration failed", error);
              alert("Registration failed");
            });
      } else {
        api.login({ email: this.form.email, password: this.form.password })
            .then(response => {
              console.log("Logging in with", this.form);
              localStorage.setItem('userToken', response.data.token);
              localStorage.setItem('isAdmin', response.data.isAdmin);
              localStorage.setItem('isStudent', response.data.isStudent);
              localStorage.setItem('isParticipant', response.data.isParticipant);
              localStorage.setItem('isReviewer', response.data.isReviewer);
              EventBus.emit('user-logged-in');
              if (response.data.isAdmin) {
                this.$router.push('/admin');
              } else {
                this.$router.push('/');
              }
            })
            .catch(error => {
              console.error("Login failed", error);
              alert("Invalid credentials");
            });
      }
    },
    redirectToOtherForm() {
      if (this.isSignUp) {
        this.$router.push("/login");
      } else {
        this.$router.push("/sign-up");
      }
    },
  },
};
</script>
  
  <style scoped>
  * {
    font-family: 'Merriweather', serif;
  }
  
  body {
    background-color: #734ae8;
    background-image: linear-gradient(315deg, #734ae8 0%, #89d4cf 74%);
    background-size: 100% 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    overflow-x: hidden;
  }
  
  .container {
    background-color: #ffffff;
    padding: 20px;
    max-width: 400px;
    margin: 0 auto;
    margin-top: 50px;
    border-radius: 5px;
    box-shadow: 0px 0px 5px 0px rgba(0, 0, 0, 0.2);
  }
  
  input[type="text"],
  input[type="password"],
  input[type="email"] {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  button {
    background-color: black;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
  }
  
  button:hover {
    background-color: rgb(4, 169, 169);
  }
  
  .cancelbtn {
    background-color: #f44336;
  }
  
  .imgcontainer {
    text-align: center;
    margin: 24px 0 12px 0;
    position: relative;
  }
  
  img.avatar {
    width: 100%;
    max-width: 150px;
    border-radius: 50%;
  }
  
  .container form {
    padding: 16px;
  }
  
  @media screen and (max-width: 600px) {
    .container {
      width: 90%;
    }
  }
  
  .alert {
    color: white;
    padding: 10px;
    width: 100%;
    text-align: center;
  }
  </style>
  
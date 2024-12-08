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
            <label for="username"><b>Username</b></label>
            <input type="text" v-model="form.username" placeholder="Enter Username" required />
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
          // handle sign up logic here
          console.log("Registering with", this.form);
        } else {
          // handle login logic here
          console.log("Logging in with", this.form);
        }
      },
      redirectToOtherForm() {
        // Here, you would handle the redirection to either login or signup based on the current view
        if (this.isSignUp) {
          this.$router.push("/login");
        } else {
          this.$router.push("/sign_up");
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
  
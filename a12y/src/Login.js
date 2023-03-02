import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import bcrypt from 'bcryptjs';

const API_BASE_URL = 'http://127.0.0.1:5000';

function Login() {

    const [userData, setUserData] = useState({
      username: '',
      password: '',
    });
  
    const handleChange = (event) => {
      const { name, value } = event.target;
      setUserData((prevUserData) => ({
        ...prevUserData,
        [name]: value,
      }));
    };
  
    const handleSubmit = (event) => {
      event.preventDefault();
  
      axios
        .get(`${API_BASE_URL}/users/${userData.username}`)
        .then((response) => {
          const user = response.data;
  
          bcrypt.compare(userData.password, user.password, (error, result) => {
            if (error) {
              console.log(error);
            } else if (result) {
              console.log('Login successful!');
              setUserData((prevUserData) => ({
                  ...prevUserData,
                  isAuthenticated: true,
              }));

              
            } else {
              console.log('Login failed');
            }
          });
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    };

    return (
        <form onSubmit={handleSubmit}>
        <label>
            Username:
            <input
            type="text"
            name="username"
            value={userData.username}
            onChange={handleChange}
            required
            />
        </label>
        <br />
        <label>
            Password:
            <input
            type="password"
            name="password"
            value={userData.password}
            onChange={handleChange}
            required
            />
        </label>
        <br />
        <button type="submit">Log in</button>
        </form>
  );
}

export default Login;

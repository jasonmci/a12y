import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import bcrypt from 'bcryptjs';

const API_BASE_URL = 'http://127.0.0.1:5000';

export default function Signup() {
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    bio: '',
    avatar_url: '',
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

    const salt = bcrypt.genSaltSync(10);
    const password = bcrypt.hashSync(userData.password, salt);

    const safeData = {
      username: userData.username,
      email: userData.email,
      password: password,
      first_name: userData.first_name,
      last_name: userData.last_name,
      bio: userData.bio,
      avatar_url: userData.avatar_url
    }

    axios
      .post(`${API_BASE_URL}/users`, safeData)
      .then((response) => {
        console.log(response.data);
        setUserData({
            username: '',
            email: '',
            password: '',
            first_name: '',
            last_name: '',
            bio: '',
            avatar_url: '',
          });
        // Handle successful response
      })
      .catch((error) => {
        console.log(error.response.data);
        // Handle error response
      });
  };

  return (
    <form className="signup-form" onSubmit={handleSubmit}>
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
          First name:
          <input
            type="text"
            name="first_name"
            value={userData.first_name}
            onChange={handleChange}
            required
        />
      </label>
      <br />
      <label>
          Last name:
          <input
            type="text"
            name="last_name"
            value={userData.last_name}
            onChange={handleChange}
            required
        />
      </label>
      <br />
      <label>
        Email:
        <input
          type="email"
          name="email"
          value={userData.email}
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
      <label>
        Personal Bio:
        <input
          type="text"
          name="bio"
          value={userData.bio}
          onChange={handleChange}
        />
      </label>
      <br />
      <label>
        Avatar Url:
        <input
          type="text"
          name="avatar_url"
          value={userData.avatar_url}
          onChange={handleChange}
        />
      </label>
      <br /> 
      
      <button type="submit">Sign up</button>
    </form>
  );
}

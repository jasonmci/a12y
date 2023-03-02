CREATE DATABASE IF NOT EXISTS a12y;
-- GRANT ALL PRIVILEGES ON mydatabase.* TO 'myuser'@'%' IDENTIFIED BY 'mypassword';
USE a12y;

CREATE TABLE users (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  bio TEXT,
  avatar_url VARCHAR(255),
  total_karma_points INT(11) NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_profile_fields (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  data_type VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_profiles (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  field_id INT(11) NOT NULL,
  value VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (field_id) REFERENCES user_profile_fields(id)
);

CREATE TABLE activities (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  start_date DATETIME NOT NULL,
  due_date DATETIME NOT NULL,
  owner_id VARCHAR(36) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status ENUM('incomplete', 'complete', 'completed_late', 'cancelled') DEFAULT 'incomplete' NOT NULL,
  completed_at DATETIME,
  reason_for_incompletion TEXT,
  size ENUM('small', 'medium', 'large') DEFAULT 'medium' NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE weekly_activities (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  activity_id VARCHAR(36) NOT NULL,
  frequency INT NOT NULL,
  monday TINYINT(1) NOT NULL DEFAULT 0,
  tuesday TINYINT(1) NOT NULL DEFAULT 0,
  wednesday TINYINT(1) NOT NULL DEFAULT 0,
  thursday TINYINT(1) NOT NULL DEFAULT 0,
  friday TINYINT(1) NOT NULL DEFAULT 0,
  saturday TINYINT(1) NOT NULL DEFAULT 0,
  sunday TINYINT(1) NOT NULL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (activity_id) REFERENCES activities(id)
);

CREATE TABLE activity_co_owners (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  activity_id VARCHAR(36) NOT NULL,
  user_id VARCHAR(36) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (activity_id) REFERENCES activities(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE activity_co_owner_map (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  activity_id VARCHAR(36) NOT NULL,
  co_owner_id VARCHAR(36) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (activity_id) REFERENCES activities(id),
  FOREIGN KEY (co_owner_id) REFERENCES users(id)
);

CREATE TABLE activity_co_owners_conversations (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  activity_id VARCHAR(36) NOT NULL,
  user_id VARCHAR(36) NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (activity_id) REFERENCES activities(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE user_followers (
  user_id VARCHAR(36) NOT NULL,
  follower_id VARCHAR(36) NOT NULL,
  PRIMARY KEY (user_id, follower_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (follower_id) REFERENCES users(id)
);

CREATE TABLE user_following (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  following_id VARCHAR(36) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (following_id) REFERENCES users(id)
);

CREATE TABLE user_groups (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT
);

CREATE TABLE group_members (
  group_id VARCHAR(36) NOT NULL,
  user_id VARCHAR(36) NOT NULL,
  PRIMARY KEY (group_id, user_id),
  FOREIGN KEY (group_id) REFERENCES user_groups(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE group_activities (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  due_date DATETIME NOT NULL,
  group_id VARCHAR(36) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status ENUM('incomplete', 'complete', 'completed_late', 'cancelled') DEFAULT 'incomplete' NOT NULL,
  completed_at DATETIME,
  reason_for_incompletion TEXT,
  FOREIGN KEY (group_id) REFERENCES user_groups(id)
);

CREATE TABLE group_activity_signups (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  group_activity_id VARCHAR(36) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (group_activity_id) REFERENCES group_activities(id)
);

CREATE TABLE group_activity_conversations (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  group_activity_id VARCHAR(36) NOT NULL,
  user_id VARCHAR(36) NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (group_activity_id) REFERENCES group_activities(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE karma_points (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  points INT(11) NOT NULL DEFAULT 0,
  reason VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE messages (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  message TEXT NOT NULL,
  activity_id VARCHAR(36),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (activity_id) REFERENCES activities(id)
);
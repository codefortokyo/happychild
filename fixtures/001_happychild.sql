CREATE TABLE `ages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_is_active` (`is_active`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `home_url` varchar(1000),
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_is_active` (`is_active`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `nursery_free_nums` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `age_id` int(11) UNSIGNED NOT NULL,
  `nursery_id` int(11) UNSIGNED NOT NULL,
  `free_num` int(11) UNSIGNED,
  `is_active` tinyint(1) DEFAULT '1',
  `modified_date` date,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_nursery_id_and_is_active` (`nursery_id`, `is_active`),
  KEY `idx_age_id` (`age_id`),
  KEY `idx_modifed_date` (`modified_date`),
  UNIQUE KEY `age_id_and_nursery_id_and_modified_date` (`age_id`, `nursery_id`, `modified_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `licenses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_is_active` (`is_active`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `nurseries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ward_id` int(11) UNSIGNED NOT NULL,
  `license_id` int(11) UNSIGNED NOT NULL,
  `school_type_id` int(11) UNSIGNED NOT NULL,
  `uuid` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `postcode` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `station_info` varchar(255),
  `url` varchar(1000),
  `phone_number` varchar(255),
  `fax_number` varchar(255),
  `thumbnail_url` varchar(1000),
  `latitude` decimal(10, 8) NOT NULL,
  `longitude` decimal(11, 8) NOT NULL,
  `open_time_weekday` varchar(255),
  `open_time_saturday` varchar(255),
  `close_day` varchar(1000),
  `accept_age` varchar(255),
  `stable_food_info` varchar(1000),
  `stable_food` tinyint(1) DEFAULT '0',
  `temporary_childcare` tinyint(1) DEFAULT '0',
  `overnight_childcare` tinyint(1) DEFAULT '0',
  `allday_childcare` tinyint(1) DEFAULT '0',
  `evaluation` tinyint(1) DEFAULT '0',
  `eco` tinyint(1) DEFAULT '0',
  `evaluation_url` varchar(255) DEFAULT '0',
  `organizer` varchar(255) DEFAULT '0',
  `event` varchar(1000),
  `service` varchar(1000),
  `policy` varchar(1000),
  `promise` varchar(1000),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_ward_id` (`ward_id`),
  KEY `idx_school_type_id` (`school_type_id`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_stable_food` (`stable_food`),
  KEY `idx_temporary_childcare` (`temporary_childcare`),
  KEY `idx_overnight_childcare` (`overnight_childcare`),
  KEY `idx_allday_childcare` (`allday_childcare`),
  KEY `idx_evaluation` (`evaluation`),
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `school_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_is_active` (`is_active`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `nursery_scores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nursery_id` int(11) UNSIGNED NOT NULL,
  `age_id` int(11) UNSIGNED NOT NULL,
  `year` varchar(10) NOT NULL,
  `score` int(11) UNSIGNED,
  `hierarchy` varchar(10),
  `note` varchar(255),
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_nursery_id_and_is_active` (`nursery_id`, `is_active`),
  KEY `idx_age_id` (`age_id`),
  KEY `idx_score` (`score`),
  UNIQUE KEY `age_id_and_nursery_id_and_year` (`age_id`, `nursery_id`, `year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `lines` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_id` int(11) UNSIGNED NOT NULL,
  `city_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_api_id` (`api_id`),
  KEY `idx_city_id` (`city_id`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `stations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_id` int(11) UNSIGNED NOT NULL,
  `line_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `latitude` decimal(10, 8) NOT NULL,
  `longitude` decimal(11, 8) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_api_id` (`api_id`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_latitude_and_longitude` (`latitude`, `longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `wards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `home_url` varchar(1000),
  `nursery_info_url` varchar(1000),
  `nursery_free_num_info_url` varchar(1000),
  `is_active` tinyint(1) DEFAULT '1',
  `latitude` decimal(10, 8) NOT NULL,
  `longitude` decimal(11, 8) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_is_active` (`is_active`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `crawled_guid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guid` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_guid` (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `user_nursery_mappings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) UNSIGNED NOT NULL,
  `nursery_id` int(11) UNSIGNED NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_id_and_is_active` (`user_id`, `is_active`),
  KEY `idx_nursery_id_and_is_active` (`nursery_id`, `is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `nursery_bookmarks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) UNSIGNED NOT NULL,
  `nursery_id` int(11) UNSIGNED NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_nursery_id` (`nursery_id`),
  UNIQUE KEY `nursery_id_and_user_id` (`nursery_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `nursery_default_tour_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nursery_id` int(11) UNSIGNED NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `capacity` int(11) UNSIGNED NOT NULL,
  `description` varchar(1000) NOT NULL,
  `note` varchar(1000) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_nursery_id` (`nursery_id`),
  UNIQUE KEY `nursery_id_and_start_time` (`nursery_id`, `start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `nursery_tours` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nursery_id` int(11) UNSIGNED NOT NULL,
  `nursery_default_tour_setting_id` int(11) UNSIGNED,
  `special_start_time` time DEFAULT NULL,
  `special_end_time` time DEFAULT NULL,
  `special_capacity` int(11) UNSIGNED DEFAULT NULL,
  `special_note` varchar(1000) DEFAULT NULL,
  `date` date NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_nursery_id_and_is_active` (`nursery_id`, `is_active`),
  KEY `idx_nursery_setting_id` (`nursery_default_tour_setting_id`),
  KEY `idx_date` (`date`),
  UNIQUE KEY `nursery_id_and_date_and_setting_id` (`nursery_id`, `date`, `nursery_default_tour_setting_id`),
  UNIQUE KEY `nursery_id_and_date_special_time` (`nursery_id`, `date`, `special_start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `nursery_reservations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nursery_tour_id` int(11) UNSIGNED NOT NULL,
  `user_id` int(11) UNSIGNED NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `status` tinyint(4) DEFAULT '0',
  `reservation_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_nursery_tour_id_and_is_active` (`nursery_tour_id`, `is_active`),
  KEY `idx_user_id_and_is_active` (`user_id`, `is_active`),
  KEY `is_active` (`is_active`),
  UNIQUE KEY `nursery_tour_id_and_user_id` (`nursery_tour_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

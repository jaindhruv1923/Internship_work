-- ==================== fee_consolidated_transport_option ====================
CREATE TABLE `fee_consolidated_transport_option` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `student_fee_id` int NOT NULL,
  `pickup_point_id` int NOT NULL,
  `route_id` int NOT NULL,
  `created_timestamp` datetime NOT NULL,
  `modified_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_fee_id_UNIQUE` (`student_fee_id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1728 DEFAULT CHARSET=latin1;


-- ==================== transport_allotment ====================
CREATE TABLE `transport_allotment` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `policy_id` int unsigned NOT NULL,
  `ukid` int unsigned NOT NULL,
  `option_id` int unsigned NOT NULL,
  `payment_mode` enum('DUES_MANAGEMENT','OFFLINE') NOT NULL,
  `due_id` int unsigned DEFAULT NULL,
  `status` enum('PROVISIONAL','CONFIRMED','CHECKEDOUT','CANCELLED') NOT NULL,
  `checkout_datetime` datetime DEFAULT NULL,
  `allotted_by_admin` int unsigned DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_transport_allotment_policy_id_idx` (`policy_id`),
  KEY `fk_transport_allotment_route_pick_up_point_idx_idx` (`option_id`),
  KEY `fk_transport_allotment_ukid_idx_idx` (`ukid`),
  KEY `fk_transport_allotment_allotted_by_admin_idx_idx` (`allotted_by_admin`),
  KEY `fk_transport_allotment_due_idx` (`due_id`),
  CONSTRAINT `fk_transport_allotment_allotted_by_admin_idx` FOREIGN KEY (`allotted_by_admin`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_allotment_due_idx` FOREIGN KEY (`due_id`) REFERENCES `dues_v2` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_allotment_policy_id_idx` FOREIGN KEY (`policy_id`) REFERENCES `transport_fee_policy` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_allotment_route_pick_up_point_idx` FOREIGN KEY (`option_id`) REFERENCES `transport_route_pickup_point` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_allotment_ukid_idx` FOREIGN KEY (`ukid`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=522 DEFAULT CHARSET=latin1;


-- ==================== transport_fee_policy ====================
CREATE TABLE `transport_fee_policy` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `code` varchar(45) NOT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `action` text,
  `activated_by` int unsigned DEFAULT NULL,
  `activated_on` datetime DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name_code` (`name`,`code`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=latin1;


-- ==================== transport_management_settings ====================
CREATE TABLE `transport_management_settings` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `college_id` int unsigned NOT NULL,
  `payment_mode` enum('DUES_MANAGEMENT','OFFLINE') NOT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_transport_management_settings_idx` (`college_id`),
  KEY `fk_transport_management_settings_college_id_idx` (`college_id`),
  CONSTRAINT `fk_transport_management_settings_college_id` FOREIGN KEY (`college_id`) REFERENCES `college` (`college_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;


-- ==================== transport_option_selection ====================
CREATE TABLE `transport_option_selection` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `allotment_id` int unsigned DEFAULT NULL,
  `student_ukid` int unsigned NOT NULL,
  `option_id` int unsigned NOT NULL,
  `selected_on` datetime NOT NULL,
  `selection_type` enum('ADMIN','SELF') NOT NULL,
  `selected_by` int unsigned NOT NULL,
  `payment_mode` enum('DUES_MANAGEMENT','OFFLINE') NOT NULL,
  `due_id` int unsigned DEFAULT NULL,
  `status` enum('PROVISIONAL','CONFIRMED','CANCELLED','CHECKEDOUT','NOT_ALLOTTED','EXPIRED') NOT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_transport_option_selection_allotment_idx` (`allotment_id`),
  KEY `fk_transport_option_selection_student_ukid_idx_idx` (`student_ukid`),
  KEY `fk_transport_option_selection_option_id_idx_idx` (`option_id`),
  KEY `fk_transport_option_selection_selected_by_idx_idx` (`selected_by`),
  KEY `fk_transport_option_selection_due_idx` (`due_id`),
  CONSTRAINT `fk_transport_option_selection_allotment_idx` FOREIGN KEY (`allotment_id`) REFERENCES `transport_allotment` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_option_selection_due_idx` FOREIGN KEY (`due_id`) REFERENCES `dues_v2` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_option_selection_option_id_idx` FOREIGN KEY (`option_id`) REFERENCES `transport_route_pickup_point` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_option_selection_selected_by_idx` FOREIGN KEY (`selected_by`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_option_selection_student_ukid_idx` FOREIGN KEY (`student_ukid`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=646 DEFAULT CHARSET=latin1;


-- ==================== transport_pickup_point ====================
CREATE TABLE `transport_pickup_point` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_pickup_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=latin1;


-- ==================== transport_route ====================
CREATE TABLE `transport_route` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `policy_id` int unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `capacity` int NOT NULL,
  `deposit` double(10,2) NOT NULL,
  `payment_mode` enum('ACADEMIC_FEE','DUES','OFFLINE') NOT NULL DEFAULT 'ACADEMIC_FEE',
  `same_pickup_point_amount` tinyint unsigned NOT NULL DEFAULT '0',
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `all_institution` tinyint unsigned NOT NULL DEFAULT '0',
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_policy_route` (`policy_id`,`name`),
  KEY `fk_tp_route_fee_policy_id_idx` (`policy_id`),
  CONSTRAINT `fk_tp_route_fee_policy_id` FOREIGN KEY (`policy_id`) REFERENCES `transport_fee_policy` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=194 DEFAULT CHARSET=latin1;


-- ==================== transport_route_category ====================
CREATE TABLE `transport_route_category` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `route_id` int unsigned NOT NULL,
  `batch_year` int unsigned DEFAULT NULL,
  `quota_id` int unsigned DEFAULT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_transport_route_category_route_id_idx` (`route_id`),
  KEY `fk_transport_route_category_quota_id_idx` (`quota_id`),
  CONSTRAINT `fk_transport_route_category_quota_id` FOREIGN KEY (`quota_id`) REFERENCES `quota` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_route_category_route_id` FOREIGN KEY (`route_id`) REFERENCES `transport_route` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=999 DEFAULT CHARSET=latin1;


-- ==================== transport_route_filter ====================
CREATE TABLE `transport_route_filter` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `route_id` int unsigned NOT NULL,
  `department_id` int unsigned DEFAULT NULL,
  `programme_id` int unsigned DEFAULT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `route_batch_prog_dept_idx` (`route_id`,`department_id`,`programme_id`),
  KEY `fk_tp_route_filters_route_id_idx` (`route_id`),
  KEY `fk_tp_route_filters_department_id_idx` (`department_id`),
  KEY `fk_tp_route_filters_programme_id_idx` (`programme_id`),
  CONSTRAINT `fk_tp_route_filters_department_id` FOREIGN KEY (`department_id`) REFERENCES `department` (`department_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_tp_route_filters_programme_id` FOREIGN KEY (`programme_id`) REFERENCES `programme` (`programme_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_tp_route_filters_route_id` FOREIGN KEY (`route_id`) REFERENCES `transport_route` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=latin1;


-- ==================== transport_route_pickup_point ====================
CREATE TABLE `transport_route_pickup_point` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `route_id` int unsigned NOT NULL,
  `pickup_point_id` int unsigned NOT NULL,
  `pickup_time` time NOT NULL,
  `amount` double(10,2) NOT NULL,
  `distance` double(10,1) NOT NULL,
  `sequence` int unsigned NOT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `route_pickup_point_sequence_unique_idx` (`route_id`,`pickup_point_id`,`sequence`),
  KEY `fk_tp_pickup_point_route_idx` (`route_id`),
  KEY `fk_tp_pickup_point_name_id_idx` (`pickup_point_id`),
  CONSTRAINT `fk_tp_pickup_point_name_id` FOREIGN KEY (`pickup_point_id`) REFERENCES `transport_pickup_point` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_tp_pickup_point_route` FOREIGN KEY (`route_id`) REFERENCES `transport_route` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=338 DEFAULT CHARSET=latin1;


-- ==================== transport_route_registration ====================
CREATE TABLE `transport_route_registration` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `policy_id` int unsigned NOT NULL,
  `ukid` int unsigned NOT NULL,
  `route_pickup_point_id` int unsigned NOT NULL,
  `amount_paid` double(10,2) NOT NULL,
  `amount_due` double(10,2) NOT NULL,
  `status` enum('provisional','confirmed','cancelled') NOT NULL,
  `payment_mode` enum('ACADEMIC_FEE','DUES','OFFLINE') DEFAULT NULL,
  `payment_id` int unsigned DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_ukid_route` (`ukid`,`route_pickup_point_id`),
  KEY `tp_route_registration_pickup_point_idx` (`route_pickup_point_id`),
  KEY `tp_route_registration_pickup_ukid_idx` (`ukid`),
  KEY `fk_transport_route_registration_policy_id_idx` (`policy_id`),
  CONSTRAINT `fk_tp_pickup_point_route_id` FOREIGN KEY (`route_pickup_point_id`) REFERENCES `transport_route_pickup_point` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_tp_pickup_point_route_ukid` FOREIGN KEY (`ukid`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transport_route_registration_policy_id` FOREIGN KEY (`policy_id`) REFERENCES `transport_fee_policy` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=359 DEFAULT CHARSET=latin1;



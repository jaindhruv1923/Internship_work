-- ==================== chc_middleware ====================
CREATE TABLE `chc_middleware` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `request_id` int unsigned NOT NULL,
  `entity_id` int unsigned DEFAULT NULL,
  `action_id` int unsigned NOT NULL,
  `requested_by` int unsigned NOT NULL,
  `chc_status` enum('open','closed','cancelled','pending','submitted','failed','scheduled') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending',
  `metadata` mediumtext COLLATE utf8mb4_unicode_ci,
  `current_payload` mediumtext COLLATE utf8mb4_unicode_ci,
  `previous_payload` mediumtext COLLATE utf8mb4_unicode_ci,
  `module_action_status` enum('SUCCESS','FAILED','IN_PROCESS') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'IN_PROCESS',
  `module_action_comment` mediumtext COLLATE utf8mb4_unicode_ci,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fk_chc_middleware_request_id_idx` (`request_id`),
  KEY `fk_chc_middleware_action_id_idx` (`action_id`),
  KEY `fk_chc_middleware_requested_by` (`requested_by`),
  CONSTRAINT `fk_chc_middleware_action_id` FOREIGN KEY (`action_id`) REFERENCES `chc_middleware_moderated_action` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_middleware_request_id` FOREIGN KEY (`request_id`) REFERENCES `chc_request` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_middleware_requested_by` FOREIGN KEY (`requested_by`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1968 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ==================== chc_middleware_moderated_action ====================
CREATE TABLE `chc_middleware_moderated_action` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `service_id` int unsigned NOT NULL,
  `entity` varchar(100) NOT NULL,
  `action_name` varchar(100) NOT NULL,
  `action_label` varchar(100) NOT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chc_middleware_moderated_service_id_unique_idx` (`service_id`),
  CONSTRAINT `fk_chc_middleware_moderated_action_service_id` FOREIGN KEY (`service_id`) REFERENCES `chc_service` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=latin1;


-- ==================== chc_request ====================
CREATE TABLE `chc_request` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `service_id` int unsigned NOT NULL,
  `ukid` int unsigned NOT NULL,
  `status` enum('open','closed','cancelled','pending','submitted','failed','scheduled') NOT NULL DEFAULT 'submitted',
  `assignee` int unsigned DEFAULT NULL,
  `created_by` int unsigned DEFAULT NULL,
  `work_centre_id` int unsigned NOT NULL,
  `created_on` timestamp NULL DEFAULT NULL,
  `is_escalated` tinyint(1) NOT NULL DEFAULT '0',
  `is_acknowledged` tinyint(1) NOT NULL DEFAULT '0',
  `is_request_reopened` tinyint(1) NOT NULL DEFAULT '0',
  `middleware_id` int unsigned DEFAULT NULL,
  `cancelled_by` int unsigned DEFAULT NULL,
  `due_id` int unsigned DEFAULT NULL,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `payment_mode` enum('DUES_MANAGEMENT','COST_CENTRE') DEFAULT NULL,
  `form_id` int unsigned DEFAULT NULL,
  `workflow_id` int unsigned DEFAULT NULL,
  `deleted` tinyint unsigned NOT NULL DEFAULT '0',
  `forcefully_cancelled` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_chc_request_service_id_idx` (`service_id`),
  KEY `fk_chc_request_ukid_idx` (`ukid`),
  KEY `fk_chc_request_assignee_idx` (`assignee`),
  KEY `fk_chc_request_work_centre_id_idx` (`work_centre_id`),
  KEY `fk_chc_request_created_by_id_idx` (`created_by`),
  KEY `chc_request_created_on_idx` (`created_on`),
  KEY `chc_request_status_idx` (`status`),
  KEY `chc_request_is_escalated_idx` (`is_escalated`),
  KEY `fk_chc_request_middleware_id` (`middleware_id`),
  KEY `fk_cancelled_by_ukid_idx` (`cancelled_by`),
  KEY `fk_chc_request_due_id` (`due_id`),
  KEY `fk_cr_form_id_idx` (`form_id`),
  KEY `fk_cr_workflow_id_idx` (`workflow_id`),
  CONSTRAINT `fk_cancelled_by_ukid` FOREIGN KEY (`cancelled_by`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_assignee` FOREIGN KEY (`assignee`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_created_by_id` FOREIGN KEY (`created_by`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_due_id` FOREIGN KEY (`due_id`) REFERENCES `dues_v2` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_middleware_id` FOREIGN KEY (`middleware_id`) REFERENCES `chc_middleware` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_service_id` FOREIGN KEY (`service_id`) REFERENCES `chc_service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_ukid` FOREIGN KEY (`ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_work_centre_id` FOREIGN KEY (`work_centre_id`) REFERENCES `chc_work_centre` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cr_form_id` FOREIGN KEY (`form_id`) REFERENCES `chc_request_form` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_cr_workflow_id` FOREIGN KEY (`workflow_id`) REFERENCES `chc_work_centre_flow` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11058 DEFAULT CHARSET=latin1;


-- ==================== chc_request_log ====================
CREATE TABLE `chc_request_log` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `request_id` int unsigned NOT NULL,
  `status` enum('open','closed','cancelled','pending','submitted','failed','scheduled') NOT NULL DEFAULT 'submitted',
  `work_centre_id` int unsigned NOT NULL,
  `assignee_ukid` int unsigned DEFAULT NULL,
  `assigned_by_ukid` int unsigned DEFAULT NULL,
  `created_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `service_escalation_id` int unsigned DEFAULT NULL,
  `is_request_reopened` tinyint(1) NOT NULL DEFAULT '0',
  `form_id` int unsigned DEFAULT NULL,
  `workflow_id` int unsigned DEFAULT NULL,
  `deleted` tinyint unsigned NOT NULL DEFAULT '0',
  `forcefully_cancelled` tinyint unsigned NOT NULL DEFAULT '0',
  `auto_approved` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_chc_request_log_request_id_idx` (`request_id`),
  KEY `fk_chc_request_log_workcentre_id_idx` (`work_centre_id`),
  KEY `fk_chc_request_log_assignee_ukid_idx` (`assignee_ukid`),
  KEY `fk_chc_request_log_assigned_by_ukid_idx` (`assigned_by_ukid`),
  KEY `fk_chc_request_log_service_escalation_id_idx` (`service_escalation_id`),
  KEY `chc_request_log_request_id_id_idx` (`request_id`,`id` DESC),
  KEY `fk_crl_form_id_idx` (`form_id`),
  KEY `fk_crl_workflow_id_idx` (`workflow_id`),
  CONSTRAINT `fk_chc_request_log_assigned_by_ukid` FOREIGN KEY (`assigned_by_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_log_assignee_ukid` FOREIGN KEY (`assignee_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_log_request_id` FOREIGN KEY (`request_id`) REFERENCES `chc_request` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_log_service_escalation_id` FOREIGN KEY (`service_escalation_id`) REFERENCES `chc_service_escalation` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_request_log_workcentre_id` FOREIGN KEY (`work_centre_id`) REFERENCES `chc_work_centre` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_crl_form_id` FOREIGN KEY (`form_id`) REFERENCES `chc_request_form` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_crl_workflow_id` FOREIGN KEY (`workflow_id`) REFERENCES `chc_work_centre_flow` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30135 DEFAULT CHARSET=latin1;


-- ==================== chc_service ====================
CREATE TABLE `chc_service` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `description` text,
  `icon` varchar(100) NOT NULL,
  `service_desk_id` int unsigned NOT NULL,
  `is_paid` tinyint(1) NOT NULL DEFAULT '0',
  `cost_center_id` int unsigned DEFAULT NULL,
  `cost_item_id` int unsigned DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `currency` char(3) DEFAULT NULL,
  `due_category_id` int unsigned DEFAULT NULL,
  `is_escalation_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `is_comments_disabled` tinyint(1) NOT NULL DEFAULT '0',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `is_anonymous` tinyint(1) NOT NULL DEFAULT '0',
  `is_send_email` tinyint(1) NOT NULL DEFAULT '0',
  `is_acknowledgement_available` tinyint(1) NOT NULL DEFAULT '0',
  `acknowledgement_time` int DEFAULT NULL,
  `duplicate_request` tinyint(1) NOT NULL DEFAULT '0',
  `is_cancellation_allowed` tinyint(1) NOT NULL DEFAULT '0',
  `is_qr_enabled` tinyint(1) DEFAULT '0',
  `allow_request_for_others` tinyint(1) NOT NULL DEFAULT '1',
  `allow_bulk_creation` tinyint unsigned NOT NULL DEFAULT '0',
  `is_feedback_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `working_hours_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `cancellation_reason_mandatory` tinyint(1) NOT NULL DEFAULT '0',
  `is_request_editable` tinyint(1) NOT NULL DEFAULT '0',
  `is_request_time_restriction_allowed` tinyint(1) NOT NULL DEFAULT '0',
  `is_reopening_allowed` tinyint(1) NOT NULL DEFAULT '0',
  `is_middleware_service` tinyint(1) NOT NULL DEFAULT '0',
  `is_fixed_service` tinyint(1) NOT NULL DEFAULT '0',
  `is_auto_fill_field_editable` tinyint(1) NOT NULL DEFAULT '0',
  `is_request_limit_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `comment_tagging_enabled` tinyint unsigned NOT NULL DEFAULT '0',
  `schedule_request_enabled` tinyint unsigned NOT NULL DEFAULT '0',
  `integrated_service` tinyint(1) DEFAULT '0',
  `current_form_id` int unsigned DEFAULT NULL,
  `current_workflow_id` int unsigned DEFAULT NULL,
  `bypass_capping_limit` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_chc_service_service_desk_id_idx` (`service_desk_id`),
  KEY `fk_chc_service_cost_center_id_idx` (`cost_center_id`),
  KEY `fk_chc_service_cost_item_id_idx` (`cost_item_id`),
  KEY `chc_service_is_deleted_idx` (`is_deleted`),
  KEY `idx_chc_service_due_category_id` (`due_category_id`),
  KEY `fk_cs_current_form_id_idx` (`current_form_id`),
  KEY `fk_cs_current_workflow_id_idx` (`current_workflow_id`),
  CONSTRAINT `fk_chc_service_cost_center_id` FOREIGN KEY (`cost_center_id`) REFERENCES `payment_cost_center` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_service_cost_item_id` FOREIGN KEY (`cost_item_id`) REFERENCES `payment_cost_item` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_service_due_category_id` FOREIGN KEY (`due_category_id`) REFERENCES `dues_category_v2` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_service_service_desk_id` FOREIGN KEY (`service_desk_id`) REFERENCES `chc_service_desk` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cs_current_form_id` FOREIGN KEY (`current_form_id`) REFERENCES `chc_request_form` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_cs_current_workflow_id` FOREIGN KEY (`current_workflow_id`) REFERENCES `chc_work_centre_flow` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=684 DEFAULT CHARSET=latin1;


-- ==================== chc_work_centre ====================
CREATE TABLE `chc_work_centre` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `service_id` int unsigned NOT NULL,
  `workflow_id` int unsigned DEFAULT NULL,
  `title` text NOT NULL,
  `assignment_type` enum('autoAssign','defaultAssign','entityAssign') NOT NULL DEFAULT 'autoAssign',
  `reassignment_type` enum('manualAssign') NOT NULL DEFAULT 'manualAssign',
  `parent_work_centre_id` int unsigned DEFAULT NULL,
  `is_closure_work_centre` tinyint(1) NOT NULL DEFAULT '0',
  `assignment_entity_id` int unsigned DEFAULT NULL,
  `is_cancellation_allowed` tinyint(1) NOT NULL DEFAULT '0',
  `hide_request_status` tinyint(1) NOT NULL DEFAULT '0',
  `assignment_category` enum('COMMON','FIELD','GROUP') NOT NULL DEFAULT 'COMMON',
  `is_ivr_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0',
  `approval_by_sms` tinyint unsigned NOT NULL DEFAULT '0',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_chc_work_centre_service_id_idx` (`service_id`),
  KEY `fk_cwc_workflow_id_idx` (`workflow_id`),
  CONSTRAINT `fk_chc_work_centre_service_id` FOREIGN KEY (`service_id`) REFERENCES `chc_service` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cwc_workflow_id` FOREIGN KEY (`workflow_id`) REFERENCES `chc_work_centre_flow` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=846 DEFAULT CHARSET=latin1;


-- ==================== chc_work_centre_action ====================
CREATE TABLE `chc_work_centre_action` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `work_centre_id` int unsigned NOT NULL,
  `name` text NOT NULL,
  `require_note` tinyint(1) NOT NULL DEFAULT '0',
  `action_taken_name` text NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `type` enum('positive','negative') NOT NULL DEFAULT 'positive',
  `is_form_available` tinyint(1) NOT NULL DEFAULT '0',
  `is_termination_action` tinyint(1) NOT NULL DEFAULT '0',
  `auto_action_date_range_field_id` int unsigned DEFAULT NULL,
  `setting_id` int unsigned DEFAULT NULL,
  `action_response_type_id` int unsigned DEFAULT NULL,
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_chc_work_centre_action_work_centre_id_idx` (`work_centre_id`),
  KEY `fk_chc_work_centre_action_auto_action_id_idx` (`auto_action_date_range_field_id`),
  KEY `fk_chc_work_centre_action_setting_id_idx` (`setting_id`),
  KEY `fk_chc_work_centre_action_response_type_id_idx` (`action_response_type_id`),
  CONSTRAINT `fk_chc_work_centre_action_auto_action_id` FOREIGN KEY (`auto_action_date_range_field_id`) REFERENCES `chc_request_form_date_range_field` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_work_centre_action_response_type_id` FOREIGN KEY (`action_response_type_id`) REFERENCES `chc_work_centre_action_response_type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_work_centre_action_setting_id` FOREIGN KEY (`setting_id`) REFERENCES `chc_work_centre_action_setting` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_work_centre_action_work_centre_id` FOREIGN KEY (`work_centre_id`) REFERENCES `chc_work_centre` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1414 DEFAULT CHARSET=latin1;


-- ==================== chc_work_centre_request_action ====================
CREATE TABLE `chc_work_centre_request_action` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `request_id` int unsigned NOT NULL,
  `work_centre_id` int unsigned NOT NULL,
  `taken_by_ukid` int unsigned NOT NULL,
  `action_id` int unsigned NOT NULL,
  `note` text,
  `created_on` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_chc_work_centre_request_action_request_id_idx` (`request_id`),
  KEY `fk_chc_work_centre_request_action_work_centre_id_idx` (`work_centre_id`),
  KEY `fk_chc_work_centre_request_action_taken_by_ukid_idx` (`taken_by_ukid`),
  KEY `fk_chc_work_centre_request_action_action_id_idx` (`action_id`),
  CONSTRAINT `fk_chc_work_centre_request_action_action_id` FOREIGN KEY (`action_id`) REFERENCES `chc_work_centre_action` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_work_centre_request_action_request_id` FOREIGN KEY (`request_id`) REFERENCES `chc_request` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_work_centre_request_action_taken_by_ukid` FOREIGN KEY (`taken_by_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_chc_work_centre_request_action_work_centre_id` FOREIGN KEY (`work_centre_id`) REFERENCES `chc_work_centre` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7905 DEFAULT CHARSET=latin1;


-- ==================== gate_pass_audience ====================
CREATE TABLE `gate_pass_audience` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ukid` int unsigned NOT NULL,
  `day_pass_allowed` tinyint unsigned NOT NULL DEFAULT '0',
  `long_pass_allowed` tinyint unsigned NOT NULL DEFAULT '0',
  `not_allowed_from` datetime DEFAULT NULL,
  `not_allowed_till` datetime DEFAULT NULL,
  `long_pass_not_allowed_from` datetime DEFAULT NULL,
  `long_pass_not_allowed_till` datetime DEFAULT NULL,
  `defaulter_count` int unsigned DEFAULT '0',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gate_pass_audience_unique` (`ukid`),
  KEY `fk_gate_pass_audience_1_idx` (`ukid`),
  CONSTRAINT `fk_gate_pass_audience_ukid` FOREIGN KEY (`ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26849 DEFAULT CHARSET=latin1;


-- ==================== gate_pass_log ====================
CREATE TABLE `gate_pass_log` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ukid` int unsigned NOT NULL,
  `in_entry` datetime DEFAULT NULL,
  `out_entry` datetime DEFAULT NULL,
  `status_id` int unsigned DEFAULT NULL,
  `marked_out_ukid` int unsigned DEFAULT NULL,
  `marked_in_ukid` int unsigned DEFAULT NULL,
  `marked_in_device` int unsigned DEFAULT NULL,
  `marked_out_device` int unsigned DEFAULT NULL,
  `notification_sent` tinyint(1) NOT NULL DEFAULT '0',
  `accommodation_type` enum('DAY_SCHOLAR','HOSTELLER','RESIDENT','NON_RESIDENT') NOT NULL DEFAULT 'HOSTELLER',
  `user_type` varchar(25) DEFAULT NULL,
  `pass_type` enum('DAY_PASS','LONG_PASS') NOT NULL DEFAULT 'DAY_PASS',
  `defaulter` tinyint(1) NOT NULL DEFAULT '0',
  `defaulted_on` datetime DEFAULT NULL,
  `missing_entry_reason` varchar(255) DEFAULT NULL,
  `hostel_id` int unsigned DEFAULT NULL,
  `marked_in_auto_entry` tinyint unsigned NOT NULL DEFAULT '0',
  `marked_out_auto_entry` tinyint unsigned NOT NULL DEFAULT '0',
  `in_punch_type` enum('MANUAL_ENTRY','BIOMETRIC','QR_PUNCH','AUTO_ENTRY') DEFAULT NULL,
  `out_punch_type` enum('MANUAL_ENTRY','BIOMETRIC','QR_PUNCH','AUTO_ENTRY') DEFAULT NULL,
  `created_timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_gate_pass_log_1_idx` (`ukid`),
  KEY `fk_gate_pass_log_2_idx` (`status_id`),
  KEY `fk_gate_pass_log_3_idx` (`marked_out_ukid`),
  KEY `fk_gate_pass_log_mar_in_ukid_idx` (`marked_in_ukid`),
  KEY `fk_gate_pass_log_in_device_idx` (`marked_in_device`),
  KEY `fk_gate_pass_log_out_device_idx` (`marked_out_device`),
  KEY `gate_pass_log_created_modified_timestamp_idx` (`created_timestamp`,`modified_timestamp`),
  KEY `gate_pass_log_defaulted_on_idx` (`defaulted_on`),
  KEY `gate_pass_log_user_type_idx` (`user_type`),
  KEY `gate_pass_log_accommodation_type_idx` (`accommodation_type`),
  KEY `gate_pass_log_accommodation_user_dates_idx` (`accommodation_type`,`user_type`,`out_entry`,`in_entry`),
  KEY `gate_pass_log_out_entry_idx` (`out_entry`),
  KEY `gate_pass_log_in_entry_idx` (`in_entry`),
  CONSTRAINT `fk_gate_pass_log_id` FOREIGN KEY (`status_id`) REFERENCES `gate_pass_status` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_log_in_device` FOREIGN KEY (`marked_in_device`) REFERENCES `biometric_device` (`device_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_log_mar_in_ukid` FOREIGN KEY (`marked_in_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_log_mar_ukid` FOREIGN KEY (`marked_out_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_log_out_device` FOREIGN KEY (`marked_out_device`) REFERENCES `biometric_device` (`device_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_log_ukid` FOREIGN KEY (`ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4058 DEFAULT CHARSET=latin1;


-- ==================== gate_pass_long_pass ====================
CREATE TABLE `gate_pass_long_pass` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ukid` int unsigned NOT NULL,
  `log_id` int unsigned DEFAULT NULL,
  `middleware_id` int unsigned NOT NULL,
  `pass_start` datetime NOT NULL,
  `pass_end` datetime NOT NULL,
  `status_id` int unsigned DEFAULT NULL,
  `pass_status` enum('availed','expired','cancelled') DEFAULT NULL,
  `hostel_id` int unsigned DEFAULT NULL,
  `cancelled_by` int unsigned DEFAULT NULL,
  `cancel_reason` varchar(500) DEFAULT NULL,
  `missing_entry_reason` varchar(255) DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_gate_pass_long_pass_middleware_id_idx` (`middleware_id`),
  UNIQUE KEY `unique_gate_pass_long_pass_log_id_idx` (`log_id`),
  KEY `fk_gate_pass_long_pass_ukid_idx` (`ukid`),
  KEY `fk_gate_pass_long_pass_log_id_idx` (`log_id`),
  KEY `fk_gate_pass_long_pass_middleware_id_idx` (`middleware_id`),
  KEY `fk_gate_pass_long_pass_status_id_idx` (`status_id`),
  KEY `fk_gate_pass_long_pass_cancelled_by_idx` (`cancelled_by`),
  CONSTRAINT `fk_gate_pass_long_pass_cancelled_by` FOREIGN KEY (`cancelled_by`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_long_pass_log_id` FOREIGN KEY (`log_id`) REFERENCES `gate_pass_log` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_long_pass_middleware_id` FOREIGN KEY (`middleware_id`) REFERENCES `chc_middleware` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_long_pass_status_id` FOREIGN KEY (`status_id`) REFERENCES `gate_pass_status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_gate_pass_long_pass_ukid` FOREIGN KEY (`ukid`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=315 DEFAULT CHARSET=latin1;


-- ==================== gate_pass_requests ====================
CREATE TABLE `gate_pass_requests` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ukid` int unsigned NOT NULL,
  `entity_id` int unsigned NOT NULL,
  `entity` varchar(45) NOT NULL,
  `is_valid` tinyint(1) DEFAULT NULL,
  `created_timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_gate_pass_requests_ukid_idx` (`ukid`),
  CONSTRAINT `fk_gate_pass_requests_ukid` FOREIGN KEY (`ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;


-- ==================== gate_pass_status ====================
CREATE TABLE `gate_pass_status` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(45) NOT NULL,
  `status` varchar(45) NOT NULL,
  `count_as_in` tinyint(1) DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gate_pass_status_code_uq` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;


-- ==================== hostel_allotment ====================
CREATE TABLE `hostel_allotment` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `infrastructure_id` int unsigned NOT NULL,
  `child_infrastructure_id` int unsigned DEFAULT NULL,
  `occupant_ukid` int unsigned NOT NULL,
  `admin_ukid` int unsigned DEFAULT NULL,
  `check_in` datetime DEFAULT NULL,
  `check_out` datetime DEFAULT NULL,
  `remark` text,
  `allotment_start_date` date DEFAULT NULL,
  `allotment_end_date` date DEFAULT NULL,
  `status` enum('provisional','confirmed','checkedout','cancelled') NOT NULL,
  `amount_paid` double(10,2) DEFAULT NULL,
  `total_amount` double(10,2) DEFAULT NULL,
  `entity` varchar(100) DEFAULT NULL,
  `entity_id` int unsigned DEFAULT NULL,
  `pay_by_dues` tinyint(1) NOT NULL DEFAULT '0',
  `payment_id` int unsigned DEFAULT NULL,
  `payment_mode` enum('ACADEMIC_FEE','DUES','OFFLINE','DUES_MANAGEMENT') NOT NULL DEFAULT 'OFFLINE',
  `fee_option_id` int unsigned DEFAULT NULL,
  `due_id` int unsigned DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `due_id_UNIQUE` (`due_id`),
  KEY `fk_hostel_allotment_infrastructure_idx` (`infrastructure_id`),
  KEY `fk_hostel_allotment_occupant_idx` (`occupant_ukid`),
  KEY `fk_hostel_allotment_admin_idx` (`admin_ukid`),
  KEY `fk_hostel_allotment_child_infrastructure_idx` (`child_infrastructure_id`),
  KEY `fk_hostel_allotment_option_id_fk_hostel_fee_option_idx` (`fee_option_id`),
  CONSTRAINT `fk_hostel_allotment_admin` FOREIGN KEY (`admin_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_hostel_allotment_child_infrastructure` FOREIGN KEY (`child_infrastructure_id`) REFERENCES `infrastructure_version` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_hostel_allotment_due_id_ref_dues_v2` FOREIGN KEY (`due_id`) REFERENCES `dues_v2` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_hostel_allotment_infrastructure` FOREIGN KEY (`infrastructure_id`) REFERENCES `infrastructure_version` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_hostel_allotment_occupant` FOREIGN KEY (`occupant_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_hostel_allotment_option_id_fk_hostel_fee_option` FOREIGN KEY (`fee_option_id`) REFERENCES `hostel_fee_policy_option` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4882 DEFAULT CHARSET=latin1;


-- ==================== hostel_fee_policy ====================
CREATE TABLE `hostel_fee_policy` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `code` varchar(255) NOT NULL,
  `is_active` tinyint unsigned NOT NULL DEFAULT '1',
  `activated_by` int unsigned DEFAULT NULL,
  `activated_on` datetime DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_code_UNIQUE` (`name`,`code`)
) ENGINE=InnoDB AUTO_INCREMENT=475 DEFAULT CHARSET=latin1;


-- ==================== hostel_fee_policy_option ====================
CREATE TABLE `hostel_fee_policy_option` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `fee_policy_id` int unsigned NOT NULL,
  `user_type` enum('STUDENT','STAFF') NOT NULL DEFAULT 'STUDENT',
  `name` varchar(200) NOT NULL,
  `code` varchar(10) DEFAULT NULL,
  `auto_generated_code` tinyint unsigned NOT NULL DEFAULT '0',
  `amount` decimal(10,2) NOT NULL,
  `deposit` decimal(10,2) NOT NULL,
  `infrastructure_id` int unsigned DEFAULT NULL,
  `capacity` int unsigned NOT NULL,
  `total_beds` int unsigned DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `attributes_filter` enum('MATCH_ALL','MATCH_ANY') DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_hostel_fee_policy_option_code` (`code`),
  KEY `fk_fee_option_fee_policy_id_references_fee_policy_id_idx` (`fee_policy_id`),
  KEY `fk_fee_policy_option_infrastructure_id_references_infrastru_idx` (`infrastructure_id`),
  KEY `idx_user_type_policy` (`fee_policy_id`,`user_type`),
  CONSTRAINT `fk_fee_option_fee_policy_id_references_fee_policy_id` FOREIGN KEY (`fee_policy_id`) REFERENCES `hostel_fee_policy` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_fee_policy_option_infrastructure_id_references_infrastructure` FOREIGN KEY (`infrastructure_id`) REFERENCES `infrastructure_version` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=830 DEFAULT CHARSET=latin1;


-- ==================== hostel_option_selection ====================
CREATE TABLE `hostel_option_selection` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `hostel_allotment_id` int unsigned DEFAULT NULL,
  `occupant_ukid` int unsigned NOT NULL,
  `option_id` int unsigned NOT NULL,
  `selected_on` datetime NOT NULL,
  `selection_type` enum('SELF','ADMIN') NOT NULL,
  `selected_by` int unsigned NOT NULL,
  `payment_mode` enum('OFFLINE','DUES_MANAGEMENT') NOT NULL,
  `due_id` int unsigned DEFAULT NULL,
  `status` enum('PROVISIONAL','CONFIRMED','NOT_ALLOTTED','CANCELLED','EXPIRED','CHECKEDOUT') NOT NULL,
  `building_id` int unsigned DEFAULT NULL,
  `infrastructure_id` int unsigned DEFAULT NULL,
  `child_infrastructure_id` int unsigned DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `allotment_id_UNIQUE` (`hostel_allotment_id`),
  UNIQUE KEY `due_id_UNIQUE` (`due_id`),
  KEY `fk_occupant_ukid_ref_ukid_authenticator` (`occupant_ukid`),
  KEY `fk_selection_option_id_ref_id_policy_option` (`option_id`),
  KEY `fk_selection_selected_by_ref_authenticator` (`selected_by`),
  KEY `idx_hostel_option_selection_building_id` (`building_id`),
  KEY `idx_hostel_option_selection_infrastructure_id` (`infrastructure_id`),
  KEY `idx_hostel_option_selection_child_infrastructure_id` (`child_infrastructure_id`),
  CONSTRAINT `fk_hostel_allotment_id_ref_id_hostel_allotment` FOREIGN KEY (`hostel_allotment_id`) REFERENCES `hostel_allotment` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_occupant_ukid_ref_ukid_authenticator` FOREIGN KEY (`occupant_ukid`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE,
  CONSTRAINT `fk_selection_bedId_ref_infrastructure` FOREIGN KEY (`child_infrastructure_id`) REFERENCES `infrastructure_version` (`id`),
  CONSTRAINT `fk_selection_buildingId_ref_infrastructure` FOREIGN KEY (`building_id`) REFERENCES `infrastructure_version` (`id`),
  CONSTRAINT `fk_selection_due_id_ref_dues_v2` FOREIGN KEY (`due_id`) REFERENCES `dues_v2` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_selection_infraId_ref_infrastructure` FOREIGN KEY (`infrastructure_id`) REFERENCES `infrastructure_version` (`id`),
  CONSTRAINT `fk_selection_option_id_ref_id_policy_option` FOREIGN KEY (`option_id`) REFERENCES `hostel_fee_policy_option` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_selection_selected_by_ref_authenticator` FOREIGN KEY (`selected_by`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2615 DEFAULT CHARSET=latin1;


-- ==================== infra_booking ====================
CREATE TABLE `infra_booking` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `booking_name` varchar(200) NOT NULL,
  `purpose` text,
  `special_request` text,
  `requester_ukid` int unsigned NOT NULL,
  `requester_department_id` int unsigned DEFAULT NULL,
  `booking_for_ukid` int unsigned DEFAULT NULL,
  `visitor_id` int unsigned DEFAULT NULL,
  `booking_source` enum('DIRECT','REQUEST') NOT NULL,
  `parent_booking_id` int DEFAULT NULL,
  `booking_module` varchar(50) NOT NULL DEFAULT 'VENUE_BOOKING',
  `is_multi_venue` tinyint(1) NOT NULL DEFAULT '0',
  `recurrence` enum('NONE','DAILY','WEEKLY','MONTHLY','YEARLY') NOT NULL DEFAULT 'NONE',
  `status` enum('PENDING_ALLOTMENT','ALLOTTED','PARTIALLY_ALLOTTED','REJECTED','CANCELLED','EXPIRED') NOT NULL,
  `priority` enum('NONE','LOW','MEDIUM','HIGH') NOT NULL DEFAULT 'NONE',
  `cancelled_by` int unsigned DEFAULT NULL,
  `cancelled_timestamp` datetime DEFAULT NULL,
  `booking_start_datetime` datetime NOT NULL,
  `booking_end_datetime` datetime NOT NULL,
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_infra_booking_status` (`status`),
  KEY `idx_infra_booking_requester` (`requester_ukid`),
  KEY `idx_infra_booking_for_ukid` (`booking_for_ukid`),
  KEY `idx_infra_booking_source` (`booking_source`),
  KEY `fk_infra_booking_visitor_id` (`visitor_id`),
  KEY `fk_infra_booking_cancelled_by` (`cancelled_by`),
  KEY `idx_infra_booking_requester_department` (`requester_department_id`),
  CONSTRAINT `fk_infra_booking_booking_for_ukid` FOREIGN KEY (`booking_for_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_infra_booking_cancelled_by` FOREIGN KEY (`cancelled_by`) REFERENCES `authenticator` (`ukid`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_infra_booking_requester_department_id` FOREIGN KEY (`requester_department_id`) REFERENCES `department` (`department_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_infra_booking_requester_ukid` FOREIGN KEY (`requester_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_infra_booking_visitor_id` FOREIGN KEY (`visitor_id`) REFERENCES `infrastructure_visitor_details` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=220445 DEFAULT CHARSET=latin1;


-- ==================== infra_booking_item ====================
CREATE TABLE `infra_booking_item` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `booking_id` int unsigned NOT NULL,
  `infrastructure_type_id` int unsigned NOT NULL,
  `infrastructure_id` int unsigned NOT NULL,
  `start_datetime` datetime NOT NULL,
  `end_datetime` datetime NOT NULL,
  `item_status` enum('PENDING_ALLOTMENT','ALLOTTED','PARTIALLY_ALLOTTED','REJECTED','CANCELLED','EXPIRED') NOT NULL,
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `action_taken_by` int unsigned DEFAULT NULL,
  `reason` text,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_infra_booking_item_booking` (`booking_id`,`deleted`,`item_status`),
  KEY `idx_infra_booking_item_venue_time` (`infrastructure_id`,`deleted`,`start_datetime`,`end_datetime`),
  KEY `idx_infra_booking_item_type` (`infrastructure_type_id`),
  CONSTRAINT `fk_infra_booking_item_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `infra_booking` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_infra_booking_item_infrastructure_id` FOREIGN KEY (`infrastructure_id`) REFERENCES `infrastructure_version` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_infra_booking_item_infrastructure_type_id` FOREIGN KEY (`infrastructure_type_id`) REFERENCES `infrastructure_type` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=181644 DEFAULT CHARSET=latin1;


-- ==================== infra_booking_request_allotment_map ====================
CREATE TABLE `infra_booking_request_allotment_map` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `request_detail_id` int unsigned NOT NULL,
  `booking_item_id` int unsigned NOT NULL,
  `is_system_recommended` tinyint(1) NOT NULL DEFAULT '0',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_infra_booking_request_allotment` (`request_detail_id`,`booking_item_id`),
  KEY `idx_allotment_booking_item` (`booking_item_id`),
  CONSTRAINT `fk_infra_booking_request_allotment_map_booking_item_id` FOREIGN KEY (`booking_item_id`) REFERENCES `infra_booking_item` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_infra_booking_request_allotment_map_request_detail_id` FOREIGN KEY (`request_detail_id`) REFERENCES `infra_booking_request_detail` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=latin1;


-- ==================== infra_booking_request_detail ====================
CREATE TABLE `infra_booking_request_detail` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `booking_id` int unsigned NOT NULL,
  `infrastructure_type_id` int unsigned NOT NULL,
  `venue_count` int unsigned NOT NULL,
  `min_occupancy` int unsigned DEFAULT NULL,
  `start_datetime` datetime NOT NULL,
  `end_datetime` datetime NOT NULL,
  `allotted_count` int unsigned NOT NULL DEFAULT '0',
  `waitlisted_count` int unsigned NOT NULL DEFAULT '0',
  `rejected_count` int unsigned NOT NULL DEFAULT '0',
  `expired_count` int unsigned NOT NULL DEFAULT '0',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_infra_booking_request_detail_booking` (`booking_id`),
  KEY `idx_infra_booking_request_detail_type` (`infrastructure_type_id`),
  CONSTRAINT `fk_infra_booking_request_detail_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `infra_booking` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_infra_booking_request_detail_infrastructure_type_id` FOREIGN KEY (`infrastructure_type_id`) REFERENCES `infrastructure_type` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;


-- ==================== infrastructure_master ====================
CREATE TABLE `infrastructure_master` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `infrastructure_version_id` int unsigned NOT NULL,
  `name` varchar(200) NOT NULL,
  `code` varchar(10) DEFAULT NULL,
  `description` text,
  `capacity` int unsigned DEFAULT NULL,
  `type_id` int unsigned DEFAULT NULL,
  `parent_id` int unsigned DEFAULT NULL,
  `archived` tinyint unsigned NOT NULL DEFAULT '0',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `INFRASTRUCTURE_VERSION_ID_UNIQUE` (`infrastructure_version_id`),
  KEY `fk_infrastructure_type_id` (`type_id`),
  CONSTRAINT `fk_infrastructure_type_id` FOREIGN KEY (`type_id`) REFERENCES `infrastructure_type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_infrastructure_version_id` FOREIGN KEY (`infrastructure_version_id`) REFERENCES `infrastructure_version` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3059 DEFAULT CHARSET=latin1;


-- ==================== infrastructure_type ====================
CREATE TABLE `infrastructure_type` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(45) DEFAULT NULL,
  `identifier` varchar(100) DEFAULT NULL COMMENT 'Unique identifier for infrastructure type',
  `category` varchar(150) DEFAULT NULL,
  `college_id` int unsigned DEFAULT NULL,
  `full_day_booking` tinyint(1) NOT NULL DEFAULT '0',
  `check_in_time` time DEFAULT NULL COMMENT 'Check-in time for infrastructure booking',
  `check_out_time` time DEFAULT NULL COMMENT 'Check-out time for infrastructure booking',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
  `modified_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Record modification timestamp',
  `venue_rule_cascade_processing` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `type` (`type`),
  UNIQUE KEY `uk_infrastructure_type_identifier` (`identifier`),
  KEY `fk_infrastructure_type_college_id_idx` (`college_id`),
  CONSTRAINT `fk_infrastructure_type_college_id` FOREIGN KEY (`college_id`) REFERENCES `college` (`college_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=latin1;


-- ==================== infrastructure_version ====================
CREATE TABLE `infrastructure_version` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `college_id` int unsigned NOT NULL,
  `opening_time` time DEFAULT NULL,
  `closing_time` time DEFAULT NULL,
  `contact_name` varchar(200) DEFAULT NULL,
  `contact_phone` varchar(15) DEFAULT NULL,
  `compulsory` tinyint unsigned NOT NULL DEFAULT '0',
  `is_bookable` tinyint(1) NOT NULL DEFAULT '0',
  `bookable_by_student` tinyint(1) NOT NULL DEFAULT '1',
  `bookable_by_faculty` tinyint(1) NOT NULL DEFAULT '1',
  `bookable_by_administrator` tinyint(1) NOT NULL DEFAULT '1',
  `description` text,
  `capacity` int unsigned DEFAULT NULL,
  `type_id` int unsigned DEFAULT NULL,
  `requires_approval` tinyint(1) DEFAULT '0',
  `student_requires_approval` tinyint(1) NOT NULL DEFAULT '1',
  `faculty_requires_approval` tinyint(1) NOT NULL DEFAULT '1',
  `administrator_requires_approval` tinyint(1) NOT NULL DEFAULT '1',
  `floor_id` int unsigned DEFAULT NULL,
  `established_on` date DEFAULT NULL,
  `number_of_floors` int DEFAULT NULL,
  `number_of_floors_under` int DEFAULT '0',
  `number_of_rooms` int DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  `contact_ukid` int unsigned DEFAULT NULL,
  `disclaimer` text,
  `availability` int unsigned DEFAULT NULL,
  `is_paid_booking` tinyint(1) NOT NULL DEFAULT '0',
  `code` varchar(10) DEFAULT NULL,
  `version` int unsigned NOT NULL DEFAULT '1',
  `current_version` tinyint unsigned NOT NULL DEFAULT '1',
  `archived` tinyint unsigned NOT NULL DEFAULT '0',
  `infrastructure_master_id` int unsigned DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` int unsigned DEFAULT NULL,
  `migrated` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_infrastructure_college_idx` (`college_id`),
  KEY `fk_infrastructure_type_idx` (`type_id`),
  KEY `fk_infrastructure_floor_id_idx` (`floor_id`),
  KEY `fk_infrastructure_contact_ukid_idx` (`contact_ukid`),
  KEY `fk_infrastructure_master_id` (`infrastructure_master_id`),
  KEY `fk_infrastructure_version_created_by` (`created_by`),
  KEY `idx_infrastructure_version_migrated` (`migrated`),
  CONSTRAINT `fk_infrastructure_college` FOREIGN KEY (`college_id`) REFERENCES `college` (`college_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_infrastructure_contact_ukid` FOREIGN KEY (`contact_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_infrastructure_floor_id` FOREIGN KEY (`floor_id`) REFERENCES `infrastructure_floor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_infrastructure_master_id` FOREIGN KEY (`infrastructure_master_id`) REFERENCES `infrastructure_master` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_infrastructure_type` FOREIGN KEY (`type_id`) REFERENCES `infrastructure_type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_infrastructure_version_created_by` FOREIGN KEY (`created_by`) REFERENCES `authenticator` (`ukid`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3306 DEFAULT CHARSET=latin1;


-- ==================== placement_application ====================
CREATE TABLE `placement_application` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `ukid` int unsigned NOT NULL,
  `job_id` int unsigned NOT NULL,
  `attachment` int unsigned DEFAULT NULL,
  `status_id` int unsigned DEFAULT NULL,
  `comment` text,
  `published_status_id` int DEFAULT NULL,
  `action_taken_on_offer` tinyint(1) NOT NULL DEFAULT '0',
  `last_date_to_take_action` datetime DEFAULT NULL,
  `offer_status_id` int unsigned DEFAULT NULL,
  `action_taken_on_offer_date` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `status_comment` text,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_placement_application_job_id_idx` (`job_id`),
  KEY `fk_placement_application_ukid_idx` (`ukid`),
  KEY `fk_placement_application_attachment_idx` (`attachment`),
  KEY `fk_placement_application_status_id_idx` (`status_id`),
  KEY `fk_placement_application_offer_idx` (`offer_status_id`),
  CONSTRAINT `fk_placement_application_attachment` FOREIGN KEY (`attachment`) REFERENCES `media_object` (`media_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_application_auth_ukid` FOREIGN KEY (`ukid`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_application_job_id` FOREIGN KEY (`job_id`) REFERENCES `placement_job` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_application_offer` FOREIGN KEY (`offer_status_id`) REFERENCES `placement_offer_status` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `fk_placement_application_status_id` FOREIGN KEY (`status_id`) REFERENCES `placement_application_status` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8183 DEFAULT CHARSET=latin1;


-- ==================== placement_application_status ====================
CREATE TABLE `placement_application_status` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `default_status` tinyint(1) NOT NULL DEFAULT '0',
  `permanent` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=latin1;


-- ==================== placement_job ====================
CREATE TABLE `placement_job` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `organization_id` int unsigned NOT NULL,
  `college_id` int unsigned NOT NULL,
  `designation` varchar(255) NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `renumeration_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `ctc` int unsigned DEFAULT NULL,
  `ctc_type` enum('annually','monthly') NOT NULL DEFAULT 'annually',
  `ctc_currency` int unsigned DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `category_id` int unsigned DEFAULT NULL,
  `venue` varchar(255) DEFAULT NULL,
  `visit_date` timestamp NULL DEFAULT NULL,
  `last_date` timestamp NULL DEFAULT NULL,
  `notes` text,
  `selection_process` text,
  `joining_date` timestamp NULL DEFAULT NULL,
  `placement_type_id` int unsigned DEFAULT NULL,
  `opportunity_type_id` int unsigned DEFAULT NULL,
  `created_by` int unsigned DEFAULT NULL,
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0',
  `is_closed` tinyint unsigned NOT NULL DEFAULT '0',
  `vacancies` int unsigned DEFAULT NULL,
  `is_ctc_in_range` tinyint unsigned NOT NULL DEFAULT '0',
  `minimum_ctc_range` int DEFAULT NULL,
  `maximum_ctc_range` int DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_archived` tinyint(1) NOT NULL DEFAULT '0',
  `placement_cycle` int unsigned DEFAULT NULL,
  `is_draft` tinyint(1) NOT NULL DEFAULT '0',
  `is_published` tinyint(1) NOT NULL DEFAULT '1',
  `score_from_student_management` tinyint unsigned NOT NULL DEFAULT '0',
  `enable_acceptance_offer` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_placement_job_category_idx` (`category_id`),
  KEY `fk_placement_job_college_idx` (`college_id`),
  KEY `fk_placement_job_organization_id_idx` (`organization_id`),
  KEY `placement_job_placement_types_FK` (`placement_type_id`),
  KEY `placement_job_opportunity_types_FK` (`opportunity_type_id`),
  KEY `fk_placement_job_created_by_idx` (`created_by`),
  KEY `fk_placement_job_currency_code_idx` (`ctc_currency`),
  KEY `fk_placement_job_placement_cycle_idx` (`placement_cycle`),
  CONSTRAINT `fk_placement_job_category` FOREIGN KEY (`category_id`) REFERENCES `placement_job_category` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `fk_placement_job_college` FOREIGN KEY (`college_id`) REFERENCES `college` (`college_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_job_created_by` FOREIGN KEY (`created_by`) REFERENCES `user_attributes` (`ukid`),
  CONSTRAINT `fk_placement_job_currency_code` FOREIGN KEY (`ctc_currency`) REFERENCES `currency` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_job_organization_id_placement_organization` FOREIGN KEY (`organization_id`) REFERENCES `placement_organization` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_job_placement_cycle` FOREIGN KEY (`placement_cycle`) REFERENCES `placement_cycle` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `placement_job_opportunity_types_FK` FOREIGN KEY (`opportunity_type_id`) REFERENCES `placement_opportunity_types` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `placement_job_placement_types_FK` FOREIGN KEY (`placement_type_id`) REFERENCES `placement_types` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2813 DEFAULT CHARSET=latin1;


-- ==================== placement_offer_status ====================
CREATE TABLE `placement_offer_status` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `action_taken_name` varchar(255) DEFAULT NULL,
  `description` text,
  `is_permanent` tinyint(1) NOT NULL DEFAULT '0',
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `is_system_status` tinyint(1) NOT NULL DEFAULT '0',
  `is_status_comment_required` tinyint(1) NOT NULL DEFAULT '0',
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;


-- ==================== placement_organization ====================
CREATE TABLE `placement_organization` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `college_id` int unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text,
  `logo_id` int unsigned DEFAULT NULL,
  `website` text,
  `code` varchar(255) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `coordinator` varchar(255) DEFAULT NULL,
  `secondary_coordinator` varchar(255) DEFAULT NULL,
  `tier` varchar(255) DEFAULT NULL,
  `head_office_location` varchar(45) DEFAULT NULL,
  `head_office_address` varchar(255) DEFAULT NULL,
  `head_office_contact` varchar(15) DEFAULT NULL,
  `head_office_landline` varchar(15) DEFAULT NULL,
  `sector_id` int unsigned DEFAULT NULL,
  `currency_id` int unsigned DEFAULT NULL,
  `min_ctc` decimal(10,2) DEFAULT NULL,
  `max_ctc` decimal(10,2) DEFAULT NULL,
  `linkedin` varchar(512) DEFAULT NULL,
  `region` enum('NORTH','SOUTH','EAST','WEST') DEFAULT NULL,
  `tier_v2` enum('TIER_1','TIER_2','TIER_3') DEFAULT NULL,
  `status` enum('HOT','WARM','COLD') DEFAULT NULL,
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0',
  `created_by` int unsigned DEFAULT NULL,
  `created_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_placement_company_college_id_name_idx` (`college_id`,`name`),
  KEY `fk_placement_company_college_idx` (`college_id`),
  KEY `fk_placement_organziation_logo_id_idx` (`logo_id`),
  KEY `fk_placement_organization_created_by_idx` (`created_by`),
  KEY `fk_placement_organization_sector_id` (`sector_id`),
  KEY `fk_placement_organization_currency_id` (`currency_id`),
  CONSTRAINT `fk_placement_company_college` FOREIGN KEY (`college_id`) REFERENCES `college` (`college_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_organization_created_by` FOREIGN KEY (`created_by`) REFERENCES `user_attributes` (`ukid`),
  CONSTRAINT `fk_placement_organization_currency_id` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`),
  CONSTRAINT `fk_placement_organization_logo_id_media_id` FOREIGN KEY (`logo_id`) REFERENCES `media_object` (`media_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_organization_sector_id` FOREIGN KEY (`sector_id`) REFERENCES `placement_organization_sector` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2386 DEFAULT CHARSET=latin1;


-- ==================== placement_status ====================
CREATE TABLE `placement_status` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `code` char(3) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;


-- ==================== placement_student_status ====================
CREATE TABLE `placement_student_status` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `student_ukid` int unsigned NOT NULL,
  `assigned_by_ukid` int unsigned DEFAULT NULL,
  `status_id` int unsigned NOT NULL DEFAULT '2',
  `standing_backlog` int DEFAULT '0',
  `total_backlog` int DEFAULT '0',
  `placement_cycle_log` json DEFAULT NULL,
  `created_timestamp` timestamp NULL DEFAULT NULL,
  `modified_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_ukid_UNIQUE` (`student_ukid`),
  KEY `fk_placement_student_status_1_idx` (`assigned_by_ukid`),
  KEY `fk_placement_student_status_2_idx` (`student_ukid`),
  KEY `fk_placement_student_status_3_idx` (`status_id`),
  CONSTRAINT `fk_placement_student_status_1` FOREIGN KEY (`assigned_by_ukid`) REFERENCES `authenticator` (`ukid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_student_status_3` FOREIGN KEY (`status_id`) REFERENCES `placement_status` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_placement_student_status_auth_ukid` FOREIGN KEY (`student_ukid`) REFERENCES `authenticator` (`ukid`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45292 DEFAULT CHARSET=latin1;



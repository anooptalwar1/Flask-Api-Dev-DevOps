-- -----------------------------------------------------
-- Schema user_management_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `user_management_db`;
CREATE SCHEMA `user_management_db`;
USE `user_management_db` ;

-- -----------------------------------------------------
-- Table `user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `level` ENUM('ADMIN', 'TECH_SUPPORT', 'REMOTE_OPERATOR', 'READ_ONLY') NOT NULL DEFAULT 'READ_ONLY',
  `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_deactive` TINYINT NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC));


-- -----------------------------------------------------
-- Table `session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `session` (
  `user_id` INT NOT NULL,
  `status` ENUM('ONLINE', 'OFFLINE', 'BUSY') NOT NULL DEFAULT 'OFFLINE',
  `device_type` ENUM('HOLOLENS', 'ANDROID') NULL DEFAULT NULL,
  `device_ip` VARCHAR(45) NULL DEFAULT NULL,
  `start_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `hololens_username` VARCHAR(45) NULL DEFAULT NULL,
  `hololens_password` VARCHAR(45) NULL DEFAULT NULL,
  `session_id` VARCHAR(85) NULL DEFAULT NULL,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`));


-- -----------------------------------------------------
-- Table `session_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `session_log` (
  `session_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `device_type` ENUM('HOLOLENS', 'ANDROID') NOT NULL,
  `device_ip` VARCHAR(45) NOT NULL,
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NOT NULL,
  PRIMARY KEY (`session_id`),
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `id`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`));

-- -----------------------------------------------------
-- View `online_android_users_view`
-- -----------------------------------------------------
CREATE VIEW `online_android_users_view` AS select `user`.`name` AS `name`,`session`.`device_ip` AS `device_ip`,`session`.`status` AS `status` from (`user` join `session`) where ((`session`.`device_type` = 'ANDROID') and (`session`.`status` <> 'OFFLINE') and (`user`.`id` = `session`.`user_id`));

-- -----------------------------------------------------
-- View `online_hololens_users_view`
-- -----------------------------------------------------
CREATE VIEW `online_hololens_users_view` AS select `user`.`name` AS `name`,`session`.`device_ip` AS `device_ip`,`session`.`status` AS `status`,`session`.`hololens_username` AS `hololens_username`,`session`.`hololens_password` AS `hololens_password` from (`user` join `session`) where ((`session`.`device_type` = 'HOLOLENS') and (`session`.`status` <> 'OFFLINE') and (`user`.`id` = `session`.`user_id`));

-- -----------------------------------------------------
-- View `users_for_dashboard_view`
-- -----------------------------------------------------
CREATE VIEW `users_for_dashboard_view` AS select `user`.`id` AS `id`,`user`.`name` AS `name`,`user`.`email` AS `email`,`user`.`level` AS `level`,`user`.`created_on` AS `created_on`,`user`.`modified_on` AS `modified_on` from `user` where (`user`.`is_deactive` = 0);

-- -----------------------------------------------------
-- Trigger `user_AFTER_INSERT`
-- -----------------------------------------------------
CREATE TRIGGER `user_AFTER_INSERT` AFTER INSERT ON `user` FOR EACH ROW INSERT INTO `session`(`user_id`) values (new.id);

-- -----------------------------------------------------
-- Trigger `user_BEFORE_UPDATE`
-- -----------------------------------------------------
CREATE TRIGGER `user_BEFORE_UPDATE` BEFORE UPDATE ON `user` FOR EACH ROW SET new.modified_on=CURRENT_TIMESTAMP();

-- -----------------------------------------------------
-- Trigger `session_AFTER_UPDATE`
-- -----------------------------------------------------
DELIMITER $$
CREATE TRIGGER `session_AFTER_UPDATE` AFTER UPDATE ON `session` FOR EACH ROW
BEGIN
	IF (new.status = 'OFFLINE') THEN 
		INSERT INTO `session_log`(`user_id`,`device_type`,`device_ip`,`start_time`,`end_time`) values (new.user_id, new.device_type, new.device_ip, new.start_time, new.end_time);
	END IF;
END$$

-- -----------------------------------------------------
-- Initial Data Insert into `user` table
-- -----------------------------------------------------
INSERT INTO `user`(`name`,`email`,`password`,`level`) VALUES ('Admin Admin','admin.admin@email.com','admin@123','ADMIN');
-- -----------------------------------------------------
-- Schema user_management_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `procedure_management_db`;
CREATE SCHEMA `procedure_management_db`;
USE `procedure_management_db` ;


-- -----------------------------------------------------
-- Table `object`
-- -----------------------------------------------------
CREATE TABLE `object` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(70) NOT NULL,
  `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC));


-- -----------------------------------------------------
-- Table `procedure`
-- -----------------------------------------------------
CREATE TABLE `procedure` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` TEXT NOT NULL,
  `spec_reference` TEXT NOT NULL,
  `dept` TEXT NOT NULL,
  `document_id` TEXT NOT NULL,
  `tools` TEXT NOT NULL,
  `safety_req` TEXT NOT NULL,
  `purpose` TEXT NOT NULL,
  `escalation_plan` TEXT NOT NULL,
  `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by_user_id` INT NOT NULL,
  `is_deactive` TINYINT NOT NULL DEFAULT '0',
  `object_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `object_id_fk_idx` (`object_id` ASC) VISIBLE,
  CONSTRAINT `object_id_fk`
    FOREIGN KEY (`object_id`)
    REFERENCES `object` (`id`)
    ON DELETE CASCADE);


-- -----------------------------------------------------
-- Table `step`
-- -----------------------------------------------------
CREATE TABLE `step` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` TEXT NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `type` ENUM('TEXT', 'VIDEO') NOT NULL DEFAULT 'TEXT',
  `sequence_number` INT NOT NULL,
  `procedure_id` INT NOT NULL,
  `media_url` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `procedure_id_fk_idx` (`procedure_id` ASC) VISIBLE,
  CONSTRAINT `procedure_id_fk`
    FOREIGN KEY (`procedure_id`)
    REFERENCES `procedure` (`id`)
    ON DELETE CASCADE);


-- -----------------------------------------------------
-- Trigger `procedure_BEFORE_UPDATE`
-- -----------------------------------------------------
CREATE TRIGGER `procedure_BEFORE_UPDATE` BEFORE UPDATE ON `procedure` FOR EACH ROW SET new.modified_on=CURRENT_TIMESTAMP();


-- -----------------------------------------------------
-- Initial Data Insert into `user` table
-- -----------------------------------------------------
INSERT INTO `object`(`name`) VALUES ('Robotic Arm');
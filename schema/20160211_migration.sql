ALTER TABLE `category` ADD COLUMN `user_fk` INT(11) DEFAULT 1 AFTER `name`;
ALTER TABLE `category` ADD COLUMN `hide_in_report` BOOL DEFAULT FALSE AFTER `user_fk`;

DROP PROCEDURE IF EXISTS update_categories;

DELIMITER #
CREATE PROCEDURE update_categories()
  BEGIN

    DECLARE user_id INT UNSIGNED DEFAULT 1;

    START TRANSACTION;
    loop_label: WHILE user_id < 15 DO

      SET user_id = user_id + 1;

      IF user_id = 5
      THEN
        ITERATE loop_label;
      END IF;
      IF user_id = 9
      THEN
        ITERATE loop_label;
      END IF;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("alcohol", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 3 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("bills", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 6 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("clothing", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 13 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("entertainment", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 10 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("food (in)", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 1 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("food (out)", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 2 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("household", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 8 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("medical", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 11 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("miscellaneous", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 7 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("rent/mortgage", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 5 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("transportation", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 4 AND `user_fk` = user_id;

      INSERT INTO `category` (`name`, `user_fk`) VALUES ("travel/vacation", user_id);
      UPDATE `expense` SET `category_fk` = (SELECT LAST_INSERT_ID()) WHERE `category_fk` = 9 AND `user_fk` = user_id;

    END WHILE loop_label;
    COMMIT;

  END #

CALL update_categories();
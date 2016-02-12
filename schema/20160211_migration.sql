ALTER TABLE category ADD COLUMN user_fk INT(11) DEFAULT 1 AFTER name;
ALTER TABLE category ADD COLUMN hide_in_report BOOL DEFAULT FALSE AFTER user_fk;

DROP PROCEDURE IF EXISTS update_categories;

delimiter #
CREATE PROCEDURE update_categories()
BEGIN

DECLARE i INT UNSIGNED DEFAULT 1;

START TRANSACTION;
loop_label: WHILE i < 10 DO

	SET i = i+1;

	IF i=5 THEN
		ITERATE loop_label;
	END IF;
	IF i=9 THEN
		ITERATE loop_label;
	END IF;

	INSERT INTO category (`name`, `user_fk`) VALUES("alcohol", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("food (in)", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("food (out)", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("transportation", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("rent/mortgage", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("bills", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("miscellaneous", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("travel/vacation", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("entertainment", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("medical", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("clothing", i);
	INSERT INTO category (`name`, `user_fk`) VALUES("savings", i);

END WHILE loop_label;
COMMIT;

END #

CALL update_categories();
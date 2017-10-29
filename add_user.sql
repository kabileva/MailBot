DELIMITER $$
CREATE DEFINER = root@localhost PROCEDURE add_user (
        IN name VARCHAR(45),
        IN email VARCHAR(45),
        IN token VARCHAR(45),
        IN FB_id BIGINT,
        IN FB_name VARCHAR(45)
)
BEGIN
        if (select exists (select 1 from tbl_users where user_email = email) ) THEN
                select 'This email address has already been used';
        ELSE
                insert into tbl_users
                (
                        user_name,
                        user_email,
                        user_token,
                        user_FB_id,
                        user_FB_name
                )
                values
                (
                        name,
                        email,
                        token,
                        FB_id,
                        FB_name
                );
        END IF;
END $$
DELIMITER ;

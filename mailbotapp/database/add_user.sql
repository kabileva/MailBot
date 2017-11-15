
CREATE DEFINER = root@localhost PROCEDURE add_user (
        IN FB_id BIGINT,
        IN token JSON,
	OUT result INT(1)
)
        insert into tbl_users
        (
                user_FB_id,
                user_token
        )
        values
        (
                FB_id,
                token
        )    

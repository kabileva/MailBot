create table tbl_users (
        user_id BIGINT UNIQUE AUTO_INCREMENT,
        user_FB_id BIGINT NULL,
	user_token JSON NOT NULL,
        PRIMARY KEY (user_id));
